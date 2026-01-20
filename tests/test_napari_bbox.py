import numpy as np
import napari
from plantcv.annotate import napari_bbox


def test_napari_bbox(test_data):
    """Test for PlantCV.Annotate"""
    # Read in test data
    viewer = napari.Viewer(show=False)
    coor = np.array([[1,1], [11,1], [11,11], [1,11]])
    viewer.add_shapes(coor, shape_type= 'rectangle', name="shapes")
    assert napari_bbox(viewer=viewer, layername="shapes") == [1, 1, 10, 10]
    viewer.close()
    
def test_napari_bbox_multiple(test_data):
    """Test for PlantCV.Annotate"""
    # Read in test data
    viewer = napari.Viewer(show=False)
    coor1 = np.array([[1,1], [11,1], [11,11], [1,11]])
    coor2 = np.array([[21,21], [41,21], [41,41], [21,41]])
    coors = [coor1, coor2]
    viewer.add_shapes(coors, shape_type= 'rectangle', name="shapes")
    assert napari_bbox(viewer=viewer, layername="shapes") == [[1, 1, 10, 10], [21, 21, 20, 20]]
    viewer.close()