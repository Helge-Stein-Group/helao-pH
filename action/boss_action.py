"""
basic mandatory imports below
"""
import sys
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
import requests
import os
from importlib import import_module
import time
import cv2 as cv
import json
import h5py

"""
importation of the config file
"""
helao_root = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(helao_root)
sys.path.append(os.path.join(helao_root, 'config'))
sys.path.append(os.path.join(helao_root, 'driver'))
config = import_module(sys.argv[1]).config
serverkey = sys.argv[2] #specifies which entry in the config file corresponds to this server
from util import hdf5_group_to_dict

"""
defines fastapi app
"""
app = FastAPI(title="boss server", 
    description="This is a camera action server", 
    version="1.0")

class return_class(BaseModel):
    parameters: dict = None
    data: dict = None

""""
below are two example action functions. these have several features
1st, they must have the fastapi function decorator
below the def statement is the body of the function, which communicates with one or more driver servers via requests.get
lastly, we have the return dictionary, which should record all inputs and outputs to the function and lower-level functions 
"""

@app.on_event("startup")
def memory():
    global data
    data = {}
    global awaitedpoints
    awaitedpoints = {}


@app.get("/boss/receiveData")
def receiveData(path: str, run: int, address: str, modelid: int = 0):
    global data

    
    print(address)
    print(run)
    print(path)
    #global awaitedpoints
    if modelid not in data.keys():
        data[modelid] = []
    #if modelid not in awaitedpoints.keys():
    #    awaitedpoints[modelid] = []
    try:
        address = json.loads(address)
    except:
        address = [address]
    newdata = []
    print(address)
    for add in address:
        with h5py.File(path, 'r') as h5file:
            add = f'run_{run}/'+add+'/'
            print('#################################### Here in the boss action receiveData ###################################')
            print(h5file)
            print(add)
            print(hdf5_group_to_dict(h5file, add))
            if isinstance(h5file[add],h5py.Group):
                newdata.append(hdf5_group_to_dict(h5file, add))
                print ("hdf5_group_to_dict")
            else:
                newdata.append(h5file[add][()])
    data[modelid].append(newdata[0] if len(newdata) == 1 else newdata)
    print(f"newdata is {newdata}")
    #if newdata['x'] in awaitedpoints[modelid]:
    #    awaitedpoints[modelid].remove(newdata['x'])
    print(data)
    #print(awaitedpoints)

    '''
        with h5py.File(path,'r') as h5file:
        for address in addresses.values():
            item = h5file[f'run_{run}/'+address]
            print ("h5file[f'run_/'+address]")
            if isinstance(item,h5py._hl.group.Group):
                data.update({address:hdf5_group_to_dict(h5file,f'run_{run}/'+address+'/')})
                print ("hdf5_group_to_dict")
            elif isinstance(item,h5py._hl.dataset.Dataset):
                data.update({address:item[()]})
    '''

@app.get("/boss/boss")
def acquire_point(address: str, modelid=0):
    global data
    print('#################################### Here in the boss action ###################################')
    print(data)
    dat = data[modelid][-1]

    

    x = [da['x']['x'] for da in dat]
    y = [da['x']['y'] for da in dat]
    z = [da['x']['z'] for da in dat]
    key_x = [[i, j, k] for i, j, k in zip(x, y, z)]
    key_y = [da['y']['response'] for da in dat]
    
    print('key_x', key_x, type(key_x))
    print('key_y', key_y, type(key_y))
    result = requests.get(f"{bossurl}/bossDriver/acquire_point",params={'X':json.dumps(key_x), 'y':json.dumps(key_y)}).json()
    
    print('boss action result:',result)
    retc = dict(parameters={'X':json.dumps(key_x), 'y':json.dumps(key_y)}, data={'next_x':result['data']['x'],'next_y':result['data']['y'],'next_z':result['data']['z']})
    return retc



if __name__ == "__main__":
    """
    run app
    """
    bossurl = config[serverkey]['url']
    uvicorn.run(app,host=config['servers'][serverkey]['host'],port=config['servers'][serverkey]['port'])