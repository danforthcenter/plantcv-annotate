# Class helpers

# Imports
import cv2
import numpy as np
from math import floor
import matplotlib.pyplot as plt
from scipy.spatial import distance


def _find_closest_pt(pt, pts):
    """
    Find the closest (Euclidean) point to a given point from a list of points.

    Inputs:
    pt           = coordinates of a point 
    pts          = a list of tuples (coordinates) 

    Outputs:
    idx         = index of the closest point 
    coord       = coordinates of the closest point

    :param pt: tuple
    :param pts:  list
    :return idx: int
    :return coord: tuple
    """
    if pt in pts:
        idx = pts.index(pt)
        return idx, pt

    dists = distance.cdist([pt], pts, 'euclidean')
    idx = np.argmin(dists)
    return idx, pts[idx]

class Points:
    """Point annotation/collection class to use in Jupyter notebooks. It allows the user to
    interactively click to collect coordinates from an image. Left click collects the point and
    right click removes the closest collected point
    """

    def __init__(self, img, figsize=(12, 6)):
        """Initialization
        :param img: image data
        :param figsize: desired figure size, (12,6) by default
        :attribute points: list of points as (x,y) coordinates tuples
        """
        self.fig, self.ax = plt.subplots(1, 1, figsize=figsize)
        self.ax.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

        self.points = []
        self.events = []

        self.fig.canvas.mpl_connect('button_press_event', self.onclick)

    def onclick(self, event):
        """Handle mouse click events."""
        self.events.append(event)
        if event.button == 1:

            self.ax.plot(event.xdata, event.ydata, 'x', c='red')
            self.points.append((floor(event.xdata), floor(event.ydata)))

        else:
            idx_remove, _ = _find_closest_pt((event.xdata, event.ydata), self.points)
            # remove the closest point to the user right clicked one
            self.points.pop(idx_remove)
            self.ax.lines[idx_remove].remove()
        self.fig.canvas.draw()
