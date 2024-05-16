import numpy as np
from plantcv.annotate import napari_label_classes
from plantcv.plantcv import readimage


def test_napari_label_classes_gray(test_data):
    """Test for PlantCV.Annotate"""
    # Read in test data
    img, _, _ = readimage(test_data.kmeans_seed_gray_img)
    viewer = napari_label_classes(img, ['seed'], show=False)
    coor = [(25, 25)]
    viewer.add_points(np.array(coor), symbol="o", name='background',
                      face_color="red", size=1)

    assert len(viewer.layers['background'].data) == 1
    viewer.close()
