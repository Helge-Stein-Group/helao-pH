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

<<<<<<< HEAD
def take_image(action, params):
    server = 'camera'
    action = action
    params = params
    res = requests.get("http://{}:{}/{}/{}".format(
        config['servers']['camera']['host'], 
        config['servers']['camera']['port'],server , action),
        params= params).json()
    return res
=======
params_exp={'start': {'collectionkey' : 'camera_test_soe'}, 'takeImage_0': dict(composition_1 = "ethanoic_acid", composition_2 = "phosphoric_acid", composition_3 = "sodium_hydroxide",composition_1_qua = 150, composition_2_qua = 100, composition_3_qua = 100),
        'extractColorFromRoi_0':{'image_path':'experiment_0:0/takeImage_0/data/mean'}}
>>>>>>> 437f98e2fcc878d05013ddf9842fa8a45be47f15

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


Total_vol = 1000
x = y = np.linspace(0,1,6)
X,Y = np.meshgrid(x,y)
xy = np.vstack([X.ravel(),Y.ravel()]).T
z = np.array([1-np.sum(xyi) for xyi in xy]).reshape(-1,1)
xyz = np.hstack([xy,z])
xyz = xyz[np.where(z>=0)[0],:]
xyz = xyz*Total_vol

comp_1 = xyz[:,0]
comp_2 = xyz[:,1]
comp_3 = xyz[:,2]




test_fnc(dict(soe=['orchestrator/start'], params = {'start': {'collectionkey' : 'camera_test_soe'}}))
#for i in range(len(comp_1)):
    #params_exp={'pumpMix_{i}': dict(V1 = comp_1[i], V2 = comp_2[i], V3 = comp_3[i], V4 = 0, V5 = 0, V6 = 0, speed = 10, mix = 1, times= 1, cell = False),
                # 'takeImage_{i}': dict(composition_1 = "ethanoic_acid", composition_2 = "phosphoric_acid", composition_3 = "sodium_hydroxide",composition_1_qua = comp_1[i], composition_2_qua = comp_2[i], composition_3_qua = comp_3[i]),
            #'extractColorFromRoi_{i}':{'image_path':r'C:\Users\DigiCat\Documents\1_1_1_titration_image'}}
    #test_fnc(dict(soe=['psd/pumpMix_{i}','camera/takeImage_{i}','image/extractColorFromRoi_{i}'], params=params_exp, meta=dict()))

for i in range(len(comp_1)):
    params_exp={'pumpMix_{i}': dict(V1 = comp_1[i], V2 = comp_2[i], V3 = comp_3[i], V4 = 0, V5 = 0, V6 = 0, speed = 10, mix = 1, times= 1, cell = False),
            'takeImage_{i}': dict(composition_1 = "ethanoic_acid", composition_2 = "phosphoric_acid", composition_3 = "sodium_hydroxide",composition_1_qua = comp_1[i], composition_2_qua = comp_2[i], composition_3_qua = comp_3[i])}
    test_fnc(dict(soe=['psd/pumpMix_{i}','camera/takeImage_{i}'], params=params_exp, meta=dict()))

test_fnc(dict(soe=['orchestrator/finish'], params={'finish': None}, meta={}))