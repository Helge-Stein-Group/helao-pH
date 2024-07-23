import requests
import sys
sys.path.append(r'../config')
sys.path.append(r'../action')
sys.path.append(r'../server')
import time
import json
from config.pHopt_config import config

def psd_test(action, params):
    server = 'psd'
    action = action
    params = params
    res = requests.get("http://{}:{}/{}/{}".format(
        config['servers']['psd']['host'], 
        config['servers']['psd']['port'],server , action),
        params= params).json()
    return res

#psd_test('pumpSimple', params=dict(volume = 200, valve = 2, speed = 10, times= 1))
# Aspirate from the single vial to the syringe and dispense to the cell
## Doesnt dispense to the cell!

#psd_test('pumpMix', params=dict(V1 = 0, V2 = 0, V3 = 800, V4 = 0, V5 = 0, V6 = 0, speed = 20, mix = 1, times= 1, cell = False))
#psd_test('pumpSimple', params=dict(volume = 400, valve = 4, speed = 10, times= 1))
# Aspirate from all desired vials to syringe, 
# if mix =! 0, then liquid will be pumped between syringe and mix vial for mix times 
# if cell = True, then dispense to the cell, else dispense to the mix vial

psd_test('pumpVial', params=dict(volume = 1200, speed = 10, times= 1)) 
psd_test('pumpMix', params=dict(V1 = 0, V2 = 0, V3 = 0, V4 = 0, V5 = 0, V6 = 1000, speed = 10, mix = 1, times= 3, cell = True))
# if V > 0, then aspirate from mix vial to syringe and dispense to the cell, if V < 0, then from cell to syringe and back to mix vial

#psd_test('pumpRead', params=dict())
# position of the syringe
