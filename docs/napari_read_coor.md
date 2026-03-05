## Read point data into Napari Format

Read points from a file or dictionary into Napari format 

**plantcv.napari_read_coor**(*coor, dataformat = 'yx'*)

**returns** dictionary of points labeled by class

- **Parameters:**
    - coor - dictionary object of coordinates, or a path to json datafile with dictionary of point coordinates
    - dataformat - either 'yx', 'xy', or 'sam', Napari takes data as y,x format. If data is 'xy' data is converted from x,y to y,x.
    If data is 'sam' point data is formatted for input into ultralytics sam3 functions. If 'sam' format is selected the function does expect a dictionary with 'pos' and 'neg' points as labelled classes.

- **Context:**
    - Import previously labeled points, or points from other functions (e.g. [`pcvan.napari_save_coor`](napari_save_coor.md))

- **Example use:**
    - Below


```python
import plantcv.plantcv as pcv 
import plantcv.annotate as pcvan

# read in data

data = pcvan.napari_read_coor(coor ='coor.json', dataformat = 'xy')

```

- **Example use for training Segment Anything Model:**
    - Below

```python
from ultralytics import SAM

model = SAM("sam3.pt")
results = model.predict(source="./Example_image.jpg", 
                        points=data["points"], 
                        labels=data["labels"])
results[0].show()

```

**Source Code:** [Here](https://github.com/danforthcenter/plantcv-annotate/blob/main/plantcv/annotate/napari_read_coor.py)
