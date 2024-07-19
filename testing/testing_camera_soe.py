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
from camera_and_take_image_config import config

def test_fnc(sequence,thread=0):
    server = 'orchestrator'
    action = 'addExperiment'
    params = dict(experiment=json.dumps(sequence),thread=thread)
    print("requesting")
    requests.post("http://{}:{}/{}/{}".format(
        config['servers']['orchestrator']['host'], 13380, server, action), params=params).json()

crop = {'x':50, 'y':50, 'width':200, 'height':150}

params_exp={'start': {'collectionkey' : 'camera_test_soe'}, 'takeImage_0': dict(composition_1 = "ethanoic_acid", composition_2 = "phosphoric_acid", composition_3 = "sodium_hydroxide",composition_1_qua = 150, composition_2_qua = 100, composition_3_qua = 100),
        'extractColorFromRoi_0':{'image_address':'experiment_0:0/takeImage_0/data/image', 'crop':json.dumps(crop)}}

test_fnc(dict(soe=['orchestrator/start','camera/takeImage_0','image/extractColorFromRoi_0'], params=params_exp, meta=dict()))

test_fnc(dict(soe=['orchestrator/finish'], params={'finish': None}, meta={}))