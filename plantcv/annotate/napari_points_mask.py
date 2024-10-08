# Make Masks of Labelled Napari Points

import numpy as np
import os
import cv2
from plantcv.annotate import napari_classes
from plantcv.plantcv import params
from plantcv.plantcv._debug import _debug


def napari_points_mask(img, viewer):
    """
    draw points mask based on Napari viewer annotations

    Inputs:
    img  = img  (grayimg, rgbimg, or hyperspectral image array data
        e.g. hyperspectraldata.array_data). This is used to find the x,y size
        of the image
    viewer = Napari Viewer with classes labeled. The size of the masked points
        will be from the viewer parameters

    Returns:
    mask_dict   = dictionary of masks; mask for each labelled class

    :param img: numpy.ndarray
    :param viewer: Napari Viewer object
    :param shape: str
    :return mask_dict: dict of numpy.ndarray

    """
    # get shape of image
    size = np.shape(img)
    keys = napari_classes(viewer)
    maskdict = {}

    for key in keys:
        maskname = str(key)
        mask = np.zeros((size[0], size[1]))
        data = list(viewer.layers[key].data)
        shapesize = viewer.layers[key]._current_size
        shapesizehalf = int(shapesize/2)

        for y, x in data:
            startpoint = (int(x-shapesizehalf), int(y-shapesizehalf))
            endpoint = (int(x+shapesizehalf-1), int(y+shapesizehalf-1))
            mask = cv2.rectangle(mask, startpoint, endpoint, (255), -1)

        maskdict[maskname] = mask

        _debug(visual=mask, filename=os.path.join(params.debug_outdir,
                                                  str(params.device) +
                                                  str(maskname) +
                                                  '_labeled_mask.png'))

    return maskdict
