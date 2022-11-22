## Detect_and_Track.py

### How to Use
#### For images
<p>Store the images in a folder in the same directory </p>

Run the following command
```    
python detect_and_track.py --weight yolov7.pt --source folder_name --classes 0 --name "YOLOV7 Object Tracking"
```
<p>class 0 represents person class
<p>If you want to test the model on one image only</p>

Run the following command
```    
python detect_and_track.py --weight yolov7.pt --source img_path --classes 0 --name "YOLOV7 Object Tracking"
```

Results are stored under run/detect/
