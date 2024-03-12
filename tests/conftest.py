import pytest
import matplotlib
import napari
from typing import Callable
import os


# Disable plotting
matplotlib.use("Template")


class TestData:
    def __init__(self):
        """Initialize simple variables."""
        # Test data directory
        self.datadir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    "testdata")
        # RGB image
        self.small_rgb_img = os.path.join(self.datadir,
                                          "setaria_small_plant_rgb.png")
        # Kmeans Clustered Gray image
        self.kmeans_seed_gray_img = os.path.join(self.datadir,
                                        "silphium_seed_labeled_example.png")
        # Small Hyperspectral image
        self.kmeans_seed_gray_img = os.path.join(self.datadir,
                                        "silphium_seed_labeled_example.png")
        # ENVI hyperspectral data
        self.envi_sample_data = os.path.join(self.datadir,
                                             "corn-kernel-hyperspectral.raw")


@pytest.fixture
def viewer_widget(make_napari_viewer: Callable[..., napari.Viewer]):
    """Test for PlantCV.Annotate"""
    # Read in test data
    viewer = make_napari_viewer()

    return viewer


@pytest.fixture(scope="session")
def test_data():
    """Test data object for the main PlantCV package."""
    return TestData()
