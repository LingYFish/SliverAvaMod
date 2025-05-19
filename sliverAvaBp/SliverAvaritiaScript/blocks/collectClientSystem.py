import mod.client.extraClientApi as clientApi
from SliverAvaritiaScript.container.InventoryClientSystem import InventoryBlockClientSystem
from SliverAvaritiaScript import modConfig

compFactory = clientApi.GetEngineCompFactory()
levelId = clientApi.GetLevelId()
minecraftEnum = clientApi.GetMinecraftEnum()

class collectClientSystem(InventoryBlockClientSystem):
    SERVER_SYSTEM_NAME = "collectServerSystem"
    UI_KEY_NAME = "collectUi"
    BLOCK_NAME = modConfig.BlockType.collect