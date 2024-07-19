"""
basic mandatory imports below
"""
import sys
import uvicorn
from fastapi import FastAPI
import requests
import os
from importlib import import_module
from pydantic import BaseModel

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
app = FastAPI(title="template server", 
    description="This is a fancy template action server", 
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
@app.get("/boss/boss")
def acquire_point(data_path):
    data = requests.get(f"{bossurl}/bossDriver/acquire_point",params={'data_path':data_path}).json()
    retc = dict(parameters={'data_path':data_path}, data=data)
    return retc



if __name__ == "__main__":
    """
    run app
    """
    bossurl = config[serverkey]['url']
    uvicorn.run(app,host=config['servers'][serverkey]['host'],port=config['servers'][serverkey]['port'])