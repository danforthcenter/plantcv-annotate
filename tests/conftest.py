import pytest
import matplotlib
import napari
from typing import Callable


# Disable plotting
matplotlib.use("Template")

@pytest.fixture
def viewer_widget(make_napari_viewer: Callable[..., napari.Viewer]):
    """Test for PlantCV.Annotate"""
    # Read in test data
    viewer = make_napari_viewer()

    return viewer
