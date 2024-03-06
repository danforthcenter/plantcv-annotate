# Class helpers

# Imports
import cv2
import json
from math import floor
import matplotlib.pyplot as plt
from plantcv.plantcv.annotate.points import _find_closest_pt
from plantcv.plantcv import warn


def _view(self, label="default", color="c", view_all=False):
    """
    View the label for a specific class label
    Inputs:
    label = (optional) class label, by default label="total"
    color = desired color, by default color="c"
    view_all = indicator of whether view all classes, by default view_all=False
    :param label: string
    :param color: string
    :param view_all: boolean
    :return:
    """
    if label not in self.coords and color in self.colors.values():
        warn("The color assigned to the new class label is already used, if proceeding, "
             "items from different classes will not be distinguishable in plots!")
    if label is not None:
        self.label = label
    self.color = color
    self.view_all = view_all

    if label not in self.coords:
        self.coords[self.label] = []
        self.count[self.label] = 0
    self.colors[self.label] = color

    self.fig, self.ax = plt.subplots(1, 1, figsize=self.figsize)

    self.events = []
    self.fig.canvas.mpl_connect('button_press_event', self.onclick)

    self.ax.imshow(cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB))
    self.ax.set_title("Please left click on objects\n Right click to remove")
    self.p_not_current = 0
    # if view_all is True, show all already marked markers
    if view_all:
        for k in self.coords:
            for (x, y) in self.coords[k]:
                self.ax.plot(x, y, marker='x', c=self.colors[k])
                if self.label not in self.coords or len(self.coords[self.label]) == 0:
                    self.p_not_current += 1
    else:
        for (x, y) in self.coords[self.label]:
            self.ax.plot(x, y, marker='x', c=color)


class Points:
    """Point annotation/collection class to use in Jupyter notebooks. It allows the user to
    interactively click to collect coordinates from an image. Left click collects the point and
    right click removes the closest collected point
    """

    def __init__(self, img, figsize=(12, 6), label="default"):
        """Initialization
        :param img: image data
        :param figsize: desired figure size, (12,6) by default
        :param label: current label for group of annotations, similar to pcv.params.sample_label
        :attribute coords: list of points as (x,y) coordinates tuples
        """
        self.img = img
        self.coords = {}  # dictionary of all coordinates per group label
        self.events = []  # includes right and left click events
        self.count = {}  # a dictionary that saves the counts of different groups (labels)
        self.label = label  # current label
        self.sample_labels = []  # list of all sample labels, one to one with points collected
        self.view_all = None  # a flag indicating whether or not view all labels
        self.color = None  # current color
        self.colors = {}  # all used colors
        self.figsize = figsize

        _view(self, label=label, color="r", view_all=True)

    def onclick(self, event):
        """Handle mouse click events."""
        self.events.append(event)
        if event.button == 1:

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
        Input variables:
        filename = Name of the file to save collected coordinate
        :param filename: str
        :return:
        """
        # Open the file for writing
        with open(filename, "w") as fp:
            # Save the data in JSON format with indentation
            json.dump(obj=self.coords, fp=fp, indent=4)

    def import_list(self, coords, label="default"):
        """Import center coordinates of already detected objects
        Inputs:
        coords = list of center coordinates of already detected objects.
        label = class label for imported coordinates, by default label="default".
        :param coords: list
        :param label: string
        :return:
        """
        if label not in self.coords:
            self.coords[label] = []
            for (y, x) in coords:
                self.coords[label].append((x, y))
            self.count[label] = len(self.coords[label])
            _view(self, label=label, color=self.color, view_all=False)
        else:
            warn(f"{label} already included and counted, nothing is imported!")

    def import_file(self, filename):
        """Method to import coordinates from file to Points object

        Inputs:
        filename = filename of stored coordinates and classes
        :param filename: str
        :return:
        """
        with open(filename, "r") as fp:
            coords = json.load(fp)

        keys = list(coords.keys())

        for key in keys:
            keycoor = coords[key]
            keycoor = list(map(lambda sub: (sub[1], sub[0]), keycoor))
            self.import_list(keycoor, label=key)

    def view(self, label="default", color="c", view_all=False):
        """Method to view current annotations

        Inputs:
        label = (optional) class label, by default label="total"
        color = desired color, by default color="c"
        view_all = indicator of whether view all classes, by default view_all=False
        :param label: string
        :param color: string
        :param view_all: boolean
        :return:
        """
        _view(self, label=label, color=color, view_all=view_all)
