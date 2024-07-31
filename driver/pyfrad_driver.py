import time
import os
import serial
import cv2 as cv
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from pyFRAD.opt_discrete import RAD_sequential, RAD_batch
from sklearn.mixture import GaussianMixture
from sklearn.cluster import KMeans


class pyfrad():
    def __init__(self,conf):  
        self.limits = conf['limits']
        self.grid = conf['candidate_grid']

    def get_labels(self, X, y):

        gm = GaussianMixture(n_components=2).fit(y.reshape(-1,1))
        labels = gm.predict(y.reshape(-1,1)).ravel()
        return labels

    def acquire_point(self, X, y):

        print('####################### in the pyfrad driver ##################')
        
        print(X)
        print(y)
        X = np.array(X)
        y = np.array(y)

        errors = np.ones(y.shape)

        labels = self.get_labels(X, y)

        conf = True
        svc_opts = {'C':1000}

        pfr = RAD_sequential(X, y, labels, errors = errors, conf = conf, cutoff = 0.1, 
                              svc_options = svc_opts)
        new_point = pfr.get_next_point(self.grid)
            
        return [round(float(new_point[0])), round(float(new_point[1])), round(float(new_point[2]))]
        

    