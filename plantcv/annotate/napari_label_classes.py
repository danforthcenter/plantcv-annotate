# Use Napari to Label

import numpy as np
import random
from plantcv.annotate import napari_open
from plantcv.annotate import napari_classes


def napari_label_classes(img, classes=False, size=10, shape='square',
                         importdata=False, show=True):
    """
    open img in napari and label classes

    Inputs:
    img  = img  (grayimg, rgbimg, or hyperspectral image array data
        e.g. hyperspectraldata.array_data). Adding labels works best on an
        image that has objects segmented/classified with contours/clusters
        labeled with values (e.g. labeled mask, output of kmeans clustering).
    classes = list of labels or classes. If no points are selected for a class,
        data without labels will default to this class when napari_join_labels
        is run. If all classes have points labeled, any clusters not labeled
        will default to the last class in the list when napari_join_labels is
        run.
    size = size of marker in pixels
    shape = either 'square' or 'circle'
    importdata = dictionary of values in Napari format (y,x).
        Output of napari_read_coor
    show = if show is True the viewer is launched. This opetion is useful for
    running tests without triggering the viewer.

    Returns:
    viewer  = Napari viewer object

    :param img: numpy.ndarray
    :param classes: list
    :param size: int
    :param shape: str
    :param importdata: dict
    :param show: str
    :return viewer: napari viewer object

    """
    showcall = show
    viewer = napari_open(img, show=showcall)

    color = ['red', 'blue', 'purple', 'green', 'orange', 'yellow', 'cyan',
             'magenta']

    keys = napari_classes(viewer)

    if classes is not False:
        for x in classes:
            if x in keys:
                pass
            else:
                viewer.add_points(np.array([]), name=x, symbol=shape,
                                  face_color=random.choice(color), size=size)
        keys = napari_classes(viewer)

    if importdata is not False:
        importkeys = list(importdata.keys())
        for key in importkeys:
            if len(importdata[key]) != 0:
                if key in keys:
                    viewer.layers[key].add(importdata[key])
                else:
                    viewer.add_points(importdata[key], name=key, symbol=shape,
                                      face_color=random.choice(color),
                                      size=size)

    return viewer
