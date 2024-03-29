import numpy as np
import napari
from plantcv.annotate import napari_open


def test_napari(qtbot):
    """PlantCV Test"""
    img = np.zeros((100, 100, 3), dtype=np.uint8)
    # viewer = napari_open(img, show=False)
    viewer = napari.view_image(img, show=False)
    coor = [(25, 25), (75, 75)]
    viewer.add_points(np.array(coor), symbol="o", name="total", face_color="red", size=1)

    # def check_open():
    #     assert np.shape(viewer.layers['total'].data) != (0, 2)

    # qtbot.waitUntil(check_open, timeout=60_000)

    assert len(viewer.layers["total"].data) == 2
