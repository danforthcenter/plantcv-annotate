from plantcv.annotate import napari_read_coor


def test_napari_read_coor_napari(test_data):
    """Test for PlantCV.Annotate"""
    # Read in test data
    data = napari_read_coor(test_data.coor_data, 'yx')

    assert isinstance(data, dict)


def test_napari_read_coor_other(test_data):
    """Test for PlantCV.Annotate"""
    # Read in test data
    data = napari_read_coor(test_data.coor_data, 'xy')

    assert data['germinated'][0] == (10, 25)


def test_napari_read_coor_flip():
    """Test for PlantCV.Annotate"""
    # Read in test data
    coor = {"germinated": [[25, 10]]}
    data = napari_read_coor(coor, 'xy')

    assert data['germinated'][0] == (10, 25)
