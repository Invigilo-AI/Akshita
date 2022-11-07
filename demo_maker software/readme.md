# Video Demo Maker
This Documentation is related to the videodemomaker.py

### Classes and Functions
This Python file has 0 classes and contains 5 functions

Function 1: run
Function 2: videomaker
Function 3: showposition
Function 4: labeler
Function 5: writer

### Requirements 
    1)opencv-python
    2)numpy
    3)webcolors

### Imports 
    1)argparse
    2)curses.textpad.rectangle
    3)os
    4)cv2
    5)numpy
    6)time
    7)json
    8)random
    9)webcolors
### How to Use
Run the following command
```    
python videodemomaker.py --source football.mp4 --processed True --fps 10 --size 20 --boxlen 20 --boxwidth 10 --boxcolor red
```
#### The above command takes the following arguements:
    1)source : videofilename
    2)processed : True - (renders video with lables) False - (doesnot render a video)
    3)fps : Frames per second
    4)size : size of bounding box
    5)boxlen : length of bounding box
    6)boxwidth : width of bounding box
    7)boxcolor : color of bounding box
         
