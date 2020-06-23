# implement common movement procedures
import sys
sys.path.append(r'../driver')
sys.path.append(r'../config')
sys.path.append(r'../server')
#from mischbares_small import config
import mecademic_server
from copy import copy
import numpy as np
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
import json
import requests

####################################################################test
config = dict()

#we define all the servers here so that the overview is a bit better
config['servers'] = dict(pumpServer = dict(host="127.0.0.1", port=13370),
                         pumpingServer = dict(host="127.0.0.1", port=13371),
                         mecademicServer = dict(host="127.0.0.1", port=13372),
                         movementServer = dict(host="127.0.0.1", port=13373),
                         autolabServer = dict(host="127.0.0.1", port=13374),
                         echemServer = dict(host="127.0.0.1", port=13375),
                         kadiServer = dict(host="127.0.0.1", port=13376),
                         dataServer = dict(host="127.0.0.1", port=13377))

config['kadi'] = dict(host = r"https://kadi4mat.iam-cms.kit.edu",
            PAT = r"98d7dfbcd77a9163dde2e8ca34867a4998ecf68bc742cf4e")

config['movement'] = dict(
    safe_sample_joints = [-56.0, 30.0, 40.0, 5.0, -72.0, 0.0],
    #pose (151.917, -245.409, 133.264, -42.574, -22.04, -70.12)
    safe_reservoir_joints = [-113.5733, 53.743, -1.5102, -132.2144, -65.2762, 32.6695],
    safe_waste_joints = [-10.0, -20.0, 45.0, 0.0, -25.0, 0.0],
    sample_rotation = 0, reservoir_rotation = 0, waste_rotation = 0,
    x_limit_sample = 75, y_limit_sample = 75,
    x_limit_reservoir = 75, y_limit_reservoir = 75,
    x_limit_waste = 10, y_limit_waste = 10)

#############################################################################################
# Add limit rejection
# Add orientationhelp so we can load the same platemap for every plane and it takes care of it

app = FastAPI(title="Mecademic action server V1", 
    description="This is a fancy mecademic action server", 
    version="1.0")

url = "http://{}:{}".format(config['servers']['mecademicServer']['host'], config['servers']['mecademicServer']['port'])

class return_class(BaseModel):
    measurement_type: str = None
    parameters :dict = None
    data: dict = None

@app.get("/movement/matrixRotation")
def matrix_rotation(theta: float):
    theta = np.radians(theta)
    c, s = np.cos(theta), np.sin(theta)
    R = np.array(((c, -s), (s, c)))   
    data = requests.get("{}/movement/rotation".format(url), params={"theta": theta}).json()
    
    retc = return_class(measurement_type='movement_command', parameters= {'command':'getmatrixrotation', "rotation_value": theta}, 
                        data = {'data': data})
    return retc


@app.get("/movement/moveToHome")
def move_to_home():
    # this moves the robot safely to home which is defined as all joints are at 0
    paramd = {lett:val for lett,val in zip("abcdef",zeroj)}
    requests.get("{}/mecademic/dMoveJoints".format(url), params=paramd).json()
    retc = return_class(measurement_type='movement_command', parameters= {'command':'move_to_home'})
    return retc

@app.get("/movement/jogging")
def jogging(joints: float):
    paramd = {lett: val for lett,val in zip("abcdef", joints)}
    data = requests.get("{}/mecademic/dMoveJoints".format(url), params= paramd).json()
    print('Please jog the robot. \n dist:axis \n (i.e 0.1:x, 0.1:y or 0.1:z dist in mm)')
    print('this runs until you say exit')
    pose = copy(requests.get("{}/mecademic/dGetPose".format(url)).json()['data']['poses'])
    pjoint = copy(requests.get("{}/mecademic/dGetJoints".format(url)).json()['data']['joints'])
    while True:
        inp = input()
        if inp == 'exit':
            pose = requests.get("{}/mecademic/dGetPose".format(url)).json()['data']['poses']
            pjoint = requests.get("{}/mecademic/dGetJoints".format(url)).json()
            break
        dist, axis = inp.split(':')
        # Ask the robot to move the poses by distance in axis direction
        dist = float(dist)
        if axis == 'x':
            pose_mod = copy(list(pose))
            pose_mod[0] += dist
            paramd = {lett: val for lett,val in zip("abcdef", pose_mod)}
            requests.get("{}/mecademic/dMovePose".format(url), params= paramd).json()
    
        if axis == 'y':
            pose_mod = copy(list(pose))
            pose_mod[1] += dist
            paramd = {lett: val for lett,val in zip("abcdef", pose_mod)}
            requests.get("{}/mecademic/dMovePose".format(url), params= paramd).json()
        
        if axis == 'z':
            pose_mod = copy(list(pose))
            pose_mod[2] += dist
            paramd = {lett: val for lett,val in zip("abcdef", pose_mod)}
            requests.get("{}/mecademic/dMovePose".format(url), params= paramd).json()

        pose = requests.get("{}/mecademic/dGetPose".format(url)).json()['data']['poses']
        pjoint = requests.get("{}/mecademic/dGetJoints".format(url)).json()

    # move to the safe plane and then return the values
    pose_mod = copy(list(pose))
    pose_mod[2] += 20
    paramd = {lett: val for lett,val in zip("abcdef", pose_mod)}
    requests.get("{}/mecademic/dMovePose".format(url), params= paramd).json()
    pose = requests.get("{}/mecademic/dGetPose".format(url)).json()
    pjoint = requests.get("{}/mecademic/dGetJoints".format(url)).json()

    retc = return_class(measurement_type='movement_command', 
    parameters= {'command':'jogging', 'poses': pose, 'joints': pjoint}, data = {'data': data})
    return retc

# Alignment to sample corner
@app.get("/movement/alignSample")
def align_sample():
    safe_sample_corner, safe_sample_joints = jogging(safe_sample_joints)
    retc = return_class(measurement_type='movement_command', parameters= {'command':'align_sample'}, 
    data = {'safe_sample_corner': safe_sample_corner, 'safe_sample_joints': safe_sample_joints })
    return retc

# Alignment to reservoir corner @fuzhan
@app.get("/movement/alignReservoir")
def align_reservoir():
    safe_reservoir_corner, safe_reservoir_joints = jogging(safe_reservoir_joints)
    retc = return_class(measurement_type='movement_command', parameters= {'command':'align_reservoir'}, 
    data = {'safe_reservoir_corner': safe_reservoir_corner, 'safe_reservoir_joints': safe_reservoir_joints})
    return retc

# Alignment to waste corner @fuzhan
@app.get("/movement/alignWaste")
def align_waste():
    safe_waste_corner, safe_waste_joints = jogging(safe_waste_joints)
    retc = return_class(measurement_type='movement_command', parameters= {'command':'align_waste'}, 
    data = {'safe_waste_corner': safe_waste_corner, 'safe_waste_joints': safe_waste_joints})
    return retc

@app.get("/movement/alignment")
def alignment():
    move_to_home()
    print('Sample Alignment...')
    align_sample()
    move_to_home()
    print('Reservoir Alignment...')
    align_reservoir()
    move_to_home()
    print('Waste Alignment...')
    align_waste()
    move_to_home()
    retc = return_class(measurement_type='movement_command', parameters= {'command':'alignment'})
    return retc

@app.get("/movement/mvToSample")
def mv2sample(x: float, y:float):
    if 0 <= x <= x_limit_sample and 0 <= y <= y_limit_sample:
        p = matrix_rotation(sample_rotation).dot(np.array((x, y)))
        safe_sample_pose = [safe_sample_corner[0] + p[0], safe_sample_corner[1] + p[1],
                            safe_sample_corner[2],
                            safe_sample_corner[3], safe_sample_corner[4], safe_sample_corner[5]]
        sample_pose = copy(safe_sample_pose)
        sample_pose[2] -= 20
        move_to_home()
        # avoid from hitting anything between home and safe sample corner
        paramd = {lett: val for lett,val in zip("abcdef", safe_sample_joints)}
        requests.get("{}/mecademic/dMoveJoints".format(url), params= paramd).json()
        # avoid from hitting anything
        paramP = {lett: val for lett,val in zip("abcdef", safe_sample_pose)}
        requests.get("{}/mecademic/dMovePose".format(url), params= paramP).json()
        # going straight down
        requests.get("{}/mecademic/dqLinZ".format(url), params= {z: -20} ).json()  
    else:
        raise Exception('you are out of boundary')

    retc = return_class(measurement_type='movement_command', parameters= {'command':'mv2sample', 'x': x, 'y': y})
    return retc

@app.get("/movement/mvToReservoir")
def mv2reservoir(x: float, y: float):
    if 0 <= x <= x_limit_reservoir and 0 <= y <= y_limit_reservoir:
        p = matrix_rotation(reservoir_rotation).dot(np.array((x, y)))
        safe_res_pose = [safe_reservoir_corner[0] + p[0], safe_reservoir_corner[1] + p[1],
                            safe_reservoir_corner[2], safe_reservoir_corner[3], safe_reservoir_corner[4],
                            safe_reservoir_corner[5]]
        res_pose = copy(safe_res_pose)
        res_pose[2] -= 20  # in xyzabc
        move_to_home()
        #avoid from hitting anything between home and safe reservoir corner
        paramd = {lett: val for lett,val in zip("abcdef", safe_reservoir_joints)}
        requests.get("{}/mecademic/dMoveJoints".format(url), params= paramd).json()
        # avoid from hitting anything
        paramP = {lett: val for lett,val in zip("abcdef", safe_res_pose)}
        requests.get("{}/mecademic/dMovePose".format(url), params= paramP).json()
        # going straight down
        requests.get("{}/mecademic/dqLinZ".format(url), params= {z: -20} ).json()
    else:
        raise Exception('you are out of boundary')
    
    retc = return_class(measurement_type='movement_command', parameters= {'command':'mv2reservoir', 'x': x, 'y': y})
    return retc
 
@app.get("/movement/moveUp")
def moveup(z: float=50.0):
    pos = requests.get("{}/mecademic/dGetPose".format(url)).json()["data"]["poses"]
    pos[2] += z
    paramd = {lett: val for lett,val in zip("abcdef", pos)}
    data = requests.get("{}/mecademic/dMovePose".format(url), params= paramd).json()
    retc = return_class(measurement_type='movement_command', parameters= {'command':'moveup', 'z': z}, data = {'data': data})
    return retc
    
@app.get("/movement/removeDrop")
def removedrop(y: float=-20):
    pos = list(requests.get("{}/mecademic/dGetPose".format(url)).json()["data"]["poses"])
    pos[1] += y
    paramd = {lett: val for lett, val in zip("abcdef", pos)}
    data = requests.get("{}/mecademic/dMovePose".format(url), params= paramd).json()
    move_to_home()
    retc = return_class(measurement_type='movement_command', parameters= {'command':'removedrop', 'y': y}, data = {'data': data})
    return retc
    
@app.get("/movement/mvToWaste")    
def mv2waste(x: float, y: float):
    if 0 <= x <= x_limit_waste and 0 <= y <= y_limit_waste:
        p = matrix_rotation(waste_rotation).dot(np.array((x, y)))
        # robot.DMoveJoints(*self.safe_waste_joints)
        safe_waste_pose = [safe_waste_corner[0] + p[0], safe_waste_corner[1] + p[1], safe_waste_corner[2],
                            safe_waste_corner[3], safe_waste_corner[4], safe_waste_corner[5]]
        
        waste_pose = copy(safe_waste_pose)
        waste_pose[2] -= 20
        plate_waste_pose = safe_waste_pose  # in xyzabc
        move_to_home()
        # avoid from hitting anything between safe waste corner and home 
        paramd = {lett: val for lett,val in zip("abcdef", safe_waste_joints)}
        datad = requests.get("{}/mecademic/dMoveJoints".format(url), params= paramd).json()
        # avoid from hitting anything
        paramP = {lett: val for lett,val in zip("abcdef", safe_waste_pose)}
        datap = requests.get("{}/mecademic/dMovePose".format(url), params= paramP).json()
        # going straight down
        dataz = requests.get("{}/mecademic/dqLinZ".format(url), params= {z: -20} ).json()
    
    else:
        raise Exception('you are out of boundary')
       
    retc = return_class(measurement_type='movement_command', parameters= {'command':'mv2waste', 'x': x, 'y': y}, 
                        data= {'joints': datad, 'poses': datap, 'z': dataz})
    return retc
 
# move gripper to a specified position, at speed and with defined force @helge
def mvgripper(position, speed, force, robot):
    pass

# just open the gripper @helge
def open():
    pass

# move the linear rail to a certain position @helge
def mvrailabs(pos):
    pass

# move the linear rail to a relative position @helge
def mvrailrel(dist):
    pass


if __name__ == "__main__":
    zeroj = [0, 0, 0, 0, 0, 0]
    move_to_home()
    safe_sample_joints = config['movement']['safe_sample_joints']
    safe_reservoir_joints = config['movement']['safe_reservoir_joints']
    safe_waste_joints = config['movement']['safe_waste_joints']
    sample_rotation = config['movement']['sample_rotation']
    reservoir_rotation = config['movement']['reservoir_rotation']
    waste_rotation = config['movement']['waste_rotation']
    x_limit_sample = config['movement']['x_limit_sample']
    y_limit_sample = config['movement']['y_limit_sample']
    x_limit_reservoir = config['movement']['x_limit_reservoir']
    y_limit_reservoir = config['movement']['y_limit_reservoir']
    x_limit_waste = config['movement']['x_limit_waste']
    y_limit_waste = config['movement']['y_limit_waste']
    
    uvicorn.run(app, host=config['servers']['movementServer']['host'], port=config['servers']['movementServer']['port'])
    print("instantiated mecademic")
    