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
import numpy as np

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
app = FastAPI(title="camera server", 
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
@app.get("/camera/takeImage")
def take_image(composition_1:str, composition_2:str, composition_3:str, composition_1_qua:float, composition_2_qua:float, composition_3_qua:float):
    print(composition_1)
    image = requests.get(f"{cameraurl}/cameraDriver/take_image",
                            params={'composition_1':composition_1, 'composition_2':composition_2, 'composition_3':composition_3, 
                                    'composition_1_qua':composition_1_qua, 'composition_2_qua':composition_2_qua, 'composition_3_qua':composition_3_qua}).json()
    retc = return_class(parameters={'composition_1_quantity':composition_1_qua, 'composition_2_quantity':composition_2_qua, 'composition_3_quantity':composition_3_qua}, data={'image':image})
    #print(image)
    return retc




if __name__ == "__main__":
    """
    run app
    """
    cameraurl = config[serverkey]['url']
    uvicorn.run(app,host=config['servers'][serverkey]['host'],port=config['servers'][serverkey]['port'])