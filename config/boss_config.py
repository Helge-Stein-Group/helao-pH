config = dict()

#urls of all servers
config['servers'] = dict(orchestrator = dict(host="127.0.0.1",port=13380),
                         bossDriver = dict(host="127.0.0.1",port=13385),
                         camera = dict(host="127.0.0.1",port=13386),)

#config information for action and driver servers
config['bossDriver'] = dict(limits=[[-1,1],[-1,1]])
config['camera'] = dict(url="http://127.0.0.1:13385")

#path determines the directory under which h5 data files will be saved
config['orchestrator'] = dict(path=r'C:\Users\Operator\Documents\data',kadiurl=None)

#
config['launch'] = dict(server = ['bossDriver'],
                        action = ['camera'],
                        orchestrator = ['orchestrator'])

config['instrument'] = "template"

