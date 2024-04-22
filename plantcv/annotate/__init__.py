from importlib.metadata import version
from plantcv.annotate.classes import Points

# Auto versioning
__version__ = version("plantcv-annotate")

__all__ = [
    "Points"
    ]
