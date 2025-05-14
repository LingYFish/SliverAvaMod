from mod.common.mod import Mod
import mod.server.extraServerApi as serverApi
import mod.client.extraClientApi as clientApi
from SliverAvaritiaScript.modConfig import *

@Mod.Binding(modName, modVersion)
class QEmcMod(object):
    def __init__(self):
        pass
    
    @Mod.InitServer()
    def initServer(self):
        print("====={} initServer=====".format(modName))
        for systemName, systemPath in SystemInit.ServerSystem:
            serverApi.RegisterSystem(modName, systemName, systemPath)
    
    @Mod.DestroyServer()
    def destroyServer(self):
        print("====={} destroyServer=====".format(modName))
    
    @Mod.InitClient()
    def initClient(self):
        print("====={} initClient=====".format(modName))
        for systemName, systemPath in SystemInit.ClientSystem:
            clientApi.RegisterSystem(modName, systemName, systemPath)

    @Mod.DestroyClient()
    def destroyClient(self):
        print("====={} destroyClient=====".format(modName))