config = dict()

#urls of all servers
config['servers'] = dict(orchestrator = dict(host="127.0.0.1",port=13380),
                         pyfradDriver = dict(host="127.0.0.1",port=13385),
                         cameraDriver = dict(host="127.0.0.1",port=13389),
                         camera = dict(host="127.0.0.1",port=13386),
                         pyfrad = dict(host="127.0.0.1",port=13383),
                         image = dict(host="127.0.0.1",port=13388),)

#config information for action and driver servers
import numpy as np
Total_vol = 1000
x = y = np.linspace(0,1,10)
X,Y = np.meshgrid(x,y)
xy = np.vstack([X.ravel(),Y.ravel()]).T
z = np.array([1-np.sum(xyi) for xyi in xy]).reshape(-1,1)
xyz = np.hstack([xy,z])
xyz = xyz[np.where(z>=0)[0],:]
xyz = np.array(xyz*Total_vol , dtype=int)

config['pyfradDriver'] = dict(limits=[[0,1],[0,1],[0,1]], candidate_grid = xyz)
config['pyfrad'] = dict(url="http://127.0.0.1:13385")
config['camera'] = dict(url="http://127.0.0.1:13389")
config['cameraDriver'] = dict(port=1, width = 640, height = 480, exposure = -1, manual_exp = True)


#path determines the directory under which h5 data files will be saved
config['orchestrator'] = dict(path=r'C:\Users\DigiCat\Documents\data',kadiurl=None)

#
config['launch'] = dict(server = ['pyfradDriver','cameraDriver'],
                        action = ['camera','image','pyfrad'],
                        orchestrator = ['orchestrator'])

config['instrument'] = "template"

