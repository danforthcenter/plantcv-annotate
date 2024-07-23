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

        Returns
        ----------
        final_mask : numpy.ndarray
            corrected and labeled mask with recovered and removed objects
        """
        from plantcv.plantcv import color_palette

        debug = params.debug
        params.debug = None

        labelnames = list(self.count)
        totalcoor = []
        unrecovered_ids = []
        debug_coords = []
        debug_labels = []
        pts_mask = np.zeros(np.shape(bin_img), np.uint8)
        final_mask = pts_mask.copy()
        debug_img = pts_mask.copy()
        debug_img = cv2.cvtColor(debug_img, cv2.COLOR_GRAY2RGB)

        for names in labelnames:
            for i, (x, y) in enumerate(self.coords[names]):
                x = int(x)
                y = int(y)
                totalcoor.append((y, x))
                # Draw pt annotations onto a blank mask
                pts_mask = cv2.circle(pts_mask, (x, y), radius=0, color=(255), thickness=-1)
        # Create a labeled mask from the input mask
        labeled_mask, total_obj_num = create_labels(mask=bin_img)
        labeled_mask1 = np.copy(labeled_mask)
        # Objects that overlap with one or more annotations get kept
        masked_image = apply_mask(img=labeled_mask1, mask=pts_mask, mask_color='black')
        keep_object_ids = np.unique(masked_image)
        # Create a color scale, use a previously stored scale if available
        rand_color = color_palette(num=len(keep_object_ids), saved=True)

        # Fill in objects that are not overlapping with an annotation
        for i in range(1, total_obj_num + 1):
            if i not in keep_object_ids:
                labeled_mask1[np.where(labeled_mask == i)] = 0
                debug_img[np.where(labeled_mask == i)] = (50,50,50)
        # Create new binary mask after filtering un-annotated objects
        completed_mask_bin = np.where(labeled_mask1 > 0, 255, 0)
        # Create a new labeled annotation mask to determine number of annotation per object
        labeled_mask_all, _ = create_labels(mask=completed_mask_bin)

        # points in class used for recovering and labeling
        for names in labelnames:
            for i, (x, y) in enumerate(self.coords[names]):
                x = int(x)
                y = int(y)
                mask_pixel_value = labeled_mask_all[y, x]
                text = f"ID:{i}"
                
                debug_coords.append(tuple([x,y]))
                debug_labels.append(text)
                
                if mask_pixel_value == 0:
                    print(f"Un-Recoverable object at coordinate: x = {x}, y = {y}")
                    unrecovered_ids.append(i)
                    # Add a pixel where unresolved annotation to the mask
                    final_mask = cv2.circle(final_mask, (x, y), radius=0, color=(i), thickness=-1)
                    # Add a thicker pixel where unresolved annotation to the debug img
                    debug_img = cv2.circle(debug_img, (x, y), radius=params.line_thickness, color=(i), thickness=-1)
                else:
                    # DRAW on labeled mask with correct pixel value (object ID and np.where to copy with new label ID i)
                    final_mask = np.where(labeled_mask_all == mask_pixel_value, i, final_mask)
                    debug_img = np.where(labeled_mask_all == mask_pixel_value, i, final_mask)
        for id, id_label in enumerate(debug_labels):
            cv2.putText(img=debug_img, text=id_label, org=debug_coords[id], fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                        fontScale=params.text_size, color=(150, 150, 150), thickness=params.text_thickness)
        params.debug = debug
        _debug(visual=final_mask,
               filename=os.path.join(params.debug_outdir,
                                     f"{params.device}_annotation-corrected.png"))
        _debug(visual=debug_img,
               filename=os.path.join(params.debug_outdir,
                                     f"{params.device}_annotation-corrected-debug.png"))
        # Count the number of objects in the final mask
        num = len(np.unique(final_mask))

        return final_mask, num, debug_img
