import os
import pytest
import matplotlib


# Disable plotting
matplotlib.use("Template")


class TestData:
    def __init__(self):
        """Initialize simple variables."""
        # Test data directory
        self.datadir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "testdata")
        # Flat image directory
        self.snapshot_dir = os.path.join(self.datadir, "snapshot_dir")
        # RGB image
        self.small_rgb_img = os.path.join(self.datadir, "setaria_small_plant_rgb.png")
        # Binary image
        self.small_bin_img = os.path.join(self.datadir, "setaria_small_plant_mask.png")
        # Text file with tuple coordinates (by group label)
        self.pollen_coords = os.path.join(self.datadir, "points_file_import.coords")
        # Kmeans Clustered Gray image
        self.kmeans_seed_gray_img = os.path.join(self.datadir, "silphium_seed_labeled_example.png")
        # Small Hyperspectral image
        self.envi_sample_data = os.path.join(self.datadir, "corn-kernel-hyperspectral.raw")
        # Binary mask including all pollen grainss 
        self.pollen_all = os.path.join(self.datadir, "pollen_all_mask.png")
        # Binary mask Eccentricity filtered objects
        self.pollen_discs = os.path.join(self.datadir, "pollen_detectdisc_mask.png")

@pytest.fixture(scope="session")
def test_data():
    """Test data object for the main PlantCV package."""
    return TestData()
