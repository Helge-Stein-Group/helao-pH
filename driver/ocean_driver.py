from seabreeze.cseabreeze import SeaBreezeAPI
import json
import time
#there are more features that the device has which we could implement
#try calling self.device.features to see a dictionary of them
#i think this is enough for now, however

class ocean:
    def __init__(self):
        self.api = SeaBreezeAPI()
        #this is convoluted, but will prevent code from crashing if initiated when no spectrometer connected
        a = self.api.list_devices()
        self.device = None if len(a) == 0 else a[0]
        self.open()

    def findDevice(self):
        a = self.api.list_devices()
        self.device = None if len(a) == 0 else a[0]
        return self.device

    def open(self):
        self.device.open()

    def close(self):
        self.device.close()

    #can integrate for between 8ms and 1600s
    #t is integration time in µs
    #maximum intensity is 200000
    def readSpectrum(self,t:int,filename:str):
        self.device.f.spectrometer.set_integration_time_micros(8000)
        self.device.f.spectrometer.get_intensities()
        #first two lines should clear buffer so that spectrometer doesn't pull any data collected before this function was called
        self.device.f.spectrometer.set_integration_time_micros(t)
        data = {'wavelengths':self.device.f.spectrometer.get_wavelengths().tolist(),'intensities':self.device.f.spectrometer.get_intensities().tolist(),
                'units':{'wavelengths':'nm','intensities':'counts'}}
        with open(filename,'w') as outfile: 
            json.dump(data,outfile)
        #time.sleep(t/1000000)
        return data

    def loadFile(self,filename:str):
        with open(filename,'r') as infile:
            data = json.load(infile)
        return data