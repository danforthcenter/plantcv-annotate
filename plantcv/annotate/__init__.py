from importlib.metadata import version
from plantcv.annotate.classes import Points
from plantcv.annotate.get_centroids import get_centroids
from plantcv.annotate.napari_classes import napari_classes
from plantcv.annotate.napari_open import napari_open
from plantcv.annotate.napari_label_classes import napari_label_classes
from plantcv.annotate.napari_join_labels import napari_join_labels
from plantcv.annotate.napari_save_coor import napari_save_coor

# Auto versioning
__version__ = version("plantcv-annotate")

__all__ = [
    "Points",
    "get_centroids",
    "napari_classes",
    "napari_open",
    "napari_label_classes",
    "napari_join_labels",
    "napari_save_coor"
]
