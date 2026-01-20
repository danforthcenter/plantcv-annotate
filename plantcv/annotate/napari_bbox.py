# Create a bounding box for ROI or SAM using a napari viewer object


def napari_bbox(viewer, layername):
    """
    Converts napari rectangles into bounding boxes for ROIs and SAM models

    Inputs:
    viewer  = napari viewer object
    layername = the name of the shapes layer

    Returns:
    boxes = list of the bounding box parameters

    :param viewer: napari.viewer.Viewer
    :param layername: str
    :return boxes: list
    """
    boxes = []
    for i in viewer.layers[layername].data:
        xs = []
        ys = []
        for j in i:
            xs.append(int(j[1]))
            ys.append(int(j[0]))
        boxes.append([min(xs), min(ys), max(ys) - min(ys), max(xs) - min(xs)])
    if len(boxes) == 1:
        return boxes[0]
    return boxes
