# Use Napari to Label

import numpy as np
import random
from plantcv.annotate import napari_open
from plantcv.annotate import napari_classes


def napari_label_classes(img, classes=False, size=10, shape='square',
                         importdata=False, show=True):
    """
    open img in napari and label classes

    Inputs:
    img  = img  (grayimg, rgbimg, or hyperspectral image array data
        e.g. hyperspectraldata.array_data). Adding labels works best on an
        image that has objects segmented/classified with contours/clusters
        labeled with values (e.g. labeled mask, output of kmeans clustering).
    classes = list of labels or classes. If no points are selected for a class,
        data without labels will default to this class when napari_join_labels
        is run. If all classes have points labeled, any clusters not labeled
        will default to the last class in the list when napari_join_labels is
        run.
    size = size of marker in pixels
    shape = either 'square' or 'circle'
    importdata = dictionary of values in Napari format (y,x).
        Output of napari_read_coor
    show = if show is True the viewer is launched. This opetion is useful for
    running tests without triggering the viewer.

    Returns:
    viewer  = Napari viewer object

    :param img: numpy.ndarray
    :param classes: list
    :param size: int
    :param shape: str
    :param importdata: dict
    :param show: str
    :return viewer: napari viewer object

    """
    showcall = show
    viewer = napari_open(img, show=showcall)

    color = ["aliceblue", "antiquewhite", "aqua", "aquamarine", "azure",
             "beige", "bisque", "black", "blanchedalmond", "blue",
             "blueviolet", "brown", "burlywood", "cadetblue",
             "chartreuse", "chocolate", "coral", "cornflowerblue",
             "cornsilk", "crimson", "cyan", "darkblue", "darkcyan",
             "darkgoldenrod", "darkgray", "darkgreen", "darkkhaki",
             "darkmagenta", "darkolivegreen", "darkorange", "darkorchid",
             "darkred", "darksalmon", "darkseagreen", "darkslateblue",
             "darkslategray", "darkturquoise", "darkviolet", "deeppink",
             "deepskyblue", "dimgray", "dodgerblue", "firebrick",
             "floralwhite", "forestgreen", "fuchsia", "gainsboro",
             "ghostwhite", "gold", "goldenrod", "gray", "green",
             "greenyellow", "honeydew", "hotpink", "indianred",
             "indigo", "ivory", "khaki", "lavender", "lavenderblush",
             "lawngreen", "lemonchiffon", "lightblue", "lightcoral",
             "lightcyan", "lightgoldenrodyellow", "lightgray", "lightgreen",
             "lightpink", "lightsalmon", "lightseagreen", "lightskyblue",
             "lightslategray", "lightsteelblue", "lightyellow", "lime",
             "limegreen", "linen", "magenta", "maroon", "mediumaquamarine",
             "mediumblue", "mediumorchid", "mediumpurple", "mediumseagreen",
             "mediumslateblue", "mediumspringgreen", "mediumturquoise",
             "mediumvioletred", "midnightblue", "mintcream", "mistyrose",
             "moccasin", "navajowhite", "navy", "oldlace", "olive",
             "olivedrab", "orange", "orangered", "orchid", "palegoldenrod",
             "palegreen", "paleturquoise", "palevioletred", "papayawhip",
             "peachpuff", "peru", "pink", "plum", "powderblue", "purple",
             "red", "rosybrown", "royalblue", "saddlebrown",
             "salmon", "sandybrown", "seagreen", "seashell", "sienna",
             "silver", "skyblue", "slateblue", "slategray", "snow",
             "springgreen", "steelblue", "tan", "teal", "thistle", "tomato",
             "turquoise", "violet", "wheat", "white", "whitesmoke",
             "yellow", "yellowgreen"]

    keys = napari_classes(viewer)

    if classes is not False:
        for x in classes:
            if x not in keys:
                viewer.add_points(np.array([]), name=x, symbol=shape,
                                  edge_color=random.choice(color),
                                  face_color=random.choice(color), size=size)
        keys = napari_classes(viewer)

    if importdata is not False:
        importkeys = list(importdata.keys())
        for key in importkeys:
            if len(importdata[key]) != 0:
                if key in keys:
                    viewer.layers[key].add(importdata[key])
                else:
                    viewer.add_points(importdata[key], name=key, symbol=shape,
                                      edge_color=random.choice(color),
                                      face_color=random.choice(color),
                                      size=size)

    return viewer
