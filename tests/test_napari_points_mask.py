from plantcv.annotate import napari_points_mask
from plantcv.plantcv import readimage
from plantcv.annotate import napari_label_classes
import numpy as np


def test_napari_points_mask(test_data):
    """Test for PlantCV.Annotate"""
    # Read in test data
    img, _, _ = readimage(test_data.small_rgb_img)
    data = {'total': [(25, 25)], 'background': [(50, 50)]}
    viewer = napari_label_classes(img, ['total'], size=50, importdata=data,
                                  show=False)
    maskdict = napari_points_mask(img, viewer, shape='square')
    maskdict1 = napari_points_mask(img, viewer, shape='circle')

    summask = int((np.sum(maskdict['total']))/255)
    summask1 = int((np.sum(maskdict1['total']))/255)

    assert summask == 2500
    assert summask1 == 1961
