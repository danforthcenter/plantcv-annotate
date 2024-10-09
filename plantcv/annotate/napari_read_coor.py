# Import points from json file

import json


def napari_read_coor(coor, dataformat='yx'):
    """
    open img in napari and label classes

    Inputs:
    coor  = either a dictionary of data or a path to a json file
    with dictionary of point coordinates
    dataformat = either 'yx' or 'xy'. Output of points function is in
    x,y format and Napari is in y,x format.

    Returns:
    data  = dictionary of data

    :param coor: dict or str
    :param dataformat: str
    :return data: dictionary of data in y,x format for napari

    """
    if isinstance(coor, dict):
        data = coor
    else:
        with open(coor) as json_file:
            data = json.load(json_file)
    data1 = {}
    if dataformat != 'yx':
        keys = list(data.keys())
        for key in keys:
            data2 = [(sub[1], sub[0]) for sub in data[key]]
            data1.update({key: data2})
        data = data1

    return data
