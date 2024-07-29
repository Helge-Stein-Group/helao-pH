config = dict()

#urls of all servers
config['servers'] = dict(orchestrator = dict(host="127.0.0.1",port=13380),
                         psdDriver=dict(host="127.0.0.1", port=13370),
                         psd=dict(host="127.0.0.1", port=13371),
                         cameraDriver = dict(host="127.0.0.1",port=13385),
                         camera = dict(host="127.0.0.1",port=13386),
                         imageDriver = dict(host="127.0.0.1",port=13387),
                         image = dict(host="127.0.0.1",port=13388),
                         bossDriver = dict(host="127.0.0.1",port=13389),
                         boss = dict(host="127.0.0.1",port=13390),
                         pyfradDriver = dict(host="127.0.0.1",port=13391),
                         pyfrad = dict(host="127.0.0.1",port=13392))

#config information for action and driver servers
import numpy as np
x = y = np.linspace(0,1,10)
X,Y = np.meshgrid(x,y)
xy = np.vstack([X.ravel(),Y.ravel()]).T
z = np.array([1-np.sum(xyi) for xyi in xy]).reshape(-1,1)
xyz = np.hstack([xy,z])
xyz = xyz[np.where(z>=0)[0],:]

config['psdDriver'] = dict(port=4, baud=9600, psd_type = '4', psd_syringe = '1.25m', speed = 10) #PSD.PSDTypes.psd4.value, PSD.SyringeTypes.syringe125mL.value
config['psd'] = dict(url="http://127.0.0.1:13370", valve = {'S1': 2, 'S2': 3, 'S3': 4, 'S4': 5, 'S5': 6, 'S6': 7, 'Out': 1, 'Mix': 8}, volume = 1250, speed = 10)
config['cameraDriver'] = dict(port=1, width = 640, height = 480, exposure = -6, manual_exp = True)
config['camera'] = dict(url="http://127.0.0.1:13385")
config['imageDriver'] = dict(x = 50, y = 50, width = 200, height = 150)
config['image'] = dict(url="http://127.0.0.1:13387")
config['bossDriver'] = dict(limits=[[0,1],[0,1],[0,1]], candidate_grid = xyz)
config['boss'] = dict(url="http://127.0.0.1:13389")
config['pyfradDriver'] = dict(limits=[[0,1],[0,1],[0,1]], candidate_grid = xyz)
config['pyfrad'] = dict(url="http://127.0.0.1:13391")


#path determines the directory under which h5 data files will be saved
config['orchestrator'] = dict(path=r'C:\Users\DigiCat\Documents\data',kadiurl=None)

#
config['launch'] = dict(server = ['psdDriver','cameraDriver','imageDriver','bossDriver','pyfradDriver'],
                        action = ['psd','camera','image','boss','pyfrad'],
                        orchestrator = ['orchestrator'])

config['instrument'] = "template"

