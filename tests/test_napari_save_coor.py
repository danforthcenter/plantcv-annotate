import numpy as np
import os
from plantcv.annotate import napari_label_classes
from plantcv.plantcv import readimage
from plantcv.annotate import napari_save_coor


def test_napari_save_coor(test_data, tmpdir):
    """Test for PlantCV.Annotate"""
    # Read in test data
    cache_dir = tmpdir.mkdir("cache")
    img, _, _ = readimage(test_data.kmeans_seed_gray_img)
    viewer = napari_label_classes(img, ['seed'], show=False)
    coor = [(25, 25)]
    viewer.add_points(np.array(coor), symbol="o", name='background',
                      face_color="red", size=1)

    filename = os.path.join(cache_dir, 'tempfile.txt')
    # Assert that the file was created
    _ = napari_save_coor(viewer, filename)
    # Triggers addtion of _1 since filename previously exists
    _ = napari_save_coor(viewer, filename)

    assert os.path.exists(filename)
