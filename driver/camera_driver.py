import time
import os
import serial
import cv2 as cv
import numpy as np


class camera():

    def __init__(self,conf):  
        self.port = conf['port']
        self.width = conf['width']
        self.height = conf['height']
        self.exposure = conf['exposure']
        self.manual_exp = conf['manual_exp']
         

    def take_image(self, composition_1:str, composition_2:str, composition_3:str, composition_1_qua:int, composition_2_qua:int, composition_3_qua:int):
        documents_path = os.path.expanduser('~\Documents')
        IMAGE_DIR = os.path.join(documents_path, composition_1+"_"+composition_2+"_"+composition_3+"_"+'titration_image')
        cap = cv.VideoCapture(self.port,cv.CAP_DSHOW)
        if self.manual_exp==True:
            manual_exp=0.25
        else:
            manual_exp=0.75
        cap.set(cv.CAP_PROP_FRAME_WIDTH, self.width)
        cap.set(cv.CAP_PROP_FRAME_HEIGHT, self.height)
        cap.set(cv.CAP_PROP_AUTO_EXPOSURE, manual_exp)  # Manual exposure
        cap.set(cv.CAP_PROP_EXPOSURE, self.exposure)  # Adjust exposure value
        if cap.isOpened():
            ret, frame = cap.read() # Try to get the first frame
        else:
            print("Cannot open camera")
            exit()
        ret, frame = cap.read()
        #time_stamp = time.strftime("%Y_%m_%d_%Hh_%Mm_%Ss", time.localtime())
        dir_name = os.path.join(IMAGE_DIR, str(composition_1_qua)+"_"+str(composition_2_qua)+"_"+str(composition_3_qua)+".jpg")
        if not os.path.exists(IMAGE_DIR):
            os.makedirs(IMAGE_DIR)
        cv.imwrite(dir_name, frame)
        print(f"Image has been saved: {dir_name}")
        cap.release()
        #print(frame)
        #print(frame.tolist())
        return frame.tolist()
    
    # def take_image(self, composition_1:str, composition_2:str, composition_3:str, composition_1_qua:int, composition_2_qua:int, composition_3_qua:int):
    #     documents_path = os.path.expanduser('~\Documents')
    #     IMAGE_DIR = os.path.join(documents_path, composition_1+"_"+composition_2+"_"+composition_3+"_"+'titration_image')
    #     frame = np.random.randint(0,256 ,size=(128,128,3))
    #     #time_stamp = time.strftime("%Y_%m_%d_%Hh_%Mm_%Ss", time.localtime())
    #     dir_name = os.path.join(IMAGE_DIR, str(composition_1_qua)+"_"+str(composition_2_qua)+"_"+str(composition_3_qua)+".jpg")
    #     if not os.path.exists(IMAGE_DIR):
    #         os.makedirs(IMAGE_DIR)
    #     cv.imwrite(dir_name, frame)
    #     print(f"Image has been saved: {dir_name}")
        
    #     #print(frame)
    #     #print(frame.tolist())
    #     return frame.tolist()