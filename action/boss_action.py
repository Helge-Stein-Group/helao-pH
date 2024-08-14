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
from sklearn import svm
from sklearn.svm import SVC
import numpy as np
from sklearn.metrics import f1_score
from sklearn.mixture import GaussianMixture

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
    key_y = [da['z']['response'] for da in dat]
    
    print('key_x', key_x, type(key_x))
    print('key_y', key_y, type(key_y))
    result = requests.get(f"{bossurl}/bossDriver/acquire_point",params={'X':json.dumps(key_x), 'y':json.dumps(key_y)}).json()
    
    print('boss action result:',result)
    retc = dict(parameters={'X':json.dumps(key_x), 'y':json.dumps(key_y)}, data={'next_x':result['data']['x'],'next_y':result['data']['y'],'next_z':result['data']['z']})
    return retc




@app.get("/boss/dataAnalysis")
def data_analysis(gridfilepath,totgridpoint,num_data,comp1,comp2,comp3,avghue,numitr,modelid = 0):
    f1_list_iter = []
    if avghue == str(0):
        f1 = 0
        f1_list_iter.append(f1)
        retc = dict(parameters={'Iteration':num_data}, data={'f1_score_list':f1})
    else:
        global data
        print('#################################### Here in the boss analysis ###################################')
        print(data)
        dat = data[modelid][-1]
        dat2 = data[modelid][-1][int(numitr)-2]

        x = [da['x']['x'] for da in dat]
        y = [da['x']['y'] for da in dat]
        z = [da['x']['z'] for da in dat]
        f1_list_array = [dat2['y']['f1_score']]
        if int(numitr) >= 5:
            f1_list_iter2 = f1_list_array[0].tolist()
        else:
            f1_list_iter2 = f1_list_array
        
        for i in range(len(f1_list_iter2)):
            f1_list_iter = f1_list_iter + [float(f1_list_iter2[i])]

        print(f1_list_iter)
        #f1_list_iter = f1_list_array
    
        opt_used_compositions = [[i, j, k] for i, j, k in zip(x, y, z)]
        opt_average_hue_value = [da['z']['response'] for da in dat]

        opt_used_compositions = opt_used_compositions+[[int(comp1),int(comp2),int(comp3)]]
        opt_average_hue_value = opt_average_hue_value+[float(avghue)]
        print('composition and average hue value at this iteration is')
        print(opt_used_compositions)
        print(opt_average_hue_value)


        grid_average_hue_value = []
        grid_all_composition = []

        with h5py.File(gridfilepath, 'r') as h5file:
            for s in range(1,int(totgridpoint)):
                hue_path = f'run_0/experiment_{s+1}:0/extractColorFromRoi_{s}/data/average_color/'
                hue_dataset = h5file[hue_path]
                hue_value = hue_dataset[()]
                grid_average_hue_value.append(hue_value)

                grid_each_composition = []
                for j in range(1,7):
                    composition_path = f'run_0/experiment_{s+1}:0/pumpMix_{2*s}/parameters/V{j}/'
                    composition_dataset = h5file[composition_path]
                    composition_value = composition_dataset[()]
                    grid_each_composition.append(composition_value)
                grid_all_composition.append(grid_each_composition)
        grid_used_compositions=[]
        for i in range(len(grid_all_composition)):
            comp_1=grid_all_composition[i][2]
            comp_2=grid_all_composition[i][4]
            comp_3=grid_all_composition[i][5]
            grid_used_compositions=grid_used_compositions + [[comp_1,comp_2,comp_3]]


    # opt_average_hue_value = []
    # opt_all_composition = []
    # with h5py.File(path, 'r') as h5file:
    #     for s in range(1,num_data):
    #         hue_path = f'run_0/experiment_{s}:0/extractColorFromRoi_{s}/data/average_color/'
    #         hue_dataset = h5file[hue_path]
    #         hue_value = hue_dataset[()]
    #         opt_average_hue_value.append(hue_value)

    #         opt_each_composition = []
    #         for j in range(1,7):
    #             composition_path = f'run_0/experiment_{s}:0/pumpMix_{2*s}/parameters/V{j}/'
    #             composition_dataset = h5file[composition_path]
    #             composition_value = composition_dataset[()]
    #             opt_each_composition.append(composition_value)
    #         opt_all_composition.append(opt_each_composition)
    # opt_used_compositions=[]
    # for i in range(len(opt_all_composition)):
    #     comp_1=opt_all_composition[i][2]
    #     comp_2=opt_all_composition[i][4]
    #     comp_3=opt_all_composition[i][5]
    #     opt_used_compositions=opt_used_compositions + [[comp_1,comp_2,comp_3]]
    
        print("Now calculating f1 score at this iteration")

        X = []
        for i in range(len(grid_average_hue_value)):
            X = X + [[grid_average_hue_value[i]]]
        X = np.array(X)
        gmm = GaussianMixture(n_components=3, random_state=0)
        gmm.fit(X)

        means = gmm.means_
        covariances = gmm.covariances_
        weights = gmm.weights_

        def predict_clusters(data, gmm):
            return gmm.predict(data)
    
        grid_hue_labels = predict_clusters(X, gmm)
    
        test = np.array(grid_used_compositions)
        composition_iter = []
    
        prediction = []
        hue_iter = []
        for s in range(0,int(num_data)):
            hue_iter =  hue_iter + [[opt_average_hue_value[s]]]
        hue_iter = np.array(hue_iter)
        composition_iter = np.array(opt_used_compositions)
        print('hue iter')
        print(hue_iter)
        #print(composition_iter)
        #hue_iter_arr = np.array(opt_hue[0:i])
        #print(hue_iter_arr)
        opt_hue_labels_iter = predict_clusters(hue_iter, gmm)
        print('labels')
        print(opt_hue_labels_iter)
        opt_svc_model = SVC(kernel='linear')
        opt_svc_model.fit(composition_iter,opt_hue_labels_iter)
        prediction_at_iter = opt_svc_model.predict(test)
        f1 = f1_score(grid_hue_labels,prediction_at_iter,average='macro')
        print(type(f1))
        f1 = float(f1)
        print(type(f1))
        print("f1 score at iteration "+num_data+" is "+str(f1))
        print("prediction of grid labels at iteration "+num_data+" is "+str(prediction_at_iter))
        prediction.append(list(prediction_at_iter))
        f1_list_iter.append(f1)
    

        print(f1_list_iter)
        print(type(f1_list_iter))
        #print(prediction)
        #print(type(prediction))

        #retc = dict(parameters={'Iteration':num_data}, data={'f1_score_list':f1_list_iter,'prediction':prediction})
        retc = dict(parameters={'Iteration':num_data}, data={'f1_score_list':f1_list_iter})
    
    return retc



if __name__ == "__main__":
    """
    run app
    """
    bossurl = config[serverkey]['url']
    uvicorn.run(app,host=config['servers'][serverkey]['host'],port=config['servers'][serverkey]['port'])