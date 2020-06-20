#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import imutils
import cv2
from imutils.video import VideoStream

# Set initial frame size.
frameSize = (640, 480)

# Debug variable
p1 = 0
p2 = 0 # start functions

def read_video_Calibrate(cap):

    if p2 == 1:
        print('read_video started')

    frame = cap.read()

    #flip frame
    frame = cv2.flip(frame, -1)

    #remove unwanted borders
    tp_till = 224
    lt_till = 50
    rt_till = 194
    frame[0:tp_till, :][0:tp_till, :][0:tp_till, :] = (0,0,0) # top rows
    frame[:, 0:lt_till][:, 0:lt_till][:, 0:lt_till] = (0,0,0) # left columns
    frame[:, rt_till:][:, rt_till:][:, rt_till:] = (0,0,0) #right columns

    if p2:
        cv2.imwrite('ImageDetection2.png', frame)

    masked_image = color_detection(frame)

    return masked_image


def read_video(cap):

    if p2 == 1:
        print('read_video started')

    frame = cap.read()

    #flip frame
    frame = cv2.flip(frame, -1)

    #remove unwanted borders
    tp_till = 224
    lt_till = 50
    rt_till = 194
    frame[0:tp_till, :][0:tp_till, :][0:tp_till, :] = (0,0,0) # top rows
    frame[:, 0:lt_till][:, 0:lt_till][:, 0:lt_till] = (0,0,0) # left columns
    frame[:, rt_till:][:, rt_till:][:, rt_till:] = (0,0,0) #right columns

    if p2:
        cv2.imwrite('ImageDetection2.png', frame)

    masked_image = color_detection(frame)

    return masked_image


def color_detection(frame):

    if p2 == 1:
        print('color_detection started')

    result = 0
    # convert the resized image to grayscale, blur it slightly and threshold it
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    blurred = cv2.GaussianBlur(hsv, (5, 5), 0)

    # Range for lower red
    lower_red = np.array([0,120,70])
    upper_red = np.array([10,255,255])
    mask1 = cv2.inRange(blurred, lower_red, upper_red)
 
    # Range for upper range
    lower_red = np.array([170,120,70])
    upper_red = np.array([180,255,255])
    mask2 = cv2.inRange(blurred,lower_red,upper_red)
 
    # Generating the final mask to detect red color
    mask1 = mask1+mask2
    
    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_OPEN, np.ones((5,5),np.uint8))
    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_DILATE, np.ones((5,5),np.uint8))
    
    # find contours in the thresholded image and initialize the
    # shape detector
    cnts = cv2.findContours(mask1.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    if len(cnts) > 0:

        for c in cnts:
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.04 * peri, True)
            (x, y, w, h) = cv2.boundingRect(approx)
            ar = w / float(h)
            print('\tar =',ar)
            
            if len(approx) >= 4 and len(cnts) >= 5:
                # Road block
                result = 2
            else:
                # Stop sign
                result = 1
                
    return result

# sign_and_roadblock_detection.check_surroundings()

def check_surroundings(debug=0):
    '''Checks for road blocks, stop signs or nothing '''

    if p1 == 1:
        print('check_surroundings started')

        # Initialize mutithreading the video stream.
        vs = VideoStream(src=0, usePiCamera=False, resolution=frameSize,
                framerate=32).start()
    else:
        # Initialize mutithreading the video stream.
        vs = VideoStream(src=0, usePiCamera=True, resolution=frameSize,
                framerate=32).start()

    result = 0
    if debug == 0:
        for ii in range(0,5):
            result += read_video(vs)
    else:
        while 1:
            result = read_video_Calibrate(vs)
            print(result)
    
    # Tanslate output:0-2 noting 3-7 is stop 8-10 is block
    final_result = 0
    if result <= 2:
        final_result = 0
    elif result > 2 and result <=7:
        final_result = 1
    else:
        final_result = 2

    # Cleanup before exit.
    vs.stop()

    if p1 == 1:
        print('Detection result',final_result)

    # Returns a string: noting=0 stop=1 block=2
    return final_result

# sign_and_roadblock_detection.take_picture('test7')

def take_picture(name):
    vs = VideoStream(src=0, usePiCamera=False, resolution=frameSize, framerate=32).start()

    frame = vs.read()

    #flip frame
    frame = cv2.flip(frame, -1)

    #remove unwanted borders
    tp_till = 224
    lt_till = 50
    rt_till = 194
    frame[0:tp_till, :][0:tp_till, :][0:tp_till, :] = (0,0,0) # top rows
    frame[:, 0:lt_till][:, 0:lt_till][:, 0:lt_till] = (0,0,0) # left columns
    frame[:, rt_till:][:, rt_till:][:, rt_till:] = (0,0,0) #right columns

    string = "".join([name,'.png'])
    cv2.imwrite(string, frame)
    vs.stop()

def testroutine():
    # Check all images
    imagesList = ['C:/Users/ThomasH/Dokumente/GitHub/Conti_S2F/conti_sign_and_roadblock_detection/blocl7.png',
        'C:/Users/ThomasH/Dokumente/GitHub/Conti_S2F/conti_sign_and_roadblock_detection/blocl14.png',
        'C:/Users/ThomasH/Dokumente/GitHub/Conti_S2F/conti_sign_and_roadblock_detection/blocl21.png',
        'C:/Users/ThomasH/Dokumente/GitHub/Conti_S2F/conti_sign_and_roadblock_detection/blocl28.png',
        'C:/Users/ThomasH/Dokumente/GitHub/Conti_S2F/conti_sign_and_roadblock_detection/blocl35.png',
        'C:/Users/ThomasH/Dokumente/GitHub/Conti_S2F/conti_sign_and_roadblock_detection/blocl42.png',
        'C:/Users/ThomasH/Dokumente/GitHub/Conti_S2F/conti_sign_and_roadblock_detection/blocl49.png',
        'C:/Users/ThomasH/Dokumente/GitHub/Conti_S2F/conti_sign_and_roadblock_detection/stop14.png',
        'C:/Users/ThomasH/Dokumente/GitHub/Conti_S2F/conti_sign_and_roadblock_detection/stop21.png',
        'C:/Users/ThomasH/Dokumente/GitHub/Conti_S2F/conti_sign_and_roadblock_detection/stop28.png',
        'C:/Users/ThomasH/Dokumente/GitHub/Conti_S2F/conti_sign_and_roadblock_detection/stop35.png',
        'C:/Users/ThomasH/Dokumente/GitHub/Conti_S2F/conti_sign_and_roadblock_detection/stop42.png',
        'C:/Users/ThomasH/Dokumente/GitHub/Conti_S2F/conti_sign_and_roadblock_detection/stop49.png']

    for image in imagesList:
        frame = cv2.imread(image,cv2.COLOR_BGR2HSV)
        masked_image = color_detection(frame)
        print(image,'detected',masked_image)


# TEST space
if 0:
    testroutine()
    #take_picture('testthh1')
    #result = check_surroundings(1)
    #print(result)