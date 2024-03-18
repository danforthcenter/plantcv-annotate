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
        filename_rgb = "setaria_small_plant_rgb.png"
        self.small_rgb_img = os.path.join(self.datadir, filename_rgb)
        # Kmeans Clustered Gray image
        filename_kmeans = "silphium_seed_labeled_example.png"
        self.kmeans_seed_gray_img = os.path.join(self.datadir, filename_kmeans)
        # Small Hyperspectral image
        filename_hyper = "corn-kernel-hyperspectral.raw"
        self.envi_sample_data = os.path.join(self.datadir, filename_hyper)


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
