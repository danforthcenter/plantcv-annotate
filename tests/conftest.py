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
        self.pollen_all = os.path.join(self.datadir, "pollen_all_mask.png")
        self.pollen_discs = os.path.join(self.datadir, "pollen_detectdisc_mask.png")
        self.pollen_watershed = os.path.join(self.datadir, "pollen_watershed.png")

@pytest.fixture(scope="session")
def test_data():
    """Test data object for the main PlantCV package."""
    return TestData()
