import requests
import os
import serial
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import sys
import json
sys.path.append(r'../config')
sys.path.append(r'../action')
sys.path.append(r'../server')
import time
#from config.mischbares_small import config
from config.pHopt_config import config


def call_orchestrator (sequence,thread=0):
    server = 'orchestrator'
    action = 'addExperiment'
    params = dict(experiment=json.dumps(sequence),thread=thread)
    print("requesting")
    requests.post("http://{}:{}/{}/{}".format(
        config['servers']['orchestrator']['host'], 13380, server, action), params=params).json()
    
def take_image(action, params):
    server = 'camera'
    action = action
    params = params
    res = requests.get("http://{}:{}/{}/{}".format(
        config['servers']['camera']['host'], 
        config['servers']['camera']['port'],server , action),
        params= params).json()
    return res

def image_analysis(action, params):
    server = 'image'
    action = action
    params = params['data']['directory']
    print(params)
    res = requests.get("http://{}:{}/{}/{}".format(
        config['servers']['image']['host'], 
        config['servers']['image']['port'],server , action),
        params={'image_path':params}).json()
    res = res['data']['average_color']
    return res


#image_path = take_image('takeImage', params=dict(composition_1 = "ethanoic_acid", composition_2 = "phosphoric_acid", composition_3 = "sodium_hydroxide",composition_1_qua = 100, composition_2_qua = 100, composition_3_qua = 100))
#print (image_path)
image_path = "C:/Users/DigiCat/Documents/red_blue_water_inorder_titration_image/0_500_500.jpg"
image = cv.imread(image_path)
image_hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)  # Convert to HSV

x=322
y=375
width = 20
height = 40
roi_image = image[int(y):int(y)+int(height),int(x):int(x)+int(width)]
roi_image_hsv = image_hsv[int(y):int(y)+int(height),int(x):int(x)+int(width)]
cv.imshow('ROI', roi_image)
cv.waitKey(0)
cv.destroyAllWindows()
#roi_image = [row[int(x):int(x)+int(width)] for row in image[int(y):int(y)+int(height)]]

        # Calculate the average color in the ROI
average_color_hsv = np.mean(roi_image_hsv, axis=(0, 1))[0]
average_color = np.mean(roi_image, axis=(0, 1))[0]
#average_col = image_analysis('extractColorFromRoi', params=dict(image_path))
print(average_color_hsv)

                    