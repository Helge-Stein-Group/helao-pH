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
from config.camera_and_take_image_config import config


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

#taking an image
call_orchestrator(dict(soe=['orchestrator/start','camera/take_image', 'image/extract_color_from_roi'],
                       params={'start': {'collectionkey' : 'al_sequential'},
                               'take_image':{'composition_1': "ethanoic_acid", 'composition_2':"phosphoric_acid", 'composition_3':"sodium_hydroxide", "composition_1_qua":150, "composition_2_qua":100, "composition_3_qua":100},
                               'extract_color_from_roi':{'image_path':image_path}}))
#image_path = take_image('take_image', params=dict(composition_1 = "ethanoic_acid", composition_2 = "phosphoric_acid", composition_3 = "sodium_hydroxide",composition_1_qua = 150, composition_2_qua = 100, composition_3_qua = 100))
#print (image_path)
#average_col = image_analysis('extract_color_from_roi', params=dict(image_path))
#print (average_col)

                    