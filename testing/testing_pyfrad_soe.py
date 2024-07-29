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
from config.pyfrad_config import config

def test_fnc(sequence,thread=0):
    server = 'orchestrator'
    action = 'addExperiment'
    params = dict(experiment=json.dumps(sequence),thread=thread)
    print("requesting")
    requests.post("http://{}:{}/{}/{}".format(
        config['servers']['orchestrator']['host'], 13380, server, action), params=params).json()

Total_vol = 1000
x = y = np.linspace(0,1,3)
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

test_fnc(dict(soe=['orchestrator/start'], params={'start': {'collectionkey':'pyfrad_test'}}, meta={}))

crop = {'x':50, 'y':50, 'width':200, 'height':150}

for i in range(len(comp_1)):
    j = i+1
    params_exp={f'takeImage_{j}': dict(composition_1 = "ethanoic_acid", composition_2 = "phosphoric_acid", composition_3 = "sodium_hydroxide",composition_1_qua = comp_1[i], composition_2_qua = comp_2[i], composition_3_qua = comp_3[i]),
                f'extractColorFromRoi_{j}':{'image_address':f'experiment_{j}:0/takeImage_{j}/data/image', 'crop' : json.dumps(crop)},
                f'prepareData_{j}':{'x_address':f'experiment_{j}:0/takeImage_{j}/parameters/composition_1_quantity','y_address':f'experiment_{j}:0/takeImage_{j}/parameters/composition_2_quantity','z_address':f'experiment_{j}:0/takeImage_{j}/parameters/composition_3_quantity',
                                    'response_address':f'experiment_{j}:0/extractColorFromRoi_{j}/data/average_color'}}
    test_fnc(dict(soe=[f'camera/takeImage_{j}',f'image/extractColorFromRoi_{j}', f'image/prepareData_{j}'], params=params_exp, meta=dict()))

j += 1

addresses = [f'experiment_{i}:0/prepareData_{i}/data' for i in range(1, len(comp_1)+1)]

test_fnc(dict(soe=[f'pyfrad/pyfrad_{j}',f'orchestrator/modify_{j}',f'camera/takeImage_{j}',f'image/extractColorFromRoi_{j}', f'image/prepareData_{j}'], 
                params={f'pyfrad_{j}':{'address':json.dumps(addresses)},
                f'modify_{j}':{'addresses':[f'experiment_{j}:0/pyfrad_{j}/data/next_x',f'experiment_{j}:0/pyfrad_{j}/data/next_y',f'experiment_{j}:0/pyfrad_{j}/data/next_z'],'pointers':[f'takeImage_{j}/composition_1_qua',f'takeImage_{j}/composition_2_qua',f'takeImage_{j}/composition_3_qua']},
                f'takeImage_{j}':dict(composition_1 = "ethanoic_acid", composition_2 = "phosphoric_acid", composition_3 = "sodium_hydroxide",composition_1_qua = '?', composition_2_qua = '?', composition_3_qua = '?'),
                f'extractColorFromRoi_{j}':{'image_address':f'experiment_{j}:0/takeImage_{j}/data/image', 'crop' : json.dumps(crop)},
                f'prepareData_{j}':{'x_address':f'experiment_{j}:0/takeImage_{j}/parameters/composition_1_quantity','y_address':f'experiment_{j}:0/takeImage_{j}/parameters/composition_2_quantity','z_address':f'experiment_{j}:0/takeImage_{j}/parameters/composition_3_quantity',
                                    'response_address':f'experiment_{j}:0/extractColorFromRoi_{j}/data/average_color'}}, meta=dict()))

n = 2
for i in range(j,j+n):
    j = i+1
    addresses = [f'experiment_{l}:0/prepareData_{l}/data' for l in range(1, j)]
    
    test_fnc(dict(soe=[f'pyfrad/pyfrad_{j}',f'orchestrator/modify_{j}',f'camera/takeImage_{j}',f'image/extractColorFromRoi_{j}', f'image/prepareData_{j}'], 
                params={f'pyfrad_{j}':{'address':json.dumps(addresses)},
                f'modify_{j}':{'addresses':[f'experiment_{j}:0/pyfrad_{j}/data/next_x',f'experiment_{j}:0/pyfrad_{j}/data/next_y',f'experiment_{j}:0/pyfrad_{j}/data/next_z'],'pointers':[f'takeImage_{j}/composition_1_qua',f'takeImage_{j}/composition_2_qua',f'takeImage_{j}/composition_3_qua']},
                f'takeImage_{j}':dict(composition_1 = "ethanoic_acid", composition_2 = "phosphoric_acid", composition_3 = "sodium_hydroxide",composition_1_qua = '?', composition_2_qua = '?', composition_3_qua = '?'),
                f'extractColorFromRoi_{j}':{'image_address':f'experiment_{j}:0/takeImage_{j}/data/image', 'crop' : json.dumps(crop)},
                f'prepareData_{j}':{'x_address':f'experiment_{j}:0/takeImage_{j}/parameters/composition_1_quantity','y_address':f'experiment_{j}:0/takeImage_{j}/parameters/composition_2_quantity','z_address':f'experiment_{j}:0/takeImage_{j}/parameters/composition_3_quantity',
                                    'response_address':f'experiment_{j}:0/extractColorFromRoi_{j}/data/average_color'}}, meta=dict()))


test_fnc(dict(soe=['orchestrator/finish'], params={'finish': None}, meta={}))