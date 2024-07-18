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

def test_fnc(sequence,thread=0):
    server = 'orchestrator'
    action = 'addExperiment'
    params = dict(experiment=json.dumps(sequence),thread=thread)
    print("requesting")
    requests.post("http://{}:{}/{}/{}".format(
        config['servers']['orchestrator']['host'], 13380, server, action), params=params).json()

def psd_test(action, params):
    server = 'psd'
    action = action
    params = params
    res = requests.get("http://{}:{}/{}/{}".format(
        config['servers']['psd']['host'], 
        config['servers']['psd']['port'],server , action),
        params= params).json()
    return res

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


params_exp={'start': {'collectionkey' : 'camera_test_soe'},
            'pumpMix_0': dict(V1 = 400, V2 = 0, V3 = 0, V4 = 0, V5 = 0, V6 = 0, speed = 10, mix = 1, times= 1, cell = False),
            'takeImage_0': dict(composition_1 = "ethanoic_acid", composition_2 = "phosphoric_acid", composition_3 = "sodium_hydroxide",composition_1_qua = 150, composition_2_qua = 100, composition_3_qua = 100),
            'extractColorFromRoi':{'image_path':r'C:\Users\DigiCat\Documents\1_1_1_titration_image'}}

test_fnc(dict(soe=['orchestrator/start','psd/pumpMix_0','camera/takeImage_0','image/extractColorFromRoi'], params=params_exp, meta=dict()))

test_fnc(dict(soe=['orchestrator/finish'], params={'finish': None}, meta={}))