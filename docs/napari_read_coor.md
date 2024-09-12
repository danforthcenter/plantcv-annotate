## Read point data into Napari Format

Save Points Labeled in Napari to a File

**plantcv.napari_read_coor**(*coor, dataformat = 'yx'*)

**returns** dictionary of points labeled by class

- **Parameters:**
    - coor - dictionary object of coordinates, or a path to json datafile with dictionary of point coordinates
    - dataformat - either 'yx' or 'xy', Napari takes data as y,x format. If data is 'xy' data is converted from x,y to y,x

- **Context:**
    - Import previously labeled points, or points from other functions (e.g. [`pcvan.napari_read_coor`](napari_read_coor.md))

- **Example use:**
    - Below


```python
import plantcv.plantcv as pcv 
import plantcv.annotate as pcvan

# read in data

data = pcvan.napari_read_points(coor ='coor.json', dataformat = 'xy')

```

**Source Code:** [Here](https://github.com/danforthcenter/plantcv-annotate/blob/main/plantcv/annotate/napari_read_coor.py)
