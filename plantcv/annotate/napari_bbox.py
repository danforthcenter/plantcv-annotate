# Create a bounding box for ROI or SAM using a napari viewer object


def napari_bbox(viewer, layername):
    """Convert napari rectangles into bounding boxes for ROIs and SAM models.

    Parameters
    ----------
    viewer : napari.viewer.Viewer
        Napari viewer object.
    layername : str
        Name of the shapes layer.

    Returns
    -------
    list
        Bounding box parameters as [x_min, y_min, height, width], or a list
        of such lists if multiple shapes are present.
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
