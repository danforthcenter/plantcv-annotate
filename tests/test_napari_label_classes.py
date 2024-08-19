import numpy as np
from plantcv.annotate import napari_label_classes
from plantcv.plantcv import readimage


def test_napari_label_classes_gray(test_data):
    """Test for PlantCV.Annotate"""
    # Read in test data
    img, _, _ = readimage(test_data.kmeans_seed_gray_img)
    data = {'total': [(25, 25)], 'background': [(50, 50)]}
    viewer = napari_label_classes(img, ['total'], size=5, importdata=data,
                                  show=False)
    coor = [(50, 25)]
    viewer.add_points(np.array(coor), symbol="square", name='coor',
                      face_color="red", size=5)

    assert len(viewer.layers['total'].data) == 1
    viewer.close()
