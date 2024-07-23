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
x = y = np.linspace(0,1,3)
X,Y = np.meshgrid(x,y)
xy = np.vstack([X.ravel(),Y.ravel()]).T
z = np.array([1-np.sum(xyi) for xyi in xy]).reshape(-1,1)
xyz = np.hstack([xy,z])
xyz = xyz[np.where(z>=0)[0],:]
xyz = xyz*Total_vol

repeat_xyz = np.repeat(xyz,3,axis=0)
repeat_xyz_random = np.random.permutation(repeat_xyz)


comp_1 = xyz[:,0]
comp_2 = xyz[:,1]
comp_3 = xyz[:,2]

comp_4 = repeat_xyz[:,0]
comp_5 = repeat_xyz[:,1]
comp_6 = repeat_xyz[:,2]

comp_7 = repeat_xyz_random[:,0]
comp_8 = repeat_xyz_random[:,1]
comp_9 = repeat_xyz_random[:,2]


#test_fnc(dict(soe=['orchestrator/start','camera/takeImage_0','image/extractColorFromRoi_0'], params=params_exp, meta=dict()))


test_fnc(dict(soe=['orchestrator/start'], params = {'start': {'collectionkey' : 'testing_camera_soe'}},meta = dict()))



crop = {'x':322, 'y':375, 'width':20, 'height':40}
#params_exp = {'start': {'collectionkey' : 'testing_camera_soe'},
              #'takeImage_0':dict(composition_1 = "acid", composition_2 = "base", composition_3 = "water",composition_1_qua = 0, composition_2_qua = 0, composition_3_qua = 0),
              #'extractColorFromRoi_0':{'image_address':'experiment_0:0/takeImage_0/data/image', 'crop':json.dumps(crop)}}
#test_fnc(dict(soe=['orchestrator/start','camera/takeImage_0','image/extractColorFromRoi_0'], params=params_exp, meta=dict()))

for i in range(len(comp_4)):
    params_exp={f'pumpMix_{2*i}': dict(V1 = 0, V2 = 0, V3 = comp_4[i], V4 = 0, V5 = comp_5[i], V6 = comp_6[i], speed = 20, mix = 1, times= 1, cell = False),
                f'takeImage_{i}': dict(composition_1 = "red", composition_2 = "blue", composition_3 = "water_inorder",composition_1_qua = comp_4[i], composition_2_qua = comp_5[i], composition_3_qua = comp_6[i]),
                f'pumpVial_{i}':dict(volume = comp_4[i]+comp_5[i]+comp_6[i], speed = 15, times= 1),
                f'pumpMix_{2*i+1}':dict(V1 = 0, V2 = 0, V3 = 0, V4 = 0, V5 = 0, V6 = 1000, speed = 10, mix = 1, times= 3, cell = True),
                f'extractColorFromRoi_{i}':{'image_address':f'experiment_{i+1}:0/takeImage_{i}/data/image', 'crop':json.dumps(crop)}}
    print("work!")
    test_fnc(dict(soe=[f'psd/pumpMix_{2*i}',f'camera/takeImage_{i}',f'psd/pumpVial_{i}',f'psd/pumpMix_{2*i+1}',f'image/extractColorFromRoi_{i}'], params=params_exp, meta=dict()))




test_fnc(dict(soe=['orchestrator/finish'], params={'finish': None}, meta={}))

