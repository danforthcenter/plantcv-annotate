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



def _remove_points(autolist, confirmedlist):
    """Function to remove points if interactively removed by user
    Inputs:
    autolist      = total list of coordinates, automatically generated
                    from the contents of coords attribute
    confirmedlist = coordinates of 'auto' detected points (e.g. coordinate
                    output of pcv.filters.eccentricity)
    Returns:
    removecoor    = list of coordinates (of objects to remove from the binary mask)
    :param autolist: list
    :param confirmedlist: list
    :return  removecoor: list
    """
    # internal function to remove to remove points specified by a user
    removecoor = []
    for element in autolist:
        if element not in confirmedlist:
            removecoor.append(element)
    return removecoor

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

    def correct_mask(self, bin_img, bin_img_recover, coords):
        """View coordinates for a specific class label.

        Parameters
        ----------
        bin_img : numpy.ndarray
            binary image, filtered mask image with selected objects
        bin_img_recover : numpy.ndarray
            binary image, unclean mask image with all potential objects
        coords : list
            coordinates of 'auto' detected points (coordinate output of annotate.get_centroids)

        Returns
        ----------
        completed_mask : numpy.ndarray
            corrected binary mask with recovered and removed objects
        """
        from plantcv.plantcv.floodfill import floodfill

        debug = params.debug
        params.debug = None

        labelnames = list(self.count)

        completed_mask = np.copy(bin_img)

        totalcoor = []
        unrecovered_ids = []

        for names in labelnames:
            for i, (x, y) in enumerate(self.coords[names]):
                x = int(x)
                y = int(y)
                totalcoor.append((y, x))

        removecoor = _remove_points(coords, totalcoor)
        removecoor = list(map(lambda sub: (sub[1], sub[0]), removecoor))
        completed_mask = floodfill(completed_mask, removecoor, 0)

        # points in class used for recovering and labeling
        for names in labelnames:
            for i, (x, y) in enumerate(self.coords[names]):
                x = int(x)
                y = int(y)
                # corrected coordinates
                if completed_mask[y, x] == 0 and bin_img_recover[y,x] > 0:
                    print(f"Recovering object at coordinates: x = {x}, y = {y}")
                    total_mask_minus_objs = floodfill(bin_img_recover, [(x, y)], 0)
                    recovered_objs = bin_img_recover - total_mask_minus_objs
                    completed_mask = completed_mask + recovered_objs
                elif completed_mask[y, x] == 0 and bin_img_recover[y,x] == 0:
                    print(f"Un-Recoverable object at coordinates: x = {x}, y = {y}")
                    unrecovered_ids.append(i)

            # Split up "coords" attribute into two classes
            unrec_points = []
            for id in unrecovered_ids:
                (x, y) = self.coords[names][id]
                unrec_points.append((x, y))
            new_name = str(names) + "_unrecovered"
            # Pull out unrecovered coords into new class
            self.coords[new_name] = unrec_points
            # Overwrite class with only coords that have corresponding objects in the completed_mask
            new_points = []
            for i, (x, y) in enumerate(self.coords[names]):
                if i not in unrecovered_ids:
                    new_points.append((x, y))

            self.coords[names] = new_points


        completed_mask1 = 1*((completed_mask + 1*(completed_mask == 255)) != 0).astype(np.uint8)

        params.debug = debug

        _debug(visual=completed_mask1,
            filename=os.path.join(params.debug_outdir,
                                    f"{params.device}_annotation-corrected.png"))

        return completed_mask1

