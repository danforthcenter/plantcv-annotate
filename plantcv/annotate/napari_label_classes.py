# Use Napari to Label

import numpy as np
import random
from plantcv.annotate import napari_open


def napari_label_classes(img, classes):
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

    Returns:
    viewer  = napari viewer object

    :param img: numpy.ndarray
    :return viewer: napari viewer object

    """
    viewer = napari_open(img)

    symbols = ['arrow', 'clobber', 'cross', 'diamond', 'disc', 'hbar', 'ring',
               'square', 'star', 'tailed_arrow', 'triangle_down',
               'triangle_up', 'vbar']

    for x in classes:
        viewer.add_points(np.array([]), name=x, symbol=random.choice(symbols),
                          face_color='white', size=10)

    return viewer
