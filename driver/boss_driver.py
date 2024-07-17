import time
import os
import serial
import cv2 as cv
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from boss_mod.bo import bo_main

class BOSS():
    def __init__(self,conf):  
        self.limits = conf['limits']
        self.grid = conf['candidate_grid']

    def acquire_point(self,data_path:str):
        f = lambda x: 1 # just a placeholder as we don't ask BOSS to call f
        bos = bo_main.BOMain(f, self.limits)
        X = np.load(data_path+'\\X.npy')
        y = np.load(data_path+'\\y.npy')

        bos._update_model(X, y)
        bos.acq_manager.optimtype = 'grid'
        
        X_next = bos.acq_manager.acquire(grid = self.grid)

        return X_next[0][0], X_next[0][1], X_next[0][2]
         

    