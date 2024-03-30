# Get Napari Keys

import re


def napari_classes(viewer):
    """
    get names of napari keys
    Inputs:
    viewer  = napari viewer object
    Returns:
    classes  = napari class value names
    :param viewer: napari.viewer.Viewer
    :return labels: numpy.ndarray, list
    """
    keylist = list(viewer.layers)
    keylist = ''.join(str(keylist))
    keylist = keylist.split(',')

    classes = []
    for x in keylist:
        if re.search('Image layer', x):
            pass
        else:
            y = x.split(" ")
            classes.append(y[3].strip("\'"))

    return classes