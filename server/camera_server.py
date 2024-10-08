"""
basic mandatory imports below
"""
import sys
import uvicorn
from fastapi import FastAPI
import os
from importlib import import_module
from pydantic import BaseModel


"""
importation of the config file
"""
helao_root = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(os.path.join(helao_root, 'config'))
sys.path.append(os.path.join(helao_root, 'driver'))
sys.path.append(helao_root)
#from template_driver import template
config = import_module(sys.argv[1]).config
serverkey = sys.argv[2]

from camera_driver import camera
"""
defines fastapi app
"""
app = FastAPI(title="camera server", 
    description="This is the camera server", 
    version="1.0")


"""
instantiate device object on server startup
"""
@app.on_event("startup")
def startup_event():
    global t
    #t = template(config[serverkey])

class return_class(BaseModel):
    parameters: dict = None
    data: dict = None

""""
below are two example action functions. these have several features
1st, they must have the fastapi function decorator
below the def statement is the body of the function, which communicates with one or more driver servers via requests.get
lastly, we have the return dictionary, which should record all inputs and outputs to the function and lower-level functions 
"""
@app.get("/cameraDriver/take_image")
def take_image(composition_1:str, composition_2:str, composition_3:str, composition_1_qua:int, composition_2_qua:int, composition_3_qua:int):  
    dir_name = c.take_image(composition_1,composition_2,composition_3,composition_1_qua,composition_2_qua,composition_3_qua)
    retc = return_class(parameters={'composition_1_quantity':composition_1_qua, 'composition_2_quantity':composition_2_qua, 'composition_3_quantity':composition_3_qua}, data={'directory':dir_name})
    return dir_name


if __name__ == "__main__":
    """
    run app
    """
    c = camera(config[serverkey])
    uvicorn.run(app,host=config['servers'][serverkey]['host'],port=config['servers'][serverkey]['port'])

