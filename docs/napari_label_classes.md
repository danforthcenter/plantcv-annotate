## Label Image with Napari

This function opens an image in Napari and then defines a set of classes to label. A random shape label is assigned to each class. 
Image can be annotate as long as viewer is open. 

**plantcv.annotate.napari_label_classes*(*img, classes, size, shape =10, 'square', importdata=False, show=True*)

**returns** napari viewer object

- **Parameters:**
    - img - image data (compatible with gray, RGB, and hyperspectral data. If data is hyperspecral it should be the array e.g. hyperspectral.array_data)
    - classes - list of classes to label. This option is not necessary if data is data is imported.
    - size - integer pixel size of label
    - shape - can be 'o', 'arrow', 'clobber', 'cross', 'diamond', 'disc', 'hbar', 'ring', 'square', 'star', 'tailed_arrow', 
    'triangle_down', 'triangle_up', 'vbar', 'x'.
    - importdata - dictionary of data, data saved from napari_save_coor or data imported from napari_read_coor
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

viewer = pcvan.napari_label_classes(img=img, classes=['background', 'wing','seed'], size = 30)

# Should open interactive napari viewer

```

![Screenshot](img/documentation_images/napari_label_classes/napari_label_classes.png)


**Source Code:** [Here](https://github.com/danforthcenter/plantcv-annotate/blob/main/plantcv/annotate/napari_label_classes.py)
