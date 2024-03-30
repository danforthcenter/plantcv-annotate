import numpy as np
#from plantcv.annotate import napari_open


def test_napari_open(make_napari_viewer):
    """PlantCV Test"""
    img = np.zeros((100, 100, 3), dtype=np.uint8)
    # viewer = napari_open(img, show=False)
    viewer = make_napari_viewer(show=False)
    viewer.add_image(img)
    #viewer = napari_open(img, viewer)
    # coor = [(25, 25), (75, 75)]
    # viewer.add_points(np.array(coor), symbol="o", name="total", face_color="red", size=1)

    # assert len(viewer.layers["total"].data) == 2
