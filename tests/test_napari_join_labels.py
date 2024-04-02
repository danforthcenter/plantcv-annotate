import numpy as np
from plantcv.annotate.napari_open import napari_open
from plantcv.annotate.napari_label_classes import napari_label_classes
from plantcv.plantcv import readimage
from plantcv.annotate.napari_join_labels import napari_join_labels


def test_napari_join_labels(test_data):
    """Test for PlantCV.Annotate"""
    # Read in test data
    img, _, _ = readimage(test_data.kmeans_seed_gray_img)
    viewer = napari_label_classes(img, ["seed"], show=False)
    labeled, _ = napari_join_labels(img, viewer)

    assert np.shape(labeled) == (576, 537)


def test_napari_join_allclass(test_data):
    """Test for PlantCV.Annotate"""
    # Read in test data
    img, _, _ = readimage(test_data.kmeans_seed_gray_img)
    viewer = napari_open(img, show=False)
    background = [(54, 143), (77, 246)]
    viewer.add_points(np.array(background), symbol="o", name='background',
                      face_color="red", size=1)
    wing = [(275, 54)]
    viewer.add_points(np.array(wing), symbol="o", name='wing',
                      face_color="red", size=1)
    seed = [(280, 218)]
    viewer.add_points(np.array(seed), symbol="o", name='seed',
                      face_color="red", size=1)

    labeled, _ = napari_join_labels(img, viewer)

    assert np.shape(labeled) == (576, 537)


def test_napari_join_warn(test_data):
    """Test for PlantCV.Annotate"""
    # Read in test data
    img, _, _ = readimage(test_data.kmeans_seed_gray_img)
    viewer = napari_open(img, show=False)
    background = [(54, 143), (77, 246)]
    viewer.add_points(np.array(background), symbol="o", name='background',
                      face_color="red", size=1)
    wing = [(275, 54)]
    viewer.add_points(np.array(wing), symbol="o", name='wing',
                      face_color="red", size=1)
    seed = [(275, 54)]
    viewer.add_points(np.array(seed), symbol="o", name='seed',
                      face_color="red", size=1)

    labeled, _ = napari_join_labels(img, viewer)

    assert np.shape(labeled) == (576, 537)
