# Get centroids. region props method (WILL Merge into PCV.annotate, opening PR this week) 

from skimage.measure import label, regionprops

def get_centroids(bin_img):
    """Get the coordinates (row,column) of the centroid of each connected region in a binary image.

    Inputs:
    bin_img         = Binary image containing the connected regions to consider

    Returns:
    coords          = List of coordinates (row,column) of the centroids of the regions

    :param bin_img: numpy.ndarray
    :return coords: list
    """
    # find contours in the binary image
    labeled_img = label(bin_img)
    # measure regions
    obj_measures = regionprops(labeled_img)
    
    coords = []
    for obj in obj_measures:
        # Convert coord values to int
        coord = tuple(map(int, obj.centroid))
        coords.append(coord)

    
    return coords
