import numpy as np
from plantcv.annotate.napari_classes import napari_classes


def test_napari_classes(make_napari_viewer):
    """PlantCV Test"""
    img = np.zeros((100, 100, 3), dtype=np.uint8)
    viewer = make_napari_viewer(show=False)
    viewer.add_image(img)
    coor = [(25, 25), (50, 50)]
    viewer.add_image(img)
    viewer.add_points(np.array(coor), symbol="o", name="total",
                      face_color="red", size=30)
    viewer.add_points(np.array(coor), symbol="o", name="test",
                      face_color="red", size=30)
    keys = napari_classes(viewer)

    #assert keys == ['total', 'test']
