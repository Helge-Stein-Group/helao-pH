import time
import os
import serial
import cv2 as cv
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

class image_process():
    def __init__(self,conf):  
        self.x = conf['x']
        self.y = conf['y']
        self.width = conf['width']
        self.height = conf['height']
        

    def extract_color_from_roi(self,image:list):
        #print (image_path)
        #image = cv.imread(image_path)
        image = np.array(image)
        image = cv.cvtColor(image, cv.COLOR_BGR2HSV)  # Convert to HSV

        x = self.x
        y = self.y
        width = self.width
        height = self.height
        #image = image.tolist()
        #print(image)

        # Extract the ROI

        roi_image = image[int(y):int(y)+int(height),int(x):int(x)+int(width)]
        #roi_image = [row[int(x):int(x)+int(width)] for row in image[int(y):int(y)+int(height)]]

        # Calculate the average color in the ROI
        average_color = np.mean(roi_image, axis=(0, 1))

        #average_color = np.uint8(average_color)
        return int(average_color[0])
         

    