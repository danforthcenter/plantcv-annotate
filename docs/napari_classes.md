## Open Image with Napari

Get class names from Napari Viewer Object.

**plantcv.annotate.napari_classes**(*viewer*)

**returns** list of napari classes

- **Parameters:**
    - viewer - Napari viewer object

- **Context:**
    - Get names of Napari classes. This is mainly an internal function but can be useful in other context.

- **Example use:**
    - Get names of Napari classes/labels. 


```python
import plantcv.plantcv as pcv 
import plantcv.annotate as pcvan

# Create an instance of the Points class
img, path, name = pcv.readimage("./grayimg.png")

viewer = pcvan.napari_label_classes(img=img, classes=['background', 'wing', 'seed'])
classes = pcvan.napari_classes(viewer)

```

**Source Code:** [Here](https://github.com/danforthcenter/plantcv-annotate/blob/main/plantcv/annotate/napari_classes.py)
