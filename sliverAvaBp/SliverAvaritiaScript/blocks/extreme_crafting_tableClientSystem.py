import mod.client.extraClientApi as clientApi
from SliverAvaritiaScript.container.InventoryClientSystem import InventoryBlockClientSystem
from SliverAvaritiaScript import modConfig

compFactory = clientApi.GetEngineCompFactory()
levelId = clientApi.GetLevelId()
minecraftEnum = clientApi.GetMinecraftEnum()

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