# Class helpers

# Imports
import os
import cv2
import json
import numpy as np
from math import floor
import matplotlib.pyplot as plt
from plantcv.plantcv.annotate.points import _find_closest_pt
from plantcv.plantcv import warn, params
from plantcv.plantcv._debug import _debug
from plantcv.plantcv import create_labels, apply_mask
import time



class Points:
    """Point annotation/collection class to use in Jupyter notebooks. It allows the user to
    interactively click to collect coordinates from an image. Left click collects the point and
    right click removes the closest collected point.
    """

    def __init__(self, img, figsize=(12, 6), label="default", color="r", view_all=False):
        """Points initialization method.

        Parameters
        ----------
        img : numpy.ndarray
            image to annotate
        figsize : tuple, optional
            figure plotting size, by default (12, 6)
        label : str, optional
            class label, by default "default"
        """
        self.img = img
        self.figsize = figsize
        self.label = label  # current label
        self.color = color  # current color
        self.view_all = view_all  # a flag indicating whether or not view all labels
        self.coords = {}  # dictionary of all coordinates per group label
        self.events = []  # includes right and left click events
        self.count = {}  # a dictionary that saves the counts of different groups (labels)
        self.sample_labels = []  # list of all sample labels, one to one with points collected
        self.colors = {}  # all used colors

        self.view(label=self.label, color=self.color, view_all=self.view_all)

    def onclick(self, event):
        """Handle mouse click events

        Parameters
        ----------
        event : matplotlib.backend_bases.MouseEvent
            matplotlib MouseEvent object
        """
        print(type(event))
        self.events.append(event)
        if event.button == 1:
            # Add point to the plot
            self.ax.plot(event.xdata, event.ydata, marker='x', c=self.color)
            self.coords[self.label].append((floor(event.xdata), floor(event.ydata)))
            self.count[self.label] += 1
            self.sample_labels.append(self.label)
        else:
            idx_remove, _ = _find_closest_pt((event.xdata, event.ydata), self.coords[self.label])
            # remove the closest point to the user right clicked one
            self.coords[self.label].pop(idx_remove)
            self.count[self.label] -= 1
            idx_remove = idx_remove + self.p_not_current
            self.ax.lines[idx_remove].remove()
            self.sample_labels.pop(idx_remove)
        self.fig.canvas.draw()

    def print_coords(self, filename):
        """Save collected coordinates to a file.

        Parameters
        ----------
        filename : str
            output filename
        """
        # Open the file for writing
        with open(filename, "w") as fp:
            # Save the data in JSON format with indentation
            json.dump(obj=self.coords, fp=fp, indent=4)

    def import_list(self, coords, label="default"):
        """Import coordinates.

        Parameters
        ----------
        coords : list
            list of coordinates (tuples)
        label : str, optional
            class label, by default "default"
        """
        if label not in self.coords:
            self.coords[label] = []
            for (y, x) in coords:
                self.coords[label].append((x, y))
            self.count[label] = len(self.coords[label])
            self.view(label=label, color=self.color, view_all=False)
        else:
            warn(f"{label} already included and counted, nothing is imported!")

    def import_file(self, filename):
        """Import coordinates from a file.

        Parameters
        ----------
        filename : str
            JSON file containing Points annotations
        """
        with open(filename, "r") as fp:
            coords = json.load(fp)

        keys = list(coords.keys())

        for key in keys:
            keycoor = coords[key]
            keycoor = list(map(lambda sub: (sub[1], sub[0]), keycoor))
            self.import_list(keycoor, label=key)

    def view(self, label="default", color="r", view_all=False):
        """View coordinates for a specific class label.

        Parameters
        ----------
        label : str, optional
            class label, by default "default"
        color : str, optional
            marker color, by default "r"
        view_all : bool, optional
            view all classes or a single class, by default False
        """
        if label not in self.coords and color in self.colors.values():
            warn("The color assigned to the new class label is already used, if proceeding, "
                 "items from different classes will not be distinguishable in plots!")
        self.label = label
        self.color = color
        self.view_all = view_all

        if self.label not in self.coords:
            self.coords[self.label] = []
            self.count[self.label] = 0
        self.colors[self.label] = self.color

        self.fig, self.ax = plt.subplots(1, 1, figsize=self.figsize)

        self.events = []
        self.fig.canvas.mpl_connect('button_press_event', self.onclick)

        self.ax.imshow(cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB))
        self.ax.set_title("Please left click on objects\n Right click to remove")
        self.p_not_current = 0
        # if view_all is True, show all already marked markers
        if self.view_all:
            for k in self.coords:
                for (x, y) in self.coords[k]:
                    self.ax.plot(x, y, marker='x', c=self.colors[k])
                    if self.label not in self.coords or len(self.coords[self.label]) == 0:
                        self.p_not_current += 1
        else:
            for (x, y) in self.coords[self.label]:
                self.ax.plot(x, y, marker='x', c=self.color)

    def correct_mask(self, bin_img):
        """View coordinates for a specific class label.

        Parameters
        ----------
        bin_img : numpy.ndarray
            binary image, filtered mask image with selected objects
        bin_img_recover : numpy.ndarray
            binary image, unclean mask image with all potential objects

        Returns
        ----------
        completed_mask : numpy.ndarray
            corrected binary mask with recovered and removed objects
        """
        tic = time.perf_counter()
        from plantcv.plantcv.floodfill import floodfill

        debug = params.debug
        params.debug = None

        labelnames = list(self.count)

        completed_mask = np.copy(bin_img)

        totalcoor = []
        unrecovered_ids = []
        pts_mask = np.zeros(np.shape(bin_img))

        for names in labelnames:
            for i, (x, y) in enumerate(self.coords[names]):
                x = int(x)
                y = int(y)
                totalcoor.append((y, x))
                # Draw pt annotations onto a blank mask
                pts_mask = cv2.circle(pts_mask, (x, y), radius=0, color=(255), thickness=-1)

        # Only removes objects that were auto detected and then removed
        labeled_mask, total_obj_num = create_labels(mask=bin_img)
        # Objects that overlap with annotations get kept
        masked_image = apply_mask(img=labeled_mask, mask=pts_mask, mask_color='black')
        keep_object_ids = np.unique(masked_image)

        for i in range(1, total_obj_num):
            if i not in keep_object_ids:
                # Fill in objects that are not overlapping with an annotation
                labeled_mask[np.where(labeled_mask == i)] = 0
        completed_mask = np.where(labeled_mask > 0, 255, 0)

        # points in class used for recovering and labeling
        for names in labelnames:
            for i, (x, y) in enumerate(self.coords[names]):
                x = int(x)
                y = int(y)
                if completed_mask[y, x] == 0 and bin_img[y, x] == 0:
                    print(f"Un-Recoverable object at coordinate: x = {x}, y = {y}")
                    unrecovered_ids.append(i)

            # Split up "coords" attribute into two classes
            if len(unrecovered_ids) > 0:
                unrec_points = []
                for id in unrecovered_ids:
                    (x, y) = self.coords[names][id]
                    unrec_points.append((x, y))
                # Put unrecovered coords into new class
                self.coords[str(names)+"_unrecovered"] = unrec_points
                # Overwrite attribute, only coords that have corresponding objects in the completed_mask
                new_points = []
                for i, (x, y) in enumerate(self.coords[names]):
                    if i not in unrecovered_ids:
                        new_points.append((x, y))
                self.coords[names] = new_points

        params.debug = debug

        _debug(visual=completed_mask,
               filename=os.path.join(params.debug_outdir,
                                     f"{params.device}_annotation-corrected.png"))
        toc = time.perf_counter()
        print(f"Function ran in {toc - tic:0.4f} seconds")
        return completed_mask

    def correct_mask2(self, bin_img):
        """View coordinates for a specific class label.

        Parameters
        ----------
        bin_img : numpy.ndarray
            binary image, filtered mask image with selected objects
        bin_img_recover : numpy.ndarray
            binary image, unclean mask image with all potential objects

        Returns
        ----------
        completed_mask : numpy.ndarray
            corrected binary mask with recovered and removed objects
        """
        from skimage.color import label2rgb
        from skimage.measure import label

        tic = time.perf_counter()
        # Output mask
        outmask = np.zeros(bin_img.shape)
        # Annotation mask
        ptmask = np.zeros(bin_img.shape, dtype=np.uint8)

        # Add one pixel to the annotation mask for each point
        for lbl in self.coords:
            for x, y in self.coords[lbl]:
                ptmask[y, x] = 255
        
        # Create a labeled mask from the input mask
        labeled_mask, num_labels = label(bin_img, background=0, return_num=True, connectivity=2)
        # Filter the mask based on annotations
        for i in range(1, num_labels + 1):
            if np.max(ptmask[np.where(labeled_mask == i)]) == 255:
                outmask[np.where(labeled_mask == i)] = i
        # Debug output
        colorful = label2rgb(outmask)
        colorful = ((255*colorful).astype(np.uint8))
        _debug(visual=colorful, 
               filename=os.path.join(params.debug_outdir, f"{params.device}_corrected_labeled_mask.png"))

        toc = time.perf_counter()
        print(f"Function ran in {toc - tic:0.4f} seconds")
        return outmask
