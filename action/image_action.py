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
import matplotlib.pyplot as plt

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

@app.get("/image/extract_color_from_roi")
def extract_color_from_roi(image_path):
    print(image_path)
    average_color = requests.get(f"{imageurl}/imageDriver/extract_color_from_roi",params={'image_path':image_path}).json()
    retc = return_class(parameters={'image_path':image_path}, data={'average_color':average_color['data']['Average Color']})
    return retc

if __name__ == "__main__":
    """
    run app
    """
    imageurl = config[serverkey]['url']
    uvicorn.run(app,host=config['servers'][serverkey]['host'],port=config['servers'][serverkey]['port'])