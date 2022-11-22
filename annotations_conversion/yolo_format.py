import json
import os

# folder containing images
folder='required_bucket'

def load_file():
    """
    :output:
        - json file is loaded

    """

    # Loading annotations file 
    f = open(f'Annotations/COCO.json')
    data = json.load(f)
    f.close()
    return data



def get_annot(id):
    """
    :input:
        -id of the image

    :output:
        - image annotations in COCO format if found
          else returns false

    """

    img_ann=[]
    found=False

    data=load_file()
    for ann in data['annotations']:
        
        if(ann is None):

            continue
        else:
            l=len(ann['bbox']) # length of bounding box 
            if(ann['image_id'] == id):
                if(l>0):
                    img_ann.append(ann)
                    found=True
    if(found):
      return img_ann
    else:
        return False



def convert_to_yolo(folder):
    """
    :input:
        -folder: folder containing images

    :output:
        - annotations converted in yolo format and saved in txt file under labels directory

    """

    for name in os.listdir(folder):

        # Extracting file_name 
        m=os.path.join(folder,name).split("\\")
        file_name=m[1]

        data=load_file()

        for info in data['images']:

            img_name=info['file_name'].split(".")[0]
            
            if(file_name==info['file_name']):
                
                # Getting annotations based on id
                id=info['id']
                img_ann=get_annot(id)
                
                img_h=info['height']
                img_w=info['width']

                if(img_ann):
                    
                    if not os.path.exists('labels'):
                            os.makedirs('labels')
                    file_object = open(f"labels/{img_name}.txt", "a")
                    for ann in img_ann:
                                    box=ann['bbox']
                                
                                    x = box[0]
                                    y = box[1]
                                    w = box[2]
                                    h = box[3]
                                    
                                    # Finding midpoints
                                    x_centre = (x + (x+w))/2
                                    y_centre = (y + (y+h))/2
                                    
                                    
                                    # Normalization
                                    x_centre = x_centre / img_w
                                    y_centre = y_centre / img_h
                                    w = w / img_w
                                    h = h / img_h
                                    
                                    # Limiting upto fixed number of decimal places
                                    x_centre = format(x_centre, '.6f')
                                    y_centre = format(y_centre, '.6f')
                                    w = format(w, '.6f')
                                    h = format(h, '.6f')

                                    img_class = ann['category_id'] - 1 # In yolo classes are assigned from 0 onwards
                                    file_object.write(f"{img_class} {x_centre} {y_centre} {w} {h}\n")

                    file_object.close()

convert_to_yolo(folder)

