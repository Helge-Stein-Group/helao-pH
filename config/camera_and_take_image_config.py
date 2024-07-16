config = dict()

#urls of all servers
config['servers'] = dict(orchestrator = dict(host="127.0.0.1",port=13380),
                         cameraDriver = dict(host="127.0.0.1",port=13385),
                         camera = dict(host="127.0.0.1",port=13386),
                         imageDriver = dict(host="127.0.0.1",port=13387),
                         image = dict(host="127.0.0.1",port=13388))

#config information for action and driver servers
config['cameraDriver'] = dict(port=1, width = 640, height = 480, exposure = -1, manual_exp = True)
config['camera'] = dict(url="http://127.0.0.1:13385")
config['imageDriver'] = dict(x = 50, y = 50, width = 200, height = 150)
config['image'] = dict(url="http://127.0.0.1:13387")

#path determines the directory under which h5 data files will be saved
config['orchestrator'] = dict(path=r'C:\Users\Operator\Documents\data',kadiurl=None)

#
config['launch'] = dict(server = ['cameraDriver','imageDriver'],
                        action = ['camera','image'],
                        orchestrator = ['orchestrator']
                        )

config['instrument'] = "template"

