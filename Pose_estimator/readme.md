# Pose Estimator
This Documentation is related to the pose_estimator.py

### Classes and Functions
This Python file has 0 classes and contains 6 functions

Function 1: process_img
Function 2: process_video
Function 3: run
Function 4: parse_opt
Function 5: plot_fps_time_comparision
Function 6: main

### Requirements 
    1)opencv-python
    2)numpy
    3)os
    4)PIL
    5)torchvision
    6)utilis

### Imports 
    1)os
    2)time
    3)matplotlib
    4)torch
    5)numpy
    6)sys
    7)transforms
    8)Path
    9)letterbox
    10)select_device
    11)attempt_load
    12)output_to_keypoint
    13)plot_skeleton_kpts
    14)non_max_suppression_kpt
    15)strip_optimizer
    16)argparse
    17) Image

### How to Use
Run the following command for predicting pose in an image:
```
python pose_estimator.py --media image --source im1.jpeg

```
Run the following command for prediction pose in a video :
```
python pose_estimator.py --media video --source football.mp4

```
### The above command takes the following arguements:
    1)media : image/video
    2)source : filename
