# Define Classes

import napari


class Viewer(napari.Viewer):
    def layer_size(self, layer):
        return self.layers[layer]._current_size
