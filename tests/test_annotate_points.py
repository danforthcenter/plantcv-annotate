"""Tests for annotate.Points."""
import os
import cv2
import matplotlib
import numpy as np
from plantcv.annotate.classes import Points


def test_points(test_data):
    """Test for plantcv-annotate."""
    # Read in a test grayscale image
    img = cv2.imread(test_data.small_rgb_img)

    # initialize interactive tool
    drawer_rgb = Points(img, figsize=(12, 6))

    # simulate mouse clicks
    # event 1, left click to add point
    e1 = matplotlib.backend_bases.MouseEvent(name="button_press_event", canvas=drawer_rgb.fig.canvas,
                                             x=0, y=0, button=1)
    point1 = (200, 200)
    e1.xdata, e1.ydata = point1
    drawer_rgb.onclick(e1)

    # event 2, left click to add point
    e2 = matplotlib.backend_bases.MouseEvent(name="button_press_event", canvas=drawer_rgb.fig.canvas,
                                             x=0, y=0, button=1)
    e2.xdata, e2.ydata = (300, 200)
    drawer_rgb.onclick(e2)

    # event 3, left click to add point
    e3 = matplotlib.backend_bases.MouseEvent(name="button_press_event", canvas=drawer_rgb.fig.canvas,
                                             x=0, y=0, button=1)
    e3.xdata, e3.ydata = (50, 50)
    drawer_rgb.onclick(e3)

    # event 4, right click to remove point with exact coordinates
    e4 = matplotlib.backend_bases.MouseEvent(name="button_press_event", canvas=drawer_rgb.fig.canvas,
                                             x=0, y=0, button=3)
    e4.xdata, e4.ydata = (50, 50)
    drawer_rgb.onclick(e4)

    # event 5, right click to remove point with coordinates close but not equal
    e5 = matplotlib.backend_bases.MouseEvent(name="button_press_event", canvas=drawer_rgb.fig.canvas,
                                             x=0, y=0, button=3)
    e5.xdata, e5.ydata = (301, 200)
    drawer_rgb.onclick(e5)

    assert drawer_rgb.coords["default"][0] == point1


def test_points_print_coords(test_data, tmpdir):
    """Test for plantcv-annotate."""
    cache_dir = tmpdir.mkdir("cache")
    filename = os.path.join(cache_dir, 'plantcv_print_coords.txt')
    # Read in a test image
    img = cv2.imread(test_data.small_rgb_img)

    # initialize interactive tool
    drawer_rgb = Points(img, figsize=(12, 6))

    # simulate mouse clicks
    # event 1, left click to add point
    e1 = matplotlib.backend_bases.MouseEvent(name="button_press_event", canvas=drawer_rgb.fig.canvas,
                                             x=0, y=0, button=1)
    point1 = (200, 200)
    e1.xdata, e1.ydata = point1
    drawer_rgb.onclick(e1)

    # event 2, left click to add point
    e2 = matplotlib.backend_bases.MouseEvent(name="button_press_event", canvas=drawer_rgb.fig.canvas,
                                             x=0, y=0, button=1)
    e2.xdata, e2.ydata = (300, 200)
    drawer_rgb.onclick(e2)

    # Save collected coords out
    drawer_rgb.print_coords(filename)
    assert os.path.exists(filename)


def test_points_import_list(test_data):
    """Test for plantcv-annotate."""
    # Read in a test image
    img = cv2.imread(test_data.small_rgb_img)
    # initialize interactive tool
    drawer_rgb = Points(img, figsize=(12, 6), label="default")
    totalpoints1 = [(158, 531), (361, 112), (500, 418), (269.25303806488864, 385.69839981447126),
                    (231.21964288863632, 445.995245825603), (293.37177646934134, 448.778177179963),
                    (240.49608073650273, 277.1640769944342), (279.4571196975417, 240.05832560296852),
                    (77.23077461405376, 165.84682282003712), (420, 364), (509.5127783246289, 353.2308673469388),
                    (527.1380102355752, 275.3087894248609), (445.50535717435065, 138.94515306122452)]
    drawer_rgb.import_list(coords=totalpoints1, label="imported")

    assert len(drawer_rgb.coords["imported"]) == 13


def test_points_import_list_warn(test_data):
    """Test for plantcv-annotate."""
    # Read in a test image
    img = cv2.imread(test_data.small_rgb_img)
    # initialize interactive tool
    drawer_rgb = Points(img, figsize=(12, 6), label="default")
    totalpoints1 = [(158, 531), (361, 112), (500, 418), (445.50535717435065, 138.94515306122452)]
    drawer_rgb.import_list(coords=totalpoints1)

    assert len(drawer_rgb.coords["default"]) == 0


def test_points_import_file(test_data):
    """Test for plantcv-annotate."""
    img = cv2.imread(test_data.small_rgb_img)
    counter = Points(img, figsize=(8, 6))
    file = test_data.pollen_coords
    counter.import_file(file)

    assert counter.count['total'] == 70


def test_points_view(test_data):
    """Test for plantcv-annotate."""
    # Read in a test grayscale image
    img = cv2.imread(test_data.small_rgb_img)

    # initialize interactive tool
    drawer_rgb = Points(img, figsize=(12, 6))

    # simulate mouse clicks
    # event 1, left click to add point
    e1 = matplotlib.backend_bases.MouseEvent(name="button_press_event", canvas=drawer_rgb.fig.canvas,
                                             x=0, y=0, button=1)
    point1 = (200, 200)
    e1.xdata, e1.ydata = point1
    drawer_rgb.onclick(e1)
    drawer_rgb.view(label="new", view_all=True)
    e2 = matplotlib.backend_bases.MouseEvent(name="button_press_event", canvas=drawer_rgb.fig.canvas,
                                             x=0, y=0, button=1)
    e2.xdata, e2.ydata = (300, 200)
    drawer_rgb.onclick(e2)
    drawer_rgb.view(view_all=False)

    assert str(drawer_rgb.fig) == "Figure(1200x600)"


def test_points_view_warn(test_data):
    """Test for plantcv-annotate."""
    # Read in a test grayscale image
    img = cv2.imread(test_data.small_rgb_img)

    # initialize interactive tool, implied default label and "r" color
    drawer_rgb = Points(img, figsize=(12, 6))

    # simulate mouse clicks, event 1=left click to add point
    e1 = matplotlib.backend_bases.MouseEvent(name="button_press_event", canvas=drawer_rgb.fig.canvas,
                                             x=0, y=0, button=1)
    point1 = (200, 200)
    e1.xdata, e1.ydata = point1
    drawer_rgb.onclick(e1)
    drawer_rgb.view(label="new", color='r')

    assert str(drawer_rgb.fig) == "Figure(1200x600)"


def test_plantcv_annotate_points_correct(test_data):
    """Test for PlantCV."""
    # Create a test tmp directory
    # generate fake testing image
    allmask = cv2.imread(test_data.pollen_all, -1)
    discs = cv2.imread(test_data.pollen_discs, -1)
    coor = [(158, 531), (265, 427), (361, 112), (500, 418)]
    totalpoints1 = [(158, 531), (361, 112), (500, 418), (269.25303806488864, 385.69839981447126),
    (231.21964288863632, 445.995245825603), (293.37177646934134, 448.778177179963), (240.49608073650273, 277.1640769944342),
    (279.4571196975417, 240.05832560296852), (77.23077461405376, 165.84682282003712), (423.24190633947126, 364.3625927643785),
    (509.5127783246289, 353.2308673469388), (527, 275), (445.50535717435065, 138.94515306122452)]
    counter = Points(np.copy(allmask), figsize=(8, 6))
    counter.import_list(totalpoints1, label="total")

    corrected_mask = counter.correct(bin_img=discs, bin_img_recover=allmask, coords=coor)
    assert np.count_nonzero(discs) < np.count_nonzero(corrected_mask)
    assert np.count_nonzero(corrected_mask) < np.count_nonzero(allmask)