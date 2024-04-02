# Use Napari to Label

import numpy as np
import os
from plantcv.plantcv.plot_image import plot_image
from plantcv.plantcv.warn import warn
from plantcv.annotate import napari_classes
from plantcv.plantcv import params
from plantcv.plantcv._debug import _debug


def napari_join_labels(img, viewer):
    """
    Join classes with the same label

    Inputs:
    img  = img  (grayimg, rgbimg, or hyperspectral image array data
        e.g. hyperspectraldata.array_data). Adding labels works best on an
        image that has objects segmented/classified with contours/clusters
        labeled with values (e.g. labeled mask, output of kmeans clustering).
    viewer = Napari Viewer with classes labeled (e.g viewer from
        napari_label_classes)
    show = if show is True the viewer is launched. This opetion is useful for
    running tests without triggering the viewer.

    Returns:
    labeled_img  = labeled image
    mask_dict   = dictionary of masks; mask for each class

    :param img: numpy.ndarray
    :param viewer: Napari Viewer object
    :return labeled_imd: numpy.ndarray
    :return mask_dict: dict of numpy.ndarray

    """
    classes = napari_classes(viewer)
    lastclassvalue = len(classes)

    allmask = np.zeros((np.shape(img)))
    maskdict = {}
    valuesused = []
    classvalue = []

    for i, classname in enumerate(classes):
        data = viewer.layers[str(classname)].data

        if len(data) == 0:
            classfinal = np.zeros((np.shape(img)))
            classfinal = np.where(allmask == 0, classfinal == classfinal,
                                  classfinal == 255)
            totalmask = (classfinal.astype(int))*(i+1)
            dictmask = classfinal.astype(int)
            key = str(classname)
            keylayer = key+"_layer"
            maskdict.update({key: dictmask})
            allmask = np.add(allmask, totalmask)
            viewer.add_labels(dictmask, blending='additive', name=keylayer)
        else:
            classmask = np.zeros((np.shape(img)))
            classmask1 = np.zeros((np.shape(img)))
            classfinal = np.zeros((np.shape(img)))
            for point in data:
                x = int(point[0])
                y = int(point[1])
                value = img[x, y]
                if value in valuesused:
                    index = np.where(valuesused == value)[0]
                    if classvalue[index] != classname:
                        warning = "A cluster in "+str(classname)
                        +" has been previously labeled as "
                        +str(classvalue[index])+".Check point at position "
                        +str(x)+","+str(y)
                        warn(warning)
                valuesused = np.append(valuesused, value)
                classvalue = np.append(classvalue, classname)
                classmask[img == value] = 1
                classmask1 = np.add(classmask, classmask1)
            classfinal = np.where(classmask1 != 0, classfinal == 0,
                                  classfinal == 255)
            totalmask = (classfinal.astype(int))*(i+1)
            dictmask = classfinal.astype(int)
            key = str(classname)
            keylayer = key+"_layer"
            maskdict.update({key: dictmask})
            allmask[totalmask == (i+1)] = i+1
            viewer.add_labels(dictmask, blending='additive', name=keylayer)

    # set any zero values to last class value
    allmask[allmask == 0] = lastclassvalue

    _debug(visual=allmask, filename=os.path.join(params.debug_outdir,
                                                 str(params.device)
                                                 + '_labeled_mask.png'))

    return allmask, maskdict
