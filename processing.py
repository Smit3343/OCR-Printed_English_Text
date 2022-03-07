from tensorflow import keras
import numpy as np
import cv2
from keras.preprocessing import image
import os
import imutils


# Vertical back projection
def vProject(binary):
    temp=binary.copy()
    temp[temp==0]=1
    temp[temp==255]=0
    v_projection=np.sum(temp,axis=0)
    return v_projection

# Horizontal projection
def hProject(binary):
    temp=binary.copy()
    temp[temp==0]=1
    temp[temp==255]=0
    h_projection=np.sum(temp,axis=1)
    return h_projection


def charSegmentation(image):  # load image in gray scale
    target_labels="0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!@%&*()+={}[]:;',#.?-"
    cnn=keras.models.load_model('./static/ocr.h5')

    image = cv2.resize(image, None, fx=4, fy=4,interpolation=cv2.INTER_CUBIC)
    ret, thresh = cv2.threshold(image, 127, 255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    
    th = thresh
    h, w = th.shape
    h_h = hProject(th)
    start = 0
    h_start, h_end = [], []
    position = []
    # Vertical segmentation based on horizontal projection
    for i in range(len(h_h)):
        if h_h[i] > 0 and start == 0:  # >0 means 1 or more black pixel
            h_start.append(i)
            start = 1
        if h_h[i] == 0 and start == 1:
            h_end.append(i)
            start = 0

    isEnter = False   
    for i in range(len(h_end)):
        cropImg = th[h_start[i]:h_end[i], 0:w]

        lh,lw = cropImg.shape
        # print(lh,lw)
        if i == 0:
            pass

        w_w = vProject(cropImg)
        wstart, wend, w_start, w_end = 0, 0, 0, 0
        for j in range(len(w_w)):
            
            if i!=0 and j == 0: # not first line and it is first char
              isEnter = True
    
            if w_w[j] > 0 and wstart == 0:  # >0 means 1 or more black pixel
                w_start = j
                wstart = 1
                wend = 0
               
            if w_w[j] == 0 and wstart == 1:
                w_end = j
                wstart = 0
                wend = 1
        
            # Save coordinates when start and end points are confirmed
            if wend == 1:
                isSpace = False
                count = 0
                while(w_w[j]==0):
                  count+=1
                  j+=1
                  if count>lh/4:
                    isSpace = True
                    break
                position.append([w_start, h_start[i], w_end, h_end[i],isSpace,isEnter])
                isEnter=False
            
                wend = 0

    char=''
    roiArr=[]
    space=[]
    enter=[]
    # # Determine division position
    for i,p in enumerate(position):
        roi = thresh[p[1]:p[3], p[0]:p[2]]
        roi = cv2.copyMakeBorder(roi, top=15, bottom=15, left=15, right=15, borderType=cv2.BORDER_CONSTANT,value=(255,255,255))
        roi = cv2.resize(roi, (64, 64), interpolation=cv2.INTER_AREA)
        roiArr.append(roi)
        if p[5]:
          enter.append(i)
        if p[4]:
          space.append(i)

    roiArr = np.asarray(roiArr)
    
    for i,element in enumerate(cnn.predict(roiArr)):
      if i in enter:
        char+='\n'
      char+=target_labels[np.argmax(element)]
      if i in space:
        char+=' '
    return char

def extractText(filename):
    image=cv2.imread("./static/img/" + filename,0)
    image = cv2.copyMakeBorder(image, top=15, bottom=15, left=15, right=15, borderType=cv2.BORDER_CONSTANT,value=(255,255,255))
    # plt.imshow(image,cmap='gray')
    text = charSegmentation(image)
    # os.remove("./static/" + filename)
    return text