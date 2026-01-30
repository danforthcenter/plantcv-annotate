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

    if dataformat == 'sam':
        pointslist = []
        pointslabel = []

        for i in range(len(data['pos'])):
            x, y = data['pos'][i]
            pointslist.append([x, y])
            pointslabel.append(1)

        for i in range(len(data['neg'])):
            x, y = data['neg'][i]
            pointslist.append([x, y])
            pointslabel.append(0)

        pointslist = [pointslist]
        pointslabel = [pointslabel]
        data1['points'] = pointslist
        data1['labels'] = pointslabel
        data = data1

    return data
