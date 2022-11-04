import argparse
from curses.textpad import rectangle
import os
import cv2
import pyautogui
import numpy as np
import time
import json
from random import randint
import webcolors as wc

framedict = {}
framecounter = 0
a = []



def showposition(action, x, y,flags,*userdata):
    """
    :input:
          -action : Mouse events(EVENT_MOUSEMOVE/EVENT_MOUSEWHEEL/EVENT_RBUTTONUP/EVENT_LBUTTONUP)
          -x : x coordinate 
          -y : y coordinate 

    :output: dictionary with key and value as:
          -key : framecounter
          -value : [x,y,size] coordinates and size of bounding box respectively
          

    """
    global framedict, framecounter,a,flag,label,boxsize,mouse_still
    
    # print(framecounter, action)
    res=[]
    label=True
    if(flag):
        
        if(action==cv2.EVENT_MOUSEMOVE):
        
            print("hover")
            
            res.append(x)
            res.append(y)
            
            
            mouse_still = False
            

        if(action== cv2.EVENT_MOUSEWHEEL):
            
            flag =True
            if(flags>0):
                print("scroll up")
                boxsize+=5
            elif(flags <0 and boxsize-5>0):
                print("scroll down")
                boxsize-=5

            
            # res.append(x)
            # res.append(y)
            # res.append(param[0])
            # framedict[f'frame{framecounter}']=res
            # print(f"After scrolling {res} ")

        

        

        

        if(action == cv2.EVENT_RBUTTONUP):
            print("right")
            flag= False
            label = False
            mouse_still=False
        
    
        
        

    if(action == cv2.EVENT_LBUTTONUP):
        print("left")
        flag= True
        label= True
    
        
    if(len(res)>0):
        res.append(boxsize)
        a.append(res)
        framedict[f'frame{framecounter}'] = res
        print(framecounter,res)
        a.append(res)

    # print(f"{framecounter} mouse still value inside showposition {mouse_still}")
    

    

def writer(filename):
    writename = filename.split('.')[0] + '.json'
    global framedict
    with open(writename, 'w') as outfile:
        json.dump(framedict, outfile)
    



def labeler(img, counter, color):
    """
    :input:
          -img : image frame
          -counter : framecounter
          -color : color of bounding box

    :output: 
          - img : image frame with labels and bounding boxes
          

    """
    global framedict, reclen,recwid
    try:
        x,y,size = framedict[f'frame{counter}']

        if(recwid is None):
            recwid=reclen

        xmin = int(x) - reclen -size - randint(0,3)
        xmax = int(x) + reclen +size + randint(0,3)
        ymin = int(y) - recwid -size - randint(0,3)
        ymax = int(y) + recwid +size + randint(0,3)
        img = cv2.rectangle(img, (xmin,ymin), (xmax,ymax), color, 2, 5)
    except Exception as e:
        print(e)
        pass
    return img


def videomaker(source, colors_required):
    """
    :input:
          -source : videofile name
          -colors_required : color of the bounding boxes
    
    :output:
          -video file : processed videofile saved in the same directory

    """
    global framedict,framecounter
    cap = cv2.VideoCapture(source)
    fps = cap.get(cv2.CAP_PROP_FPS)
    print(f"processed video '{fps}'")
    if (cap.isOpened()== False): 
        print("Error opening video stream or file")
    starter = 0
    height, width, layers = None, None, None
    out = None
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == True:
            height, width, layers = frame.shape
            size = (width,height)
            break
    cap.release()
    cv2.destroyAllWindows()
    coloring = colors_required
    writename = source.split('.')[0] + '_processed.mp4'
    out = cv2.VideoWriter(writename, cv2.VideoWriter_fourcc(*'mp4v'),fps,size)
    cap = cv2.VideoCapture(source)
    if (cap.isOpened()== False): 
        print("Error opening video stream or file")
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == True:
            out.write(labeler(frame,starter,coloring))
            starter = starter + 1
        else:
            break
    cap.release()
    out.release()
    cv2.destroyAllWindows()
                   

def run(source, processed = False,fps=10,size=20,boxlen=20,boxwidth=10,boxcolor='red'):
    """
    :input:
          -source : videofile name
          -processed : processed video (True/False)
          -fps : frames per second
          -size : size of the bounding box
          -boxlen: bounding box length
          -boxwidth : bounding box width
          -boxcolor : color of the bounding box

    :output: 
          -videofile : video opens in gui window


    """

    global framecounter,flag,label,boxsize,reclen,recwid,color,mouse_still

    boxsize=size
    reclen=boxlen
    recwid=boxwidth
    color=wc.name_to_rgb(boxcolor)
    
    # print(c)
    cap = cv2.VideoCapture(source)
    if (cap.isOpened()== False): 
        print("Error opening video stream or file")
    starter = 0
    flag = True
    label= True
    while(cap.isOpened()):
        ret, frame = cap.read()
        mouse_still=True
        if ret == True:
            cv2.imshow(f'Frame',frame)
            
            cv2.setMouseCallback('Frame', showposition)
            # print(f"after mouse event {mouse_still}")
            if(label):
             cv2.imshow(f'Frame',labeler(frame,framecounter,color))
            cv2.waitKey(2)

            if(mouse_still):
             if(f'frame{framecounter-1}' in framedict.keys()):
                prev_res=framedict[f'frame{framecounter-1}'] 
                framedict[f'frame{framecounter}'] = prev_res
                print(f"mouse still{prev_res}")
                a.append(prev_res)
            print(mouse_still)
            framecounter = framecounter + 1
            
            if cv2.waitKey(fps) & 0xFF == ord('q'):
                break
            if starter==0:
                time.sleep(2)
                starter = 1
        
        else: 
            break
        
    cap.release()
    cv2.destroyAllWindows()
    writer(source)
    if processed:
        videomaker(source, color)

def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=str)
    parser.add_argument('--processed', type=bool)
    parser.add_argument('--fps',default=20,type=int)
    parser.add_argument('--size',default=20,type=int)
    parser.add_argument('--boxlen',default=20,type=int)
    parser.add_argument('--boxwidth',type=int)
    parser.add_argument('--boxcolor',default='red',type=str)
    opt = parser.parse_args()
    return opt



def main(opt):
    run(**vars(opt))

if __name__ == "__main__":
    opt = parse_opt()
    main(opt)

# print(a)
print(framecounter)
print(framedict)
