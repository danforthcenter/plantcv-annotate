import numpy as np
from plantcv.annotate import napari_classes


def test_napari_classes(make_napari_viewer, qtbot):
    """Test for PlantCV.Annotate"""
    # Read in test data
    viewer = make_napari_viewer()
    img = np.zeros((100, 100))
    coor = [(25, 25), (50, 50)]
    viewer.add_image(img)
    viewer.add_points(np.array(coor), symbol="o", name="total",
                      face_color="red", size=30)
    viewer.add_points(np.array(coor), symbol="o", name="test",
                      face_color="red", size=30)
    keys = napari_classes(viewer)

    def check_keys():
        assert keys != []

    qtbot.waitUntil(check_keys, timeout=60_000)

    assert keys == ['total', 'test']
