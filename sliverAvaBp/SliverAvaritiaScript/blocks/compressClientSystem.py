import mod.client.extraClientApi as clientApi
from SliverAvaritiaScript.container.InventoryClientSystem import InventoryBlockClientSystem
from SliverAvaritiaScript import modConfig

compFactory = clientApi.GetEngineCompFactory()
levelId = clientApi.GetLevelId()
minecraftEnum = clientApi.GetMinecraftEnum()

class compressClientSystem(InventoryBlockClientSystem):
    SERVER_SYSTEM_NAME = "compressServerSystem"
    UI_KEY_NAME = "compressUi"
    BLOCK_NAME = modConfig.BlockType.compress