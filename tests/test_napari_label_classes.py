import numpy as np
from plantcv.annotate import napari_label_classes
from plantcv.plantcv import readimage


def test_napari_label_classes_gray(make_napari_viewer, qtbot, test_data):
    """Test for PlantCV.Annotate"""
    # Read in test data
    img, _, _ = readimage(test_data.kmeans_seed_gray_img)
    viewer = make_napari_viewer()
    viewer = napari_label_classes(img, viewer, ['seed'])
    coor = [(25, 25)]
    viewer.add_points(np.array(coor), symbol="o", name='background',
                      face_color="red", size=1)

    def check_open():
        assert np.shape(viewer.layers['background'].data) != (0, 2)

    qtbot.waitUntil(check_open, timeout=60_000)

    assert len(viewer.layers['background'].data) == 1
