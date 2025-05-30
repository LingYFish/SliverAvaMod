from ..sliver_x_lib.ui.backpack.InventoryClientSystem import InventoryBlockClientSystem
from ..sliver_x_lib.server.core import api as sApi
from ..sliver_x_lib.client.core import api as cApi
from ..sliver_x_lib.server.level import level
from ..sliver_x_lib.util import minecraftEnum
from SliverAvaritiaScript import modConfig


compFactory = cApi.clientApi.GetEngineCompFactory()
levelId = cApi.clientApi.GetLevelId()
minecraftEnum = cApi.clientApi.GetMinecraftEnum()

class extreme_crafting_tableClientSystem(InventoryBlockClientSystem):
    SERVER_SYSTEM_NAME = "extreme_crafting_tableServerSystem"
    UI_KEY_NAME = "extreme_crafting_tableUi"
    BLOCK_NAME = modConfig.BlockType.extreme_crafting_table
    
    def listenEvent(self):
        InventoryBlockClientSystem.listenEvent(self)
        self.addListenEvent(self.showItemText, modConfig.modName, self.SERVER_SYSTEM_NAME, "showItemText")
    
    def showItemText(self, args):
        text = args["text"]
        if self.screen:
            self.screen.ShowItemText(text)

    def openContainer(self, args):
        compFactory.CreatePlayer(cApi.clientApi.GetLocalPlayerId()).Swing()
        self.screen = cApi.clientApi.PushScreen(modConfig.modName, self.UI_KEY_NAME, {"playerId": cApi.clientApi.GetLocalPlayerId(), "clientSystem": self, "pos": args["pos"],"recipeItems":args['recipeItems']})