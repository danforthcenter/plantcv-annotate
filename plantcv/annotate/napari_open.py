# Use Napari to Label

import cv2
import numpy as np
from skimage.color import label2rgb
import napari


def napari_open(img, mode='native', show=True):
    """Open an image with a napari interactive viewer

    Parameters
    ----------
    img : numpy.ndarray
        Image to be opened, img can be gray, rgb, or multispectral
    mode: str
        Viewing mode, either 'native' (default) or 'colorize'
    show: bool
        if show is True the viewer is launched. This option is useful for
    running tests without triggering the viewer.

    Returns
    -------
    napari.viewer.Viewer
        Napari viewer object
    """
    shape = np.shape(img)
    if len(shape) == 2 and mode == 'colorize':
        colorful = label2rgb(img)
        img = (255*colorful).astype(np.uint8)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    if len(shape) == 3:
        if shape[2] == 3:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        if shape[2] > 3:
            img = img.transpose(2, 0, 1)
    showcall = show
    viewer = napari.Viewer(show=showcall)
    viewer.add_image(img)
    return viewer
