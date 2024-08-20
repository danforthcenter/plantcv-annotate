# Define Classes

import napari


class Viewer(napari.Viewer):
    def layer_size(self, layer):
        """
        method to get current size of points
        """
        return self.layers[layer]._current_size
