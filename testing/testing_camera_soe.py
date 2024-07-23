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

def test_fnc(sequence,thread=0):
    server = 'orchestrator'
    action = 'addExperiment'
    params = dict(experiment=json.dumps(sequence),thread=thread)
    print("requesting")
    requests.post("http://{}:{}/{}/{}".format(
        config['servers']['orchestrator']['host'], 13380, server, action), params=params).json()


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
x = y = np.linspace(0,1,1)
X,Y = np.meshgrid(x,y)
xy = np.vstack([X.ravel(),Y.ravel()]).T
z = np.array([1-np.sum(xyi) for xyi in xy]).reshape(-1,1)
xyz = np.hstack([xy,z])
xyz = xyz[np.where(z>=0)[0],:]
xyz = xyz*Total_vol

comp_1 = xyz[:,0]
comp_2 = xyz[:,1]
comp_3 = xyz[:,2]



#test_fnc(dict(soe=['orchestrator/start','camera/takeImage_0','image/extractColorFromRoi_0'], params=params_exp, meta=dict()))


test_fnc(dict(soe=['orchestrator/start'], params = {'start': {'collectionkey' : 'testing_camera_soe'}},meta = dict()))



crop = {'x':322, 'y':375, 'width':20, 'height':40}
#params_exp = {'start': {'collectionkey' : 'testing_camera_soe'},
              #'takeImage_0':dict(composition_1 = "acid", composition_2 = "base", composition_3 = "water",composition_1_qua = 0, composition_2_qua = 0, composition_3_qua = 0),
              #'extractColorFromRoi_0':{'image_address':'experiment_0:0/takeImage_0/data/image', 'crop':json.dumps(crop)}}
#test_fnc(dict(soe=['orchestrator/start','camera/takeImage_0','image/extractColorFromRoi_0'], params=params_exp, meta=dict()))

for i in range(len(comp_1)):
    params_exp={f'pumpMix_{2*i}': dict(V1 = 0, V2 = 0, V3 = comp_1[i], V4 = 0, V5 = comp_2[i], V6 = comp_3[i], speed = 10, mix = 1, times= 1, cell = False),
                'takeImage_{i}': dict(composition_1 = "acid", composition_2 = "base", composition_3 = "water",composition_1_qua = comp_1[i], composition_2_qua = comp_2[i], composition_3_qua = comp_3[i]),
                'pumpVial_{i}':dict(volume = comp_1[i]+comp_2[i]+comp_3[i], speed = 15, times= 1),
                f'pumpMix_{2*i+1}':dict(V1 = 0, V2 = 0, V3 = 0, V4 = 0, V5 = 0, V6 = 1000, speed = 10, mix = 1, times= 1, cell = True),
                'extractColorFromRoi_{i}':{'image_address':'experiment_{i}:0/takeImage_{i}/data/image', 'crop':json.dumps(crop)}}
    print("work!")
    test_fnc(dict(soe=[f'psd/pumpMix_{2*i}','camera/takeImage_{i}','psd/pumpVial_{i}',f'psd/pumpMix_{2*i+1}','image/extractColorFromRoi_{i}'], params=params_exp, meta=dict()))




test_fnc(dict(soe=['orchestrator/finish'], params={'finish': None}, meta={}))

