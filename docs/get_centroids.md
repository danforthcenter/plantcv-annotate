## Get Centroids 

Extract the centroid coordinate (column,row) from regions in a binary image. 

**plantcv.annotate.get_centroids**(*bin_img*)

**returns** list containing coordinates of centroids 

- **Parameters:**
    - bin_img - Binary image containing the connected regions to consider
- **Context:**
    - Given an arbitrary mask of the objects of interest, `get_centroids`
    returns a list of coordinates that can the be imported into the annotation class [Points](Points.md).

- **Example use:**
    - Below

**Binary image**

![count_img](img/documentation_images/get_centroids/discs_mask.png)

```python

from plantcv import plantcv as pcv

# Set global debug behavior to None (default), "print" (to file),
# or "plot"
pcv.params.debug = "plot"

# Apply get centroids to the binary image
coords = pcv.annotate.get_centroids(bin_img=binary_img)
print(coords)
# [[1902, 600], [1839, 1363], [1837, 383], [1669, 1977], [1631, 1889], [1590, 1372], [1550, 1525],
# [1538, 1633], [1522, 1131], [1494, 2396], [1482, 1917], [1446, 1808], [1425, 726], [1418, 2392],
# [1389, 198], [1358, 1712], [1288, 522], [1289, 406], [1279, 368], [1262, 1376], [1244, 1795],
# [1224, 1327], [1201, 624], [1181, 725], [1062, 85], [999, 840], [885, 399], [740, 324], [728, 224],
# [697, 860], [660, 650], [638, 2390], [622, 1565], [577, 497], [572, 2179], [550, 2230], [547, 1826],
# [537, 892], [538, 481], [524, 2144], [521, 2336], [497, 201], [385, 1141], [342, 683], [342, 102],
# [332, 1700], [295, 646], [271, 60], [269, 1626], [210, 1694], [189, 878], [178, 1570], [171, 2307],
# [61, 286], [28, 2342]]

```

**Source Code:** [Here](https://github.com/danforthcenter/plantcv-annotate/blob/main/plantcv/annotate/get_centroids.py)
