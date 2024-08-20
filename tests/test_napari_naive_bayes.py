import os
import numpy as np
from plantcv.plantcv import readimage
from plantcv.annotate import napari_naive_bayes_colors


def test_napari_join_labels(test_data, tmpdir):
    """Test for PlantCV.Annotate"""
    # Read in test data
    cache_dir = tmpdir.mkdir("cache")
    img, _, _ = readimage(test_data.nb_rgb)
    maskdict = np.load(test_data.nb_mask, allow_pickle='TRUE').item()
    filename = os.path.join(cache_dir, 'tempfile.txt')
    data = napari_naive_bayes_colors(img, maskdict, filename)

    assert data.shape == (16, 1)
