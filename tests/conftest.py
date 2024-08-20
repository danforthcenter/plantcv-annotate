import pytest
import matplotlib
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
        # Coordinates File
        filename_coor = "germinated.txt"
        self.coor_data = os.path.join(self.datadir, filename_coor)
        # Naive Bayes Data
        filename_nbrgb = "08_02_16-QTHJ-RIL-019_zoomed.png"
        self.nb_rgb = os.path.join(self.datadir, filename_nbrgb)
        filename_nbmask = "my_maskdict.npy"
        self.nb_mask = os.path.join(self.datadir, filename_nbmask)


@pytest.fixture(scope="session")
def test_data():
    """Test data object for the main PlantCV package."""
    return TestData()
