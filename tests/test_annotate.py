from plantcv import annotate as an


def test_annotate():
    """PlantCV Test"""
    assert an.__name__ == "plantcv.annotate"


def test_napari(make_napari_viewer):
    """PlantCV Test"""
    viewer = make_napari_viewer(show=False)
