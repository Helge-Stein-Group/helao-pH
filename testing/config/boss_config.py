config = dict()

#urls of all servers
config['servers'] = dict(orchestrator = dict(host="127.0.0.1",port=13380),
                         bossDriver = dict(host="127.0.0.1",port=13385),
                         camera = dict(host="127.0.0.1",port=13386),)

#config information for action and driver servers
import numpy as np
x = y = np.linspace(0,1,10)
X,Y = np.meshgrid(x,y)
xy = np.vstack([X.ravel(),Y.ravel()]).T
z = np.array([1-np.sum(xyi) for xyi in xy]).reshape(-1,1)
xyz = np.hstack([xy,z])
xyz = xyz[np.where(z>=0)[0],:]

config['bossDriver'] = dict(limits=[[0,1],[0,1],[0,1]], candidate_grid = xyz)
config['camera'] = dict(url="http://127.0.0.1:13385")

#path determines the directory under which h5 data files will be saved
config['orchestrator'] = dict(path=r'C:\Users\Operator\Documents\data',kadiurl=None)

#
config['launch'] = dict(server = ['bossDriver'],
                        action = ['camera'],
                        orchestrator = ['orchestrator'])

config['instrument'] = "template"

