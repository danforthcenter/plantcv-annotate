# Contrbution to PlantCV-Annotate

!!! note 
    PlantCV-Annotate is an add-on package to PlantCV so please first refer to the main package's [contributing guide](https://plantcv.readthedocs.io/en/latest/CONTRIBUTING/) for the majority of the information on what and how to contribute to either project (including  but not limited to reporting bugs, requesting new features, add/revise documentation, and adding tutorials). 

## Overview Of What To Contribute to PlantCV-Annotate vs. Other Packages 

This document aims to give an overview of what to contribute to PlantCV-Annotate, and guidelines to
decide which repository is the most appropriate place for new features. Please 
[create an issue in GitHub](https://github.com/danforthcenter/plantcv-annotate/issues) assuming one
does not already exist.

Functions in the Annotate toolbox are considered lower throughput, since they
usually involve interacting with data on a per-image basis, compared to tools from the main PlantCV
package which aim to build modularly into workflows that can be batch processed. 

Data annotation is helpful when downstream analysis steps include machine learning or deep learning,
but it's also helpful for tuning computer vision algorithm approaches by ground truthing a
dataset with annotation and comparing results from the two methods. 
