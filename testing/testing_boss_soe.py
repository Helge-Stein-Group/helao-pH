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

Total_vol = 1000
x = y = np.linspace(0,1,2)
X,Y = np.meshgrid(x,y)
xy = np.vstack([X.ravel(),Y.ravel()]).T
z = np.array([1-np.sum(xyi) for xyi in xy]).reshape(-1,1)
xyz = np.hstack([xy,z])
xyz = xyz[np.where(z>=0)[0],:]
xyz = xyz*Total_vol

comp_1 = xyz[:,0]
comp_2 = xyz[:,1]
comp_3 = xyz[:,2]
print(len(comp_1))

test_fnc(dict(soe=['orchestrator/start'], params={'start': {'collectionkey':'boss_test'}}, meta={}))

crop = {'x':322, 'y':375, 'width':20, 'height':40}

for i in range(len(comp_1)):
    j = i+1
    params_exp={f'pumpMix_{2*j}': dict(V1 = 0, V2 = 0, V3 = comp_1[i], V4 = 0, V5 = comp_2[i], V6 = comp_3[i], speed = 20, mix = 1, times= 1, cell = False),
                f'takeImage_{j}': dict(composition_1 = "red", composition_2 = "blue", composition_3 = "water_bosstest",composition_1_qua = comp_1[i], composition_2_qua = comp_2[i], composition_3_qua = comp_3[i]),
                f'pumpVial_{j}':dict(volume = 1100, speed = 15, times= 1),
                f'pumpMix_{2*j+1}':dict(V1 = 0, V2 = 0, V3 = 0, V4 = 0, V5 = 0, V6 = 1000, speed = 10, mix = 1, times= 3, cell = True),
                f'extractColorFromRoi_{j}':{'image_address':f'experiment_{j}:0/takeImage_{j}/data/image', 'crop' : json.dumps(crop)},
                f'prepareData_{j}':{'x_address':f'experiment_{j}:0/takeImage_{j}/parameters/composition_1_quantity','y_address':f'experiment_{j}:0/takeImage_{j}/parameters/composition_2_quantity','z_address':f'experiment_{j}:0/takeImage_{j}/parameters/composition_3_quantity',
                                    'response_address':f'experiment_{j}:0/extractColorFromRoi_{j}/data/average_color'}}
    test_fnc(dict(soe=[f'psd/pumpMix_{2*j}',f'camera/takeImage_{j}', f'psd/pumpVial_{j}', f'psd/pumpMix_{2*j+1}', f'image/extractColorFromRoi_{j}', f'image/prepareData_{j}'], params=params_exp, meta=dict()))

j += 1

addresses = [f'experiment_{i}:0/prepareData_{i}/data' for i in range(1, len(comp_1)+1)]
print("done until initial grid point")

test_fnc(dict(soe=[f'boss/boss_{j}',f'orchestrator/modify_{j}',f'psd/pumpMix_{2*j}',f'camera/takeImage_{j}', f'psd/pumpVial_{j}', f'psd/pumpMix_{2*j+1}',f'image/extractColorFromRoi_{j}', f'image/prepareData_{j}'], 
                params={f'boss_{j}':{'address':json.dumps(addresses)},
                f'modify_{2*j}':{'addresses':[f'experiment_{j}:0/boss_{j}/data/next_x',f'experiment_{j}:0/boss_{j}/data/next_y',f'experiment_{j}:0/boss_{j}/data/next_z'],'pointers':[f'pumpMix_{2*j}/V3',f'pumpMix_{2*j}/V5',f'pumpMix_{2*j}/V6']},
                f'pumpMix_{2*j}': dict(V1 = 0, V2 = 0, V3 = '?', V4 = 0, V5 = '?', V6 = '?', speed = 20, mix = 1, times= 1, cell = False),
                f'modify_{2*j+1}':{'addresses':[f'experiment_{j}:0/boss_{j}/data/next_x',f'experiment_{j}:0/boss_{j}/data/next_y',f'experiment_{j}:0/boss_{j}/data/next_z'],'pointers':[f'takeImage_{j}/composition_1_qua',f'takeImage_{j}/composition_2_qua',f'takeImage_{j}/composition_3_qua']},
                f'takeImage_{j}':dict(composition_1 = "red", composition_2 = "blue", composition_3 = "water_bosstest",composition_1_qua = '?', composition_2_qua = '?', composition_3_qua = '?'),
                f'pumpVial_{j}':dict(volume = 1100, speed = 15, times= 1),
                f'pumpMix_{2*j+1}':dict(V1 = 0, V2 = 0, V3 = 0, V4 = 0, V5 = 0, V6 = 1000, speed = 10, mix = 1, times= 3, cell = True),
                f'extractColorFromRoi_{j}':{'image_address':f'experiment_{j}:0/takeImage_{j}/data/image', 'crop' : json.dumps(crop)},
                f'prepareData_{j}':{'x_address':f'experiment_{j}:0/takeImage_{j}/parameters/composition_1_quantity','y_address':f'experiment_{j}:0/takeImage_{j}/parameters/composition_2_quantity','z_address':f'experiment_{j}:0/takeImage_{j}/parameters/composition_3_quantity',
                                    'response_address':f'experiment_{j}:0/extractColorFromRoi_{j}/data/average_color'}}, meta=dict()))

n = 2
for i in range(j,j+n):
    j = i+1
    addresses = [f'experiment_{l}:0/prepareData_{l}/data' for l in range(1, j)]
    
    test_fnc(dict(soe=[f'boss/boss_{j}',f'orchestrator/modify_{j}',f'psd/pumpMix_{2*j}',f'camera/takeImage_{j}',f'psd/pumpVial_{j}', f'psd/pumpMix_{2*j+1}',f'image/extractColorFromRoi_{j}', f'image/prepareData_{j}'], 
                params={f'boss_{j}':{'address':json.dumps(addresses)},
                f'modify_{j}':{'addresses':[f'experiment_{j}:0/boss_{j}/data/next_x',f'experiment_{j}:0/boss_{j}/data/next_y',f'experiment_{j}:0/boss_{j}/data/next_z'],'pointers':[f'takeImage_{j}/composition_1_qua',f'takeImage_{j}/composition_2_qua',f'takeImage_{j}/composition_3_qua']},
                f'pumpMix_{2*j}': dict(V1 = 0, V2 = 0, V3 = '?', V4 = 0, V5 = '?', V6 = '?', speed = 20, mix = 1, times= 1, cell = False),
                f'takeImage_{j}':dict(composition_1 = "red", composition_2 = "blue", composition_3 = "water_bosstest",composition_1_qua = '?', composition_2_qua = '?', composition_3_qua = '?'),
                f'pumpVial_{j}':dict(volume = 1100, speed = 15, times= 1),
                f'pumpMix_{2*j+1}':dict(V1 = 0, V2 = 0, V3 = 0, V4 = 0, V5 = 0, V6 = 1000, speed = 10, mix = 1, times= 3, cell = True),
                f'extractColorFromRoi_{j}':{'image_address':f'experiment_{j}:0/takeImage_{j}/data/image', 'crop' : json.dumps(crop)},
                f'prepareData_{j}':{'x_address':f'experiment_{j}:0/takeImage_{j}/parameters/composition_1_quantity','y_address':f'experiment_{j}:0/takeImage_{j}/parameters/composition_2_quantity','z_address':f'experiment_{j}:0/takeImage_{j}/parameters/composition_3_quantity',
                                    'response_address':f'experiment_{j}:0/extractColorFromRoi_{j}/data/average_color'}}, meta=dict()))


test_fnc(dict(soe=['orchestrator/finish'], params={'finish': None}, meta={}))