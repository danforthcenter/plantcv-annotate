# Save Napari Data to a File

import json
import os
from plantcv.annotate import napari_classes


def napari_save_coor(viewer, filepath):
    """
    save napari labeled points to a file

    Inputs:
    viewer = Napari viewer object
    filepath = path to file to save data to

    Returns:
    dictionary  = dictionary of saved data points

    :param viewer: napari viewer object
    :param filepath: str
    :return dictionary: dictionary

    """
    classes = napari_classes(viewer)
    datadict = {}

    for label in classes:
        coordict = []
        for i, (x, y) in enumerate(viewer.layers[label].data):
            x = int(x)
            y = int(y)
            coordict.append((x, y))
        datadict.update({label: coordict})

    if os.path.exists(filepath):
        filepath = str(filepath)+"_1.txt"
    with open(filepath, 'w') as fp:
        fp.write(json.dumps(datadict))
        fp.close()

    return datadict
