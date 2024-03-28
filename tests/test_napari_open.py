import numpy as np
from plantcv.annotate import napari_open
from plantcv.plantcv import readimage


def test_napari_open_rgb(qtbot, test_data):
    """Test for PlantCV.Annotate"""
    # Read in test data
    img, _, _ = readimage(test_data.small_rgb_img)
    viewer = napari_open(img, show=False)
    coor = [(25, 25), (50, 50)]
    viewer.add_points(np.array(coor), symbol="o", name="total",
                      face_color="red", size=1)

    def check_open():
        assert np.shape(viewer.layers['total'].data) != (0, 2)

    qtbot.waitUntil(check_open, timeout=60_000)

    assert len(viewer.layers['total'].data) == 2


def test_napari_open_gray(qtbot, test_data):
    """Test for PlantCV.Annotate"""
    # Read in test data
    img, _, _ = readimage(test_data.kmeans_seed_gray_img)
    viewer = napari_open(img, show=False)
    coor = [(25, 25), (50, 50)]
    viewer.add_points(np.array(coor), symbol="o", name="total",
                      face_color="red", size=1)

    def check_open():
        assert np.shape(viewer.layers['total'].data) != (0, 2)

    qtbot.waitUntil(check_open, timeout=60_000)

    assert len(viewer.layers['total'].data) == 2


def test_napari_open_envi(qtbot, test_data):
    """Test for PlantCV.Annotate"""
    # Read in test data
    img = readimage(test_data.envi_sample_data, mode='envi')
    img = img.array_data
    viewer = napari_open(img, show=False)
    coor = [(25, 25), (50, 50)]
    viewer.add_points(np.array(coor), symbol="o", name="total",
                      face_color="red", size=1)

    def check_open():
        assert np.shape(viewer.layers['total'].data) != (0, 2)

    qtbot.waitUntil(check_open, timeout=60_000)

    assert len(viewer.layers['total'].data) == 2
