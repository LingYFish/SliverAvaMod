from ..sliver_x_lib.client.core.api import  clientApi
from ..sliver_x_lib.ui.backpack.Inventory import Inventory
from ..sliver_x_lib.ui.backpack.itemSlot import ItemSlot
from ..sliver_x_lib.ui.backpack.hoverButton import hoverButton
from ..sliver_x_lib.util.itemStack import ItemStack
import json
import math
ViewBinder = clientApi.GetViewBinderCls()
compFactory = clientApi.GetEngineCompFactory()
levelId = clientApi.GetLevelId()
minecraftEnum = clientApi.GetMinecraftEnum()

class collect(Inventory):
    PATH_TO_CONTAINER = {}
    inventoryPanel = Inventory.bg + "/inventory_panel"
    hotbarGrid = inventoryPanel + "/hotbar_grid"
    inventoryGrid = inventoryPanel + "/inventory_grid"

    def __init__(self, namespace, name, param = None):
        Inventory.__init__(self, namespace, name, param)
        self.data = {}
        self.Progress = "NaN"

    @staticmethod
    def truncate_float(num):
        return float("{:.3f}".format(float(num)))

    @ViewBinder.binding(ViewBinder.BF_BindString, "#Progress")
    def ProgressInfo(self):
        return "Progress:" + str(self.Progress) + "%%"

    def LoadContainer(self):
        path = self.bg + '/item_cell'
        self.PATH_TO_CONTAINER[path] = "output"
        self.containerSlots[path] = ItemSlot(self, path, path,True,False)

    def Update(self):
        Inventory.Update(self)
        if not self.gridLoaded:
            return
        blockInfoComp = compFactory.CreateBlockInfo(levelId)
        blockEntityData = blockInfoComp.GetBlockEntityData(self.pos)
        if not blockEntityData:
            return
        if not "exData" in blockEntityData:
            return
        exData = blockEntityData["exData"]
        if float(exData['_container_']['__Progress__']['Progress'].get("__value__")) <= 0.0:
            self.Progress = "NaN"
        else:
            self.Progress = self.truncate_float(exData['_container_']['__Progress__']['Progress'].get("__value__"))
        if exData != self.data:
            self.reloadContainer(exData)

    def reloadContainer(self, data):
        self.data = data
        containerToPath = {v: k for k, v in self.PATH_TO_CONTAINER.items()}
        if 'container_slot' not in self.data['_container_']:
            return
        for i in self.data['_container_']['container_slot'].keys():
            path = containerToPath.get(i)
            if path:
                itemDict = json.loads(self.data['_container_']['container_slot'][i].get("__value__"))
                self.containerSlots[path].setSlotItem(itemDict)