import argparse
from curses.textpad import rectangle
import os
import cv2
import pyautogui
import numpy as np
import time
import json
from random import randint

framedict = {}
framecounter = 0
a = []



def showposition(action, x, y,flags,param):
    global framedict, framecounter,a
    print(framecounter, action)
    res=[]
    res.append(x)
    res.append(y)
    if(action==0):
        print("hover")
        
        framedict[f'frame{framecounter}'] = res
        
    if(action== cv2.EVENT_MOUSEWHEEL):
        
        if(flags>0):
            print("scroll up")
            param[0]+=5
        elif(flags <0 and param[0]-5>0):
            print("scroll down")
            param[0]-=5
    res.append(param[0])
    print(res)
    a.append(res)
    framedict[f'frame{framecounter}'] = res
    
    

    # elif(action == cv2.EVENT_LBUTTONDOWN):
    #     print("left")
    #     key=f'frame{framecounter}'
    #     if(key in framedict.keys()):
    #         print("deleted")
    #         del framedict[f'frame{framecounter}']
    # elif(action == cv2.EVENT_RBUTTONDOWN):
    #     print("right")
    #     framedict[f'frame{framecounter}'] = [x,y,param]
    #     print("added back")






def writer(filename):
    writename = filename.split('.')[0] + '.json'
    global framedict
    with open(writename, 'w') as outfile:
        json.dump(framedict, outfile)
    



def labeler(img, counter, color):
    global framedict, reclen
    try:
        x,y,size = framedict[f'frame{counter}']
        reclen=size
        xmin = int(x) - reclen - randint(0,3)
        xmax = int(x) + reclen + randint(0,3)
        ymin = int(y) - reclen - randint(0,3)
        ymax = int(y) + reclen + randint(0,3)
        img = cv2.rectangle(img, (xmin,ymin), (xmax,ymax), color, 2, 5)
    except Exception as e:
        print(e)
        pass
    return img

def videomaker(source, colors_required=(0,0,255),fps=10,size=20):
    global framedict,framecounter
    cap = cv2.VideoCapture(source)
    #fps = cap.get(cv2.CAP_PROP_FPS)
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
                   

def run(source, processed = False, color = (0,0,255), fps=10,size=20):
    global framecounter
    
    print(fps)
    cap = cv2.VideoCapture(source)
    if (cap.isOpened()== False): 
        print("Error opening video stream or file")
    starter = 0
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == True:
            cv2.imshow(f'Frame',frame)
            param=[size,frame]
            cv2.setMouseCallback('Frame', showposition,param)
            cv2.imshow(f'Frame',labeler(param[1],framecounter,(0,0,255)))
            
            framecounter = framecounter + 1
            
            if cv2.waitKey(int(1000/fps)) & 0xFF == ord('q'):
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
        videomaker(source, color,fps)

def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=str)
    parser.add_argument('--processed', type=bool)
    parser.add_argument('--fps', deafult=50,type=int)
    parser.add_argument('--size',default=20,type=int)
    opt = parser.parse_args()
    return opt

def main(opt):
    run(**vars(opt))

if __name__ == "__main__":
    opt = parse_opt()
    main(opt)

# print(a)
# print(len(a))
print(a)
