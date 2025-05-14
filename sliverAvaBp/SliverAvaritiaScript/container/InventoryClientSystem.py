import mod.client.extraClientApi as clientApi
from SliverAvaritiaScript.api.client.BaseClientSystem import BaseClientSystem
from SliverAvaritiaScript import modConfig
import math

compFactory = clientApi.GetEngineCompFactory()
levelId = clientApi.GetLevelId()
minecraftEnum = clientApi.GetMinecraftEnum()

class InventoryClientSystem(BaseClientSystem):
    SERVER_SYSTEM_NAME = ""
    UI_KEY_NAME = ""
    
    def __init__(self, namespace, systemName):
        BaseClientSystem.__init__(self, namespace, systemName)
        self.localPlayerId = clientApi.GetLocalPlayerId()
        self.screen = None
        self.addListenEvent(self.inventoryItemChangedClient, eventName="InventoryItemChangedClientEvent")
        self.addListenEvent(self.openContainer, modConfig.modName, self.SERVER_SYSTEM_NAME, "openContainer")
        self.addListenEvent(self.closeContainer, modConfig.modName, self.SERVER_SYSTEM_NAME, "closeContainer")
        self.listenEvent()

    def listenEvent(self):
        """一个可覆盖的自定义监听函数"""
        pass
    
    def inventoryItemChangedClient(self, args):
        if self.screen and self.screen.gridLoaded:
            playerId = args["playerId"]
            if playerId == self.localPlayerId:
                compFactory.CreateGame(levelId).AddTimer(0.05, self.screen.reloadInventory)
    
    def openContainer(self, args):
        compFactory.CreatePlayer(self.localPlayerId).Swing()
        self.screen = clientApi.PushScreen(modConfig.modName, self.UI_KEY_NAME, {"playerId": self.localPlayerId, "clientSystem": self})
    
    def closeContainer(self, args):
        if self.screen:
            self.screen.OnCloseButtonClick()
        self.serverCaller("OnCloseContainer", {})

class InventoryItemsClientSystem(BaseClientSystem):
    SERVER_SYSTEM_NAME = ""
    UI_KEY_NAME = ""
    ITEM_NAME = []
    def __init__(self, namespace, systemName):
        BaseClientSystem.__init__(self, namespace, systemName)
        self.localPlayerId = clientApi.GetLocalPlayerId()
        self.screen = None
        self.addListenEvent(self.inventoryItemChangedClient, eventName="InventoryItemChangedClientEvent")
        self.addListenEvent(self.openContainer, modConfig.modName, self.SERVER_SYSTEM_NAME, "openContainer")
        self.addListenEvent(self.closeContainer, modConfig.modName, self.SERVER_SYSTEM_NAME, "closeContainer")
        self.listenEvent()

    def listenEvent(self):
        """一个可覆盖的自定义监听函数"""
        pass
    
    def inventoryItemChangedClient(self, args):
        if self.screen and self.screen.gridLoaded:
            playerId = args["playerId"]
            if playerId == self.localPlayerId:
                compFactory.CreateGame(levelId).AddTimer(0.05, self.screen.reloadInventory)
    
    def openContainer(self, args):
        compFactory.CreatePlayer(self.localPlayerId).Swing()
        self.screen = clientApi.PushScreen(modConfig.modName, self.UI_KEY_NAME, {"playerId": self.localPlayerId, "clientSystem": self,"data":args['data']})
    
    def closeContainer(self, args):
        if self.screen:
            self.screen.OnCloseButtonClick()
        self.serverCaller("OnCloseContainer", {})

class InventoryEntityClientSystem(BaseClientSystem):
    SERVER_SYSTEM_NAME = ""
    UI_KEY_NAME = ""
    def __init__(self, namespace, systemName):
        BaseClientSystem.__init__(self, namespace, systemName)
        self.localPlayerId = clientApi.GetLocalPlayerId()
        self.screen = None
        self.addListenEvent(self.inventoryItemChangedClient, eventName="InventoryItemChangedClientEvent")
        self.addListenEvent(self.openContainer, modConfig.modName, self.SERVER_SYSTEM_NAME, "openContainer")
        self.addListenEvent(self.closeContainer, modConfig.modName, self.SERVER_SYSTEM_NAME, "closeContainer")
        self.listenEvent()

    def listenEvent(self):
        """一个可覆盖的自定义监听函数"""
        pass
    
    def inventoryItemChangedClient(self, args):
        if self.screen and self.screen.gridLoaded:
            playerId = args["playerId"]
            if playerId == self.localPlayerId:
                compFactory.CreateGame(levelId).AddTimer(0.05, self.screen.reloadInventory)
    
    def openContainer(self, args):
        compFactory.CreatePlayer(self.localPlayerId).Swing()
        self.screen = clientApi.PushScreen(modConfig.modName, self.UI_KEY_NAME, {"playerId": self.localPlayerId, "clientSystem": self,"data":args['data']})
    
    def closeContainer(self, args):
        if self.screen:
            self.screen.OnCloseButtonClick()
        self.serverCaller("OnCloseContainer", {})

class InventoryBlockClientSystem(BaseClientSystem):
    SERVER_SYSTEM_NAME = ""
    UI_KEY_NAME = ""
    BLOCK_NAME = ""
    def __init__(self, namespace, systemName):
        BaseClientSystem.__init__(self, namespace, systemName)
        self.localPlayerId = clientApi.GetLocalPlayerId()
        self.screen = None
        self.addListenEvent(self.clientItemUseOn, eventName="ClientItemUseOnEvent")
        self.addListenEvent(self.inventoryItemChangedClient, eventName="InventoryItemChangedClientEvent")
        self.addListenEvent(self.openContainer, modConfig.modName, self.SERVER_SYSTEM_NAME, "openContainer")
        self.addListenEvent(self.closeContainer, modConfig.modName, self.SERVER_SYSTEM_NAME, "closeContainer")
        self.listenEvent()

    def listenEvent(self):
        """一个可覆盖的自定义监听函数"""
        pass
    
    def clientItemUseOn(self, args):
        entityId = args["entityId"]
        blockName = args["blockName"]
        if blockName == self.BLOCK_NAME and not compFactory.CreatePlayer(entityId).isSneaking():
            args["ret"] = True
    
    def inventoryItemChangedClient(self, args):
        if self.screen and self.screen.gridLoaded:
            playerId = args["playerId"]
            if playerId == self.localPlayerId:
                compFactory.CreateGame(levelId).AddTimer(0.05, self.screen.reloadInventory)
    
    def openContainer(self, args):
        compFactory.CreatePlayer(self.localPlayerId).Swing()
        self.screen = clientApi.PushScreen(modConfig.modName, self.UI_KEY_NAME, {"playerId": self.localPlayerId, "clientSystem": self, "pos": args["pos"]})
    
    def closeContainer(self, args):
        if self.screen:
            self.screen.OnCloseButtonClick()
        self.serverCaller("OnCloseContainer", {})