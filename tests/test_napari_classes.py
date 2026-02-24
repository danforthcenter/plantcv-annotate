import numpy as np
from plantcv.annotate import napari_classes, napari_open


def test_napari_classes():
    """Test for PlantCV.Annotate"""
    # Read in test data
    img = np.zeros((100, 100))
    coor = [(25, 25), (50, 50)]
    viewer = napari_open(img, show=False)
    viewer.add_points(np.array(coor), symbol="square", name="total",
                      face_color="red", size=30)
    viewer.add_points(np.array(coor), symbol="square", name="test",
                      face_color="red", size=30)
    keys = napari_classes(viewer)

    assert keys == ['total', 'test']
    viewer.close()
