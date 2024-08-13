# Class helpers

# Imports
import os
import cv2
import json
import numpy as np
from math import floor
import matplotlib.pyplot as plt
from plantcv.plantcv.annotate.points import _find_closest_pt
from plantcv.plantcv import warn, params
from plantcv.plantcv._debug import _debug
from plantcv.plantcv import create_labels, apply_mask


class Points:
    """Point annotation/collection class to use in Jupyter notebooks. It allows the user to
    interactively click to collect coordinates from an image. Left click collects the point and
    right click removes the closest collected point.
    """

    def __init__(self, img, figsize=(12, 6), label="default", color="r", view_all=False):
        """Points initialization method.

        Parameters
        ----------
        img : numpy.ndarray
            image to annotate
        figsize : tuple, optional
            figure plotting size, by default (12, 6)
        label : str, optional
            class label, by default "default"
        """
        self.img = img
        self.figsize = figsize
        self.label = label  # current label
        self.color = color  # current color
        self.view_all = view_all  # a flag indicating whether or not view all labels
        self.coords = {}  # dictionary of all coordinates per group label
        self.events = []  # includes right and left click events
        self.count = {}  # a dictionary that saves the counts of different groups (labels)
        self.sample_labels = []  # list of all sample labels, one to one with points collected
        self.colors = {}  # all used colors

        self.view(label=self.label, color=self.color, view_all=self.view_all)

    def onclick(self, event):
        """Handle mouse click events

        Parameters
        ----------
        event : matplotlib.backend_bases.MouseEvent
            matplotlib MouseEvent object
        """
        print(type(event))
        self.events.append(event)
        if event.button == 1:
            # Add point to the plot
            self.ax.plot(event.xdata, event.ydata, marker='x', c=self.color)
            self.coords[self.label].append((floor(event.xdata), floor(event.ydata)))
            self.count[self.label] += 1
            self.sample_labels.append(self.label)
        else:
            idx_remove, _ = _find_closest_pt((event.xdata, event.ydata), self.coords[self.label])
            # remove the closest point to the user right clicked one
            self.coords[self.label].pop(idx_remove)
            self.count[self.label] -= 1
            idx_remove = idx_remove + self.p_not_current
            self.ax.lines[idx_remove].remove()
            self.sample_labels.pop(idx_remove)
        self.fig.canvas.draw()

    def print_coords(self, filename):
        """Save collected coordinates to a file.

        Parameters
        ----------
        filename : str
            output filename
        """
        # Open the file for writing
        with open(filename, "w") as fp:
            # Save the data in JSON format with indentation
            json.dump(obj=self.coords, fp=fp, indent=4)

    def import_list(self, coords, label="default"):
        """Import coordinates.

        Parameters
        ----------
        coords : list
            list of coordinates (tuples)
        label : str, optional
            class label, by default "default"
        """
        if label not in self.coords:
            self.coords[label] = []
            for (y, x) in coords:
                self.coords[label].append((x, y))
            self.count[label] = len(self.coords[label])
            self.view(label=label, color=self.color, view_all=False)
        else:
            warn(f"{label} already included and counted, nothing is imported!")

    def import_file(self, filename):
        """Import coordinates from a file.

        Parameters
        ----------
        filename : str
            JSON file containing Points annotations
        """
        with open(filename, "r") as fp:
            coords = json.load(fp)

        keys = list(coords.keys())

        for key in keys:
            keycoor = coords[key]
            keycoor = list(map(lambda sub: (sub[1], sub[0]), keycoor))
            self.import_list(keycoor, label=key)

    def view(self, label="default", color="r", view_all=False):
        """View coordinates for a specific class label.

        Parameters
        ----------
        label : str, optional
            class label, by default "default"
        color : str, optional
            marker color, by default "r"
        view_all : bool, optional
            view all classes or a single class, by default False
        """
        if label not in self.coords and color in self.colors.values():
            warn("The color assigned to the new class label is already used, if proceeding, "
                 "items from different classes will not be distinguishable in plots!")
        self.label = label
        self.color = color
        self.view_all = view_all

        if self.label not in self.coords:
            self.coords[self.label] = []
            self.count[self.label] = 0
        self.colors[self.label] = self.color

        self.fig, self.ax = plt.subplots(1, 1, figsize=self.figsize)

        self.events = []
        self.fig.canvas.mpl_connect('button_press_event', self.onclick)

        self.ax.imshow(cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB))
        self.ax.set_title("Please left click on objects\n Right click to remove")
        self.p_not_current = 0
        # if view_all is True, show all already marked markers
        if self.view_all:
            for k in self.coords:
                for (x, y) in self.coords[k]:
                    self.ax.plot(x, y, marker='x', c=self.colors[k])
                    if self.label not in self.coords or len(self.coords[self.label]) == 0:
                        self.p_not_current += 1
        else:
            for (x, y) in self.coords[self.label]:
                self.ax.plot(x, y, marker='x', c=self.color)

    def _create_pts_mask(self, bin_img):
        """Fitler a binary mask based on annotations.

        Parameters
        ----------
        bin_img : numpy.ndarray
            binary image

        Returns
        ----------
        pts_mask : numpy.ndarray
            binary mask of annotations
        """
        labelnames = list(self.count)
        pts_mask = np.zeros(np.shape(bin_img), np.uint8)
        # Create points mask from all annotations
        for names in labelnames:
            for i, (x, y) in enumerate(self.coords[names]):
                x = int(x)
                y = int(y)
                # Draw pt annotations onto a blank mask
                pts_mask = cv2.circle(pts_mask, (x, y), radius=0, color=(255), thickness=-1)
        
        return pts_mask
    
    def _remove_unannotated_objects(pts_mask, bin_img):
        """Fitler a binary mask based on annotations.

        Parameters
        ----------
        pts_mask : numpy.ndarray
            binary image, mask with all annotations plotted as pixels
        bin_img : numpy.ndarray
            binary image, mask to get corrected

        Returns
        ----------
        filetered_mask : numpy.ndarray
            corrected mask
        debug_img_removed : numpy.ndarray
            binary mask of objects that were removed
        """
        debug_img_removed = cv2.cvtColor(pts_mask.copy(), cv2.COLOR_GRAY2RGB)
        
        # Create a labeled mask from the input mask
        labeled_mask, total_obj_num = create_labels(mask=bin_img)
        labeled_mask1 = np.copy(labeled_mask)
        # Objects that overlap with one or more annotations get kept
        masked_image = apply_mask(img=labeled_mask1, mask=pts_mask, mask_color='black')
        keep_object_ids = np.unique(masked_image)
        
        # Fill in objects that are not overlapping with an annotation
        for i in range(1, total_obj_num + 1):
            if i not in keep_object_ids:
                labeled_mask1[np.where(labeled_mask == i)] = 0
                debug_img_removed[np.where(labeled_mask == i)] = (50, 50, 50)
                
        # Create new binary mask after filtering un-annotated objects
        completed_mask_bin = np.where(labeled_mask1 > 0, 255, 0)
                
        return completed_mask_bin, debug_img_removed
    

    def correct_mask(self, bin_img):
        """Fitler a binary mask and make a labeled mask for analysis.

        Parameters
        ----------
        bin_img : numpy.ndarray
            binary image, mask to get corrected

        Returns
        ----------
        final_mask : numpy.ndarray
            corrected and labeled mask with recovered and removed objects
        num : int
            number of objects represented within the labeled mask
        """
        from plantcv.plantcv.visualize import colorize_label_img
        from plantcv.plantcv import dilate

        debug = params.debug
        params.debug = None

        unrecovered_ids = []
        debug_coords = []
        debug_labels = []
        added_obj_labels = []
        analysis_labels = []
        
        pts_mask = _create_pts_mask(bin_img)
        
        final_mask = np.zeros(np.shape(bin_img), np.uint32)
        debug_img = np.zeros(np.shape(bin_img), np.uint8)
        
        debug_img_duplicates = debug_img.copy()

        completed_mask_bin, debug_img_removed = _remove_unannotated_objects(pts_mask, bin_img)

        # Create a new labeled annotation mask to determine number of annotation per object
        labeled_mask_all, _ = create_labels(mask=completed_mask_bin)
        masked_image2 = apply_mask(img=labeled_mask_all, mask=pts_mask, mask_color='black')
        keep_object_ids, keep_object_count = np.unique(masked_image2, return_counts=True) 
        print("ids: " + str(keep_object_ids))
        print("counts: " + str(keep_object_count))
        # Initialize object count
        object_id_count = 1
        # pts in class used for recovering and labeling
        for names in labelnames:
            for i, (x, y) in enumerate(self.coords[names]):
                x = int(x)
                y = int(y)
                mask_pixel_value = labeled_mask_all[y, x]
                text = str(object_id_count)
                
                # Check if current annotation can be resolved to an object in the mask
                if mask_pixel_value == 0:
                    if params.verbose == True:
                        print(f"Object could not be resolved at coordinate: x = {x}, y = {y}")
                    unrecovered_ids.append(object_id_count)
                    added_obj_labels.append(object_id_count)
                    analysis_labels.append(names)
                    # Add a pixel where unresolved annotation to the mask
                    final_mask[y,x] = object_id_count
                    # Add a thicker pixel where unresolved annotation to the debug img
                    cv2.circle(debug_img, (x, y), radius=params.line_thickness, color=(object_id_count), thickness=-1)
                    # Add debug label annotations later
                    debug_coords.append((x, y))
                    debug_labels.append(text)
                if mask_pixel_value > 0:
                    # An object is resolved but check if there are other annotations associated with an object
                    associated_count = keep_object_count[mask_pixel_value]
                    if associated_count == 1:
                        # New object getting added
                        added_obj_labels.append(mask_pixel_value)
                        analysis_labels.append(names)
                        # Draw on labeled mask with correct pixel value
                        final_mask = np.where(labeled_mask_all == mask_pixel_value, object_id_count, final_mask)
                        debug_img = np.where(labeled_mask_all == mask_pixel_value, object_id_count, debug_img)
                        # Add debug label annotations later
                        debug_coords.append((x, y))
                        debug_labels.append(text)
                    if associated_count > 1:
                        # Object annotated more than once so find all associated annotations 
                        associated_coords = np.where(masked_image2 == mask_pixel_value)
                        associated_coords = tuple(zip(*associated_coords))
                        coord_labels = []
                        # Find all class labels for each annotation
                        for dup_coord in associated_coords:
                            # Flip x & y for numpy, and find the associated class label with each coordinate
                            coord_class_label = [k for k, v in self.coords.items() if (dup_coord[1], dup_coord[0]) in v]
                            coord_labels.append(coord_class_label)
                        print(coord_labels)
                        # Is there more than one class label associated with the given object?
                        re = np.unique(coord_labels)
                        if len(re) == 1:
                            # Labels are duplicated
                            # Draw the ghost of objects removed
                            debug_img_duplicates = np.where(labeled_mask_all == mask_pixel_value, (255), debug_img_duplicates)
                            if mask_pixel_value not in added_obj_labels:
                                # Fill in the duplicate object in the labeled mask, replace with pixel annotations
                                final_mask = np.where(labeled_mask_all == mask_pixel_value, (0), final_mask)
                                added_obj_labels.append(mask_pixel_value)
                                for dup_coord in associated_coords:
                                    final_mask[dup_coord[1], dup_coord[0]] = object_id_count
                                    analysis_labels.append(names)
                                    # Add a thicker pixel where unresolved annotation to the debug img
                                    cv2.circle(debug_img, (dup_coord[1], dup_coord[0]), radius=params.line_thickness, color=(object_id_count), thickness=-1)
                                    # Add debug label annotations later
                                    debug_coords.append((dup_coord[1], dup_coord[0]))
                                    debug_labels.append(str(object_id_count))
                                    # Increment object count up so each pixel drawn in labeled mask is unique
                                    object_id_count += 1
                            params.debug = debug
                            print(np.unique(final_mask))
                            _debug(visual=final_mask,
                                filename=os.path.join(params.debug_outdir,
                                f"{params.device}_annotation-corrected.png"))
                        if len(re) > 1: # and count of each label = 1 (count is all "1"s??)
                            # More than one class label associated with a given object
                            splitup = []
                            # Split on "_" in case something has already been combined
                            for lbl in re:
                                list_lbl = lbl[0].split("_")
                                splitup.append(list_lbl)
                            # Flatten list of labels
                            flat = np.concatenate(splitup)
                            # Grab each unique label from the list
                            unique_lbls, lbl_counts = np.unique(flat, return_counts=True)
                            # Is there duplication within each class label for the given object?
                            if np.all(lbl_counts == 1):
                                # If no, Concat with "_" delimiter
                                concat_lbl = "_".join(list(unique_lbls))
                                # Adding the object
                                added_obj_labels.append(object_id_count)
                                analysis_labels.append(concat_lbl)
                                final_mask = np.where(labeled_mask_all == mask_pixel_value, object_id_count, final_mask)
                                # Add debug label annotations later
                                debug_coords.append((x, y))
                                debug_labels.append(text)
                            else:
                                # Draw the ghost of objects removed
                                debug_img_duplicates = np.where(labeled_mask_all == mask_pixel_value, (255), debug_img_duplicates)
                                # Fill in the duplicate object in the labeled mask, replace with pixel annotations
                                final_mask = np.where(labeled_mask_all == mask_pixel_value, (0), final_mask)
                        # If there are duplication in labels (e.g. [['total'], ['total']] then add to list)
                        dupes = [x for n, x in enumerate(coord_labels) if x in coord_labels[:n]]
                        # original_index = added_obj_labels.index(mask_pixel_value)
                        # original_label = analysis_labels[original_index]
                        # original_coord = debug_coords[original_index]
                        # # Determine label duplicate or unique for combination
                        # coord_class_label = [k for k, v in self.coords.items() if (x, y) in v]
                        # if coord_class_label[0] in original_label:
                        #     # We found a duplicate label
                        #     # New object getting added
                        #     added_obj_labels.append(object_id_count)
                        #     analysis_labels.append(names)
                        #     # Fill in the duplicate object in the debug mask
                        #     debug_img = np.where(debug_img == original_index, (0), debug_img)
                        #     # Replace with pixel annotations in debug
                        #     cv2.circle(debug_img, (x, y), radius=params.line_thickness, color=(object_id_count), thickness=-1)
                        #     cv2.circle(debug_img, original_coord, radius=params.line_thickness, color=(original_index), thickness=-1)
                        #     # Draw the ghost of objects removed
                        #     debug_img_duplicates = np.where(labeled_mask_all == mask_pixel_value, (255), debug_img_duplicates)
                        #     # Add debug label annotations later
                        #     debug_coords.append((x, y))
                        #     debug_labels.append(text)
                        #     # Fill in the duplicate object in the labeled mask, replace with pixel annotations
                        #     final_mask = np.where(labeled_mask_all == mask_pixel_value, (0), final_mask)
                        #     final_mask[y,x] = object_id_count
                        #     final_mask[original_coord[1], original_coord[0]] = original_index + 1
                        # else:
                        #     # If unique then combine labels 
                        #     analysis_labels[added_obj_labels.index(mask_pixel_value)] = original_label + "_" + coord_class_label[0]
                        #     # De-increment object count since just a single object
                        #     object_id_count -= 1

                object_id_count += 1

        # Combine and colorize the debug image
        # Dilate duplicate objs and subtract the object itself to leave just a halo around
        debug_img_duplicates1 = dilate(debug_img_duplicates, ksize=params.line_thickness, i=1)
        debug_img_duplicates = debug_img_duplicates1 - debug_img_duplicates
        debug_img_duplicates = cv2.cvtColor(debug_img_duplicates, cv2.COLOR_GRAY2RGB)
        debug_img = colorize_label_img(debug_img)
        debug_img = debug_img + debug_img_removed + debug_img_duplicates
        # Write ID labels
        for id, id_label in enumerate(debug_labels):
            cv2.putText(img=debug_img, text=id_label, org=debug_coords[id], fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                        fontScale=params.text_size, color=(150, 150, 150), thickness=params.text_thickness)
        params.debug = debug
        # _debug(visual=final_mask,
        #        filename=os.path.join(params.debug_outdir,
        #                              f"{params.device}_annotation-corrected.png"))
        _debug(visual=debug_img,
               filename=os.path.join(params.debug_outdir,
                                     f"{params.device}_annotation-corrected-debug.png"))
        # Count the number of objects in the final mask
        num = len(np.unique(final_mask)) - 1

        return final_mask, analysis_labels, num
