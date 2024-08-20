# Get Data from Dictionary of Masks and Format for Naive Bayes

import pandas as pd
import numpy as np


def napari_naive_bayes_colors(img, maskdict, filename):
    """
    get names of napari keys

    Inputs:
    img  = rgb image
    maskdict = dictionary of masks, output of napari_points_mask for example
    filename = name/path of file to save data

    Returns:
    dataarray  = pandas data array

    :param img: RGB image
    :param maskdict = dictionary of masks
    :param filename = str
    :return dataarray: pandas dataframe
    """
    keys = list(maskdict.keys())
    datadict = {}
    for key in keys:
        mask = maskdict[key]
        nonzero = np.transpose(np.nonzero(mask))
        keydata = []
        for x, y in nonzero:
            rgbdata = list(img[x][y])
            rgblist = ", ".join(repr(int(e)) for e in rgbdata)
            keydata.append(rgblist)
        dict1 = {key: keydata}
        datadict.update(dict1)
    dataarray = pd.DataFrame.from_dict(datadict, orient='index')
    datatranspose = dataarray.transpose()
    datatranspose.to_csv(filename, sep="\t", index=False)

    return datatranspose
