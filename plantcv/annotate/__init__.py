from importlib.metadata import version
from plantcv.annotate.classes import Points
from plantcv.annotate.get_centroids import get_centroids

# Auto versioning
__version__ = version("plantcv-annotate")

__all__ = [
    "Points",
    "get_centroids"
    ]
