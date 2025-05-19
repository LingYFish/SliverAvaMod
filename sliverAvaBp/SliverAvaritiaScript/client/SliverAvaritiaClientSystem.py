from SliverAvaritiaScript.api.client.BaseClientSystem import BaseClientSystem
from SliverAvaritiaScript.modConfig import *
from SliverAvaritiaScript.api.lib.unicodeUtils import UnicodeConvert
import mod.client.extraClientApi as clientApi
import json
import uuid
compFactory = clientApi.GetEngineCompFactory()
levelId = clientApi.GetLevelId()
minecraftEnum = clientApi.GetMinecraftEnum()
localId = clientApi.GetLocalPlayerId()
class SliverAvaritiaClientSystem(BaseClientSystem):
    gameComp = compFactory.CreateGame(levelId)

    def __init__(self, namespace, systemName):
        BaseClientSystem.__init__(self, namespace, systemName)
        self.addListenEvent(self.UiInitFinished,eventName='UiInitFinished')
        self.addListenEvent(self.OnLocalPlayerStopLoading, eventName="OnLocalPlayerStopLoading")
        self.addListenEvent(self.syncFlyState, modName, "SliverAvaritiaServerSystem", "syncFlyState")
    
    def Destroy(self):
        queryVariableComp = compFactory.CreateQueryVariable(levelId)
        queryVariableComp.UnRegister("query.mod.show_wing")
    
    def OnLocalPlayerStopLoading(self, args):
        queryVariableComp = compFactory.CreateQueryVariable(levelId)
        queryVariableComp.Register("query.mod.show_wing", 0.0)
        self.serverCaller("requestFlyState", {})
    
    def syncFlyState(self, args):
        for entityId, flying in args["state"].iteritems():
            queryVariableComp = compFactory.CreateQueryVariable(entityId)
            queryVariableComp.Set("query.mod.show_wing", float(flying))

    def UiInitFinished(self,args):
        for uiKey, clsPath, uiScreenDef in SystemInit.UiScreenNode:
            clientApi.RegisterUI(modName, uiKey, clsPath, uiScreenDef)