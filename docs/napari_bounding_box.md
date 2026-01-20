## Use Napari to draw a bounding box

Use an interactive Napari viewer to draw a rectangle that is converted to the appropriate parameters for either defining an ROI or bounding box for deep learning models like Segment Anything. 

**plantcv.annotate.napari_bbox**(*viewer, layername*)

**returns** a list with x and y coordinates of the top left corner of the box, height and width. If more than one rectangle is drawn in the Napari shapes layer, the function returns a list of lists containing the parameters for each shape. 

- **Parameters:**
    - viewer - a Napari viewer object. Should have a shapes layer with one or more rectangles drawn. 
    - layername - the name of the shapes layer where the rectangles have been drawn. 

- **Context:**
    - Used to convert easily drawn rectangles to [x, y, h, w], the format for either defining an ROI for image analysis with PlantCV or a bounding box for deep learning using Segment Anything.

- **Example use below:**
 
```python
import plantcv.plantcv as pcv 
import plantcv.annotate as pcvan

# Open and image and a Napari viewer
img, _, _ = pcv.readimage("./exampleimage.png")

viewer = pcvan.napari_open(img=img)

# Add a shapes layer
viewer.add_shapes(name="shapes")

# In the interactive viewer, draw a rectangle. In the next cell, run:
boxes = napari_bbox(viewer=viewer, layername="shapes")

```

**Source Code:** [Here](https://github.com/danforthcenter/plantcv-annotate/blob/main/plantcv/annotate/napari_bbox.py)
