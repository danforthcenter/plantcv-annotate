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
    maskdict = napari_points_mask(img, viewer)

    summask = int((np.sum(maskdict['total']))/255)

    assert summask == 2500
    viewer.close()
