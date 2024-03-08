# Get Napari Keys

import re


def napari_keys(viewer):
    """
    get names of napari keys

    Inputs:
    viewer  = napari viewer object

    Returns:
    labels  = napari key value names

    :param viewer: napari.viewer.Viewer
    :return labels: numpy.ndarray, list
    """
    keylist = [key for key in viewer.layers]
    keylist = ''.join(str(keylist))
    keylist = keylist.split(',')

    labels = []
    for x in keylist:
        if re.search('Image layer', x):
            pass
        else:
            y = x.split(" ")
            labels.append(y[3].strip("\'"))

    return labels
