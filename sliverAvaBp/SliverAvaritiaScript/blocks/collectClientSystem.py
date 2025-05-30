from ..sliver_x_lib.ui.backpack.InventoryClientSystem import InventoryBlockClientSystem
from ..sliver_x_lib.server.core import api as sApi
from ..sliver_x_lib.client.core import api as cApi
from ..sliver_x_lib.server.level import level
from ..sliver_x_lib.util import minecraftEnum
from SliverAvaritiaScript import modConfig


compFactory = cApi.clientApi.GetEngineCompFactory()
levelId = cApi.clientApi.GetLevelId()
minecraftEnum = cApi.clientApi.GetMinecraftEnum()

class collectClientSystem(InventoryBlockClientSystem):
    SERVER_SYSTEM_NAME = "collectServerSystem"
    UI_KEY_NAME = "collectUi"
    BLOCK_NAME = modConfig.BlockType.collect