"""
basic mandatory imports below
"""
import sys
import uvicorn
from fastapi import FastAPI
import requests
import json
import os
from pydantic import BaseModel
from importlib import import_module
import cv2 as cv
import numpy as np
import h5py
import matplotlib.pyplot as plt
import h5py#


"""
importation of the config file
"""
helao_root = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(os.path.join(helao_root, 'config'))
config = import_module(sys.argv[1]).config
serverkey = sys.argv[2] #specifies which entry in the config file corresponds to this server


"""
defines fastapi app
"""
app = FastAPI(title="image server (action)", 
    description="This is an image action server", 
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

@app.get("/image/receiveData")
def receiveData(path:str,run:int,addresses:str):
    addresses = json.loads(addresses)
    print("yes we can")
    #print('adresses:',addresses)
    global data
    print ("after global data")
    with h5py.File(path,'r') as h5file:
        for address in addresses.values():
            item = h5file[f'run_{run}/'+address]
            print ("h5file[f'run_/'+address]")
            if isinstance(item,h5py._hl.group.Group):
                data.update({address:hdf5_group_to_dict(h5file,f'run_{run}/'+address+'/')})
                print ("hdf5_group_to_dict")
            elif isinstance(item,h5py._hl.dataset.Dataset):
                data.update({address:item[()]})
        

@app.get("/image/extractColorFromRoi")
def extractColorFromRoi(image_address:str, crop):
    #print(image_path)
    
    print('############################################# HELLO ##################################')
    image = data[image_address]
    image = np.array(image)
    print(type(image))
    print(image.shape, image.dtype)
    image = cv.cvtColor(image.astype('uint8'), cv.COLOR_BGR2HSV)  # Convert to HSV
    crop = json.loads(crop)
    x = crop['x']
    y = crop['y']
    width = crop['width']
    height = crop['height']
    # Extract the ROI

    roi_image = image[int(y):int(y)+int(height),int(x):int(x)+int(width)]
    #print('roi_image', roi_image)
    # Calculate the average color in the ROI
    average_color = np.mean(roi_image, axis=(0, 1))[0]
    color_roi_std = np.std(roi_image, axis=(0, 1))[0]

    print('average_color', average_color)

    retc = return_class(parameters={'image_address':image_address, 'crop':crop}, data={'average_color':average_color, 'standard_deviation':color_roi_std})
    
    return retc

if __name__ == "__main__":
    """
    run app
    """
    #imageurl = config[serverkey]['url']
    uvicorn.run(app,host=config['servers'][serverkey]['host'],port=config['servers'][serverkey]['port'])