"""
basic mandatory imports below
"""
import sys
import uvicorn
from fastapi import FastAPI
import os
from importlib import import_module
from pydantic import BaseModel
import json

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

from boss_driver import BOSS
"""
defines fastapi app
"""
app = FastAPI(title="boss server", 
    description="This is the boss server", 
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
@app.get("/bossDriver/acquire_point")
def acquire_point(X:str,y:str):

    x,y,z = b.acquire_point(json.loads(X),json.loads(y))
    retc = return_class(parameters={}, data={'x':x,'y':y,'z':z})
    return retc


if __name__ == "__main__":
    """
    run app
    """
    b = BOSS(config[serverkey])
    uvicorn.run(app,host=config['servers'][serverkey]['host'],port=config['servers'][serverkey]['port'])

