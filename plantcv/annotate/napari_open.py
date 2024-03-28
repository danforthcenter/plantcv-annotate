# Use Napari to Label

import napari
import cv2
import numpy as np
from skimage.color import label2rgb


def napari_open(img, show=True):
    """
    open img in napari and label classes

    Inputs:
    img  = img  (grayimg, rgbimg, or hyperspectral image array data e.g.
    hyperspectraldata.array_data)
    show = if show is True the viewer is launched. This opetion is useful for
    running tests without triggering the viewer.

    Returns:
    viewer  = napari viewer object

    :param img: numpy.ndarray
    :return viewer: napari viewer object

    """
    shape = np.shape(img)
    showcall = show
    if len(shape) == 2:
        colorful = label2rgb(img)
        img = (255*colorful).astype(np.uint8)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    if len(shape) == 3:
        if shape[2] == 3:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        if shape[2] > 3:
            img = img.transpose(2, 0, 1)

    viewer = napari.view_image(img, show=showcall)

    return viewer
