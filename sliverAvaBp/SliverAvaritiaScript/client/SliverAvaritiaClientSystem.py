from SliverAvaritiaScript.api.client.BaseClientSystem import BaseClientSystem
from SliverAvaritiaScript.modConfig import *
from SliverAvaritiaScript.api.lib.unicodeUtils import UnicodeConvert
from random import uniform
from ..sliver_x_lib.client.core.api import extraClientApi as clientApi
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
        self.default_option = None
        self.NativeScreenManager = clientApi.GetNativeScreenManagerCls().instance()
        self.addListenEvent(self.UiInitFinished,eventName='UiInitFinished')
        self.addListenEvent(self.OnLocalPlayerStopLoading, eventName="OnLocalPlayerStopLoading")
        self.addListenEvent(self.syncFlyState, modName, "SliverAvaritiaServerSystem", "syncFlyState")
        self.addListenEvent(self.StartUsingItemClient, eventName="StartUsingItemClientEvent")
        self.addListenEvent(self.StopUsingItemClientEvent, eventName="StopUsingItemClientEvent")
        self.addListenEvent(self.OnCarriedNewItemChangedClient, eventName="OnCarriedNewItemChangedClientEvent")
        self.addListenEvent(self.shootSound, modName, "SliverAvaritiaServerSystem", "shootSound")
        self.addListenEvent(self.pushScreen, eventName="PushScreenEvent")

    def StartUsingItemClient(self, args):
        playerId = args['playerId']
        itemDict = args['itemDict']
        if itemDict['newItemName'] == ItemType.INFINITY_BOW:
            if playerId == localId:
                compFactory.CreatePlayerAnim(playerId).PlayTpAnimation("bow_equipped")
                self.serverCaller("startUsingBow", {})
    
    def StopUsingItemClientEvent(self, args):
        playerId = args['playerId']
        itemDict = args['itemDict']
        if itemDict['newItemName'] == ItemType.INFINITY_BOW:
            if playerId == localId:
                compFactory.CreatePlayerAnim(playerId).StopAnimation("bow_equipped")
                self.serverCaller("stopUsingBow", {})
    
    def OnCarriedNewItemChangedClient(self, args):
        itemDict = args['itemDict']
        if itemDict and itemDict['newItemName'] == ItemType.INFINITY_BOW:
            playerViewComp = compFactory.CreatePlayerView(levelId)
            if playerViewComp.GetToggleOption(minecraftEnum.OptionId.INPUT_MODE) == minecraftEnum.InputMode.Touch:
                if self.default_option is None:
                    self.default_option = playerViewComp.GetToggleOption(minecraftEnum.OptionId.SPLIT_CONTROLS)
                    if self.default_option == 0:
                        clientApi.SetCrossHair(True)
        else:
            if self.default_option == 0:
                clientApi.SetCrossHair(False)
            self.default_option = None
    
    def shootSound(self, args):
        audioCustomComp = compFactory.CreateCustomAudio(levelId)
        posComp = compFactory.CreatePos(args["playerId"])
        pos = posComp.GetPos()
        audioCustomComp.PlayCustomMusic('random.bow', pos, 1.0, uniform(0.83, 1.25))
    
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
        self.NativeScreenManager.RegisterScreenProxy('crafting.inventory_screen','SliverAvaritiaScript.ui.color_ui.colorUiProxy')
        self.NativeScreenManager.RegisterScreenProxy("crafting_pocket.inventory_screen_pocket", 'SliverAvaritiaScript.ui.color_ui.colorUiProxy')

    def pushScreen(self, args):
        screenName = args.get('screenName', '')
        print (screenName)
        if not screenName:
            return
        if screenName == 'inventory_screen':
            self.NativeScreenManager.RegisterScreenProxy('crafting.inventory_screen','SliverAvaritiaScript.ui.color_ui.colorUiProxy')
        elif screenName == 'inventory_screen_pocket':
            self.NativeScreenManager.RegisterScreenProxy("crafting_pocket.inventory_screen_pocket", 'SliverAvaritiaScript.ui.color_ui.colorUiProxy')