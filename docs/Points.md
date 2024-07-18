## Interactive Point Annotation Tool

Using [Jupyter Notebooks](https://plantcv.readthedocs.io/en/stable/jupyter/) it is possible to interactively click to collect coordinates from an image, which can be used in various downstream applications. Left click on the image to collect a point. Right click removes the
closest collected point.

**plantcv.annotate.Points**(*img, figsize=(12,6), label="dafault"*)

**returns** interactive image class

- **Parameters:**
    - img - Image data
    - figsize - Interactive plot figure size (default = (12,6))
    - label - The current label (default = "default")

- **Attributes:**
    - coords - dictionary of all coordinates per group label
    - events - includes right and left click events
    - count - dictionary that save the counts of different groups (labels)
    - label - the current label
    - sample_labels - list of all sample labels, one to one with coordinates collected 
    - view_all - flag indicating whether or not to view all labels 
    - color - current color 
    - colors - all used colors 
    - figsize - size of the interactive plotting figure 

- **Context:**
    - Used to define a list of coordinates of interest.
    - Can be helpful to ground truth counting algorithms, and exported coordinates could be used in other image analysis workflows.
- **Example use:**
    - (pcv.roi.multi)
    - Shown below (pcv.roi.custom)


```python
import plantcv.plantcv as pcv 
import plantcv.annotate as an

# Create an instance of the Points class
marker = an.Points(img=img, figsize=(12,6))

# Click on the plotted image to collect coordinates

# Use the identified coordinates to create a custom polygon ROI
roi = pcv.roi.custom(img=img, vertices=marker.coords['default'])

```

## Methods
### Correct a Mask using Point Annotations

Using [Jupyter Notebooks](https://plantcv.readthedocs.io/en/stable/jupyter/) it is possible to interactively click to collect coordinates from an image, then use these coordinate to remove and recover objects from a binary mask.

**plantcv.annotate.Points.correct_mask**(*bin_img*)

**returns** corrected_mask

- **Parameters:**
    - bin_img - binary image, filtered mask image with selected objects
    
- **Context:**
    - Filters objects from the `bin_mask` if they do not overlap with an annotation in the `Points` class instance. Also adds a labeled pixel to the corrected mask if an object cannot be resolved for any annotations.

- **Example use:**
    - Remove noise from a microscopy image that is otherwise difficult to filter out with traditional computer vision
    techniques, and recover stomata that were filtered out during mask cleaning. 

**Original Image with Annotations**

![Screenshot](img/documentation_images/points_correct_mask/annotated_stomata.png)

**bin_img**

![Screenshot](img/documentation_images/points_correct_mask/bin_img.png)

```python
import plantcv.plantcv as pcv 
import plantcv.annotate as pcvan

# Create an instance of the Points class
img, path, name = pcv.readimage("stomata.tif")

# Segmentation & mask clean up steps here 

# Create an instance of the Points class & click on stomata
marker = pcvan.Points(img=img, figsize=(12,6))

corrected_mask = marker.correct_mask(bin_img=mask_clean, bin_img_recover=bin_img_recover)

debug_vis = pcv.visualize.overlay_two_imgs(img, corrected_mask, alpha=.4)
```

**Corrected Mask**

![Screenshot](img/documentation_images/points_correct_mask/corrected_mask.png)

**Overlaid Image**

![Screenshot](img/documentation_images/points_correct_mask/overlay.png)

**Source Code:** [Here](https://github.com/danforthcenter/plantcv-annotate/blob/main/plantcv/annoate/classes.py)
