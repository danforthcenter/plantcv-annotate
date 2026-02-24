# Import points from json file

import json


def napari_read_coor(coor, dataformat='yx'):
    """Open img in napari and label classes

    Parameters
    ----------
    coor : dict or str
        Either a dictionary or path to json file of points and label classes.
    dataformat : str
        Use 'xy' for points function outputs, 'yx' for Napari outputs, and 'sam' for
        Segment Anything Model, which includes "pos" and "neg" labeled classes;
        defaults to 'yx'.

    Returns
    ----------
    dict
        Dictionary of points data.
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

        for i in enumerate(data['pos']):
            x, y = i[1]
            pointslist.append([x, y])
            pointslabel.append(1)

        for i in enumerate(data['neg']):
            x, y = i[1]
            pointslist.append([x, y])
            pointslabel.append(0)

        data1['points'] = [pointslist]
        data1['labels'] = [pointslabel]
        data = data1

    return data
