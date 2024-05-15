## Correct a Mask using Point Annotations

Using [Jupyter Notebooks](https://plantcv.readthedocs.io/en/stable/jupyter/) it is possible to interactively click to collect coordinates from an image, then use these coordinate to remove and recover objects from a binary mask.

**plantcv.annotate.Points.correct_mask**(*bin_img, bin_img_recover*)

**returns** corrected_mask

- **Parameters:**
    - bin_img - binary image, filtered mask image with selected objects
    - bin_img_recover - binary image, unclean mask image with all potentially recoverable objects

- **Context:**
    - Adds objects back to the `bin_mask` if they overlap with an annotation in the [`Points` class instance](Points.md) and can be recovered from the unclean mask `bin_img_recover`. Also checks each object in `bin_mask` and removes
    it in the `corrected_mask` if there is not a corresponding annotation.

- **Example use:**
    - Remove noise from a microscopy image that is otherwise difficult to filter out with traditional computer vision
    techniques, and recover stomata that were filtered out during mask cleaning. 

**Original Image with Annotations**

![Screenshot](img/documentation_images/points_correct_mask/)

**bin_img**

![Screenshot](img/documentation_images/points_correct_mask/)

**bin_img_recover**

![Screenshot](img/documentation_images/points_correct_mask/)

```python
import plantcv.plantcv as pcv 
import plantcv.annotate as pcvan

# Create an instance of the Points class
img, path, name = pcv.readimage("stomata.tif")

# Segmentation & mask clean up steps here 

# Create an instance of the Points class & click on stomata
marker = pcvan.Points(img=img, figsize=(12,6))

corrected_mask = marker.correct_mask(bin_img=mask_clean, bin_img_recover=bin_img_recover)

```

**Corrected Mask**

![Screenshot](img/documentation_images/points_correct_mask/)


**Source Code:** [Here](https://github.com/danforthcenter/plantcv-annotate/blob/main/plantcv/annotate/classes.py)

