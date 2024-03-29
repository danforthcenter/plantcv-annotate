import pytest
import matplotlib
import os
import napari
from typing import Callable


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


@pytest.fixture(scope="session")
def test_data():
    """Test data object for the main PlantCV package."""
    return TestData()
