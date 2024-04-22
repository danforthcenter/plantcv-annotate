import cv2
from plantcv.annotate.get_centroids import get_centroids


def test_get_centroids(test_data):
    """Test for PlantCV."""
    # Read in test data
    mask = cv2.imread(test_data.small_bin_img, -1)

    coor = get_centroids(bin_img=mask)

    assert coor == [(166, 214)]
