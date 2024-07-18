config = dict()

#urls of all servers
config['servers'] = dict(orchestrator = dict(host="127.0.0.1",port=13380),
                         psdDriver=dict(host="127.0.0.1", port=13370),
                         psd=dict(host="127.0.0.1", port=13371),
                         cameraDriver = dict(host="127.0.0.1",port=13385),
                         camera = dict(host="127.0.0.1",port=13386),
                         imageDriver = dict(host="127.0.0.1",port=13387),
                         image = dict(host="127.0.0.1",port=13388))

#config information for action and driver servers
config['psdDriver'] = dict(port=4, baud=9600, psd_type = '4', psd_syringe = '1.25m', speed = 10) #PSD.PSDTypes.psd4.value, PSD.SyringeTypes.syringe125mL.value
config['psd'] = dict(url="http://127.0.0.1:13370", valve = {'S1': 2, 'S2': 3, 'S3': 4, 'S4': 5, 'S5': 6, 'S6': 7, 'Out': 1, 'Mix': 8}, volume = 1250, speed = 10)
config['cameraDriver'] = dict(port=1, width = 640, height = 480, exposure = -1, manual_exp = True)
config['camera'] = dict(url="http://127.0.0.1:13385")
config['imageDriver'] = dict(x = 50, y = 50, width = 200, height = 150)
config['image'] = dict(url="http://127.0.0.1:13387")

#path determines the directory under which h5 data files will be saved
config['orchestrator'] = dict(path=r'C:\Users\Operator\Documents\data',kadiurl=None)

#
config['launch'] = dict(server = ['psdDriver','cameraDriver','imageDriver'],
                        action = ['psd','camera','image'],
                        orchestrator = ['orchestrator']
                        )

config['instrument'] = "template"

