# Use Napari to Label

import napari
import cv2
import numpy as np
from skimage.color import label2rgb
import random
from plantcv.plantcv.fatal_error import fatal_error


def napari_label_classes(grayimg, classes):
    """
    open img in napari and label classes
    
    Inputs:
    grayimg  = classified gray image with contours/clusters labeled with values (e.g. labeled mask, output of kmeans clustering)
    classes = list of labels or classes. If no points are selected for a class, data without labels will default to this class when napari_join_labels is run. 
    If all classes have points labeled, any clusters not labeled will default to the last class in the list when napari_join_labels is run.
    
    Returns:
    viewer  = napari viewer object
    
    :param grayimg: numpy.ndarray
    :return viewer: napari viewer object
    
    """
    shape = np.shape(grayimg)
    
    if len(shape) == 2:
        colorful = label2rgb(grayimg)
        img = ((255*colorful).astype(np.uint8))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    if len(shape) == 3:
        fatal_error("Input image is not a single channel gray image")
               
    viewer = napari.view_image(img)

    symbols = ['arrow', 'clobber', 'cross', 'diamond', 'disc', 'hbar', 'ring', 
               'square', 'star', 'tailed_arrow', 'triangle_down', 'triangle_up', 'vbar']
    
    for i,x in enumerate(classes):
        viewer.add_points(np.array([]), name = x, symbol = random.choice(symbols), face_color = 'white', size = 10)
    
    return viewer