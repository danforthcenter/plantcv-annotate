## Label Image with Napari

This function opens an image in Napari and then defines a set of classes to label. A random shape label is assigned to each class. 
Image can be annotated as long as viewer is open. 

**plantcv.annotate.napari_label_classes*(*img, classes, show=True*)

**returns** napari viewer object

- **Parameters:**
    - img - image data (compatible with gray, RGB, and hyperspectral data. If data is hyperspecral it should be the array e.g. hyperspectral.array_data)
    - classes - list of classes to label. If no points are selected for a class,
        data without labels will default to this class when napari_join_labels
        is run. If all classes have points labeled, any clusters not labeled
        will default to the last class in the list if napari_join_labels is
        run.
    - show - if show = True, viewer is launched. False setting is useful for test purposes.

- **Context:**
    - Adding class labels to images. Works best on an image that has objects segmented/classified with contours/clusters labeled with values (e.g. labeled mask, output of kmeans clustering).

- **Example use:**
    - Labeling output of kmeans clustering into classes. Labeling points.


```python
import plantcv.plantcv as pcv 
import plantcv.annotate as pcvan
import napari

# Create an instance of the Points class
img, path, name = pcv.readimage("./grayimg.png")

viewer = pcvan.napari_label_classes(img=img, classes=['background', 'wing','seed'])

# Should open interactive napari viewer

```

![Screenshot](img/documentation_images/napari_label_classes/napari_label_classes.png)


**Source Code:** [Here](https://github.com/danforthcenter/plantcv-annotate/blob/main/plantcv/annotate/napari_label_classes.py)
