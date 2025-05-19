import mod.client.extraClientApi as clientApi
from SliverAvaritiaScript.container.Inventory import Inventory
from SliverAvaritiaScript.container.itemSlot import ItemSlot
from SliverAvaritiaScript.container.hoverButton import hoverButton
from SliverAvaritiaScript.api.lib.itemStack import ItemStack
from SliverAvaritiaScript import modConfig
import json
import math
ViewBinder = clientApi.GetViewBinderCls()
compFactory = clientApi.GetEngineCompFactory()
levelId = clientApi.GetLevelId()
minecraftEnum = clientApi.GetMinecraftEnum()

class compress(Inventory):
    PATH_TO_CONTAINER = {}
    inventoryPanel = Inventory.bg + "/inventory_panel"
    hotbarGrid = inventoryPanel + "/hotbar_grid"
    inventoryGrid = inventoryPanel + "/inventory_grid"

    def __init__(self, namespace, name, param = None):
        Inventory.__init__(self, namespace, name, param)
        self.data = {}
        self.Progress = "NaN"

    def setInput(self,ItemName,text,Aux):
        return "§9输入物品:§r:{}\n§9物品标识符:{}".format(ItemName,text)
    
    def setOutput(self,ItemName,text,Aux):
        return "§9输出物品:§r:{}\n§9n§9物品标识符:{}".format(ItemName,text)

    @ViewBinder.binding(ViewBinder.BF_BindString, "#Progress")
    def ProgressInfo(self):
        return "Progress:" + str(self.Progress)

    def LoadContainer(self):
        self.output = hoverButton(self,'{}/output_item/image_button_hover'.format(self.bg),self.setOutput)
        self.input = hoverButton(self,'{}/input_item/image_button_hover'.format(self.bg),self.setInput)
        path = self.bg + '/output'
        self.PATH_TO_CONTAINER[path] = "output"
        self.containerSlots[path] = ItemSlot(self, path, path)

        path = self.bg + '/input'
        self.PATH_TO_CONTAINER[path] = "input"
        self.containerSlots[path] = ItemSlot(self, path, path)

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
        if exData['_container_']['output']['item'].get("__value__") != None:
            self.output.itemDict = json.loads(exData['_container_']['output']['item'].get("__value__"))
            self.output.setUiItem()
        else:
            self.output.itemDict = None
            self.output.setUiItem()
        if exData['_container_']['input']['item'].get("__value__") != None:
            self.input.itemDict = json.loads(exData['_container_']['input']['item'].get("__value__"))
            self.input.setUiItem()
            self.output.setUiItem()
        else:
            self.input.itemDict = None
        if int(exData['_container_']['__Progress__']['Progress'].get("__value__")) <= 0:
            self.Progress = "NaN"
            self.GetBaseUIControl("{}/progress_bar".format(self.bg)).asProgressBar().SetValue(0)
            self.GetBaseUIControl("{}/progress_bar2".format(self.bg)).asProgressBar().SetValue(0)
        else:
            self.Progress = str(exData['_container_']['__Progress__']['Progress'].get("__value__") + '/' + str(exData['_container_']['__Progress__']['MaxProgress'].get("__value__")))
            self.GetBaseUIControl("{}/progress_bar".format(self.bg)).asProgressBar().SetValue(max(0,float(exData['_container_']['__Progress__']['Progress'].get("__value__"))/float(exData['_container_']['__Progress__']['MaxProgress'].get("__value__"))))
            self.GetBaseUIControl("{}/progress_bar2".format(self.bg)).asProgressBar().SetValue(max(0,float(exData['_container_']['__Progress__']['Progress'].get("__value__"))/float(exData['_container_']['__Progress__']['MaxProgress'].get("__value__"))))
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

    def exchangeContainerSlot(self, fromSlot, toSlot):
        fromItemStack = fromSlot.itemStack
        toItemStack = toSlot.itemStack
        if toSlot.path in self.PATH_TO_CONTAINER and self.PATH_TO_CONTAINER[toSlot.path] == "output":
            return False
        if not (self.CanDrop(fromItemStack) and self.CanDrop(toItemStack)):
            return
        if self.IsContainerSlot(fromSlot) and not self.IsContainerSlot(toSlot):#从容器内拿取物品
            self.pickItemFromContainer(fromSlot, toSlot)
        elif not self.IsContainerSlot(fromSlot) and self.IsContainerSlot(toSlot):#输入物品到容器
            self.inputItemToContainer(fromSlot, toSlot)
        elif self.IsContainerSlot(fromSlot) and self.IsContainerSlot(toSlot):#移动容器中物品
            self.moveItemInContainer(fromSlot, toSlot)
    
    def pickItemFromContainer(self, fromSlot, toSlot):
        fromItemStack = fromSlot.itemStack
        toItemStack = toSlot.itemStack
        itemComp = compFactory.CreateItem(levelId)
        maxStackSize = toItemStack.getMaxStackSize(itemComp)
        if self.holdSlot == fromSlot:#长按容器内物品后再次点击
            fromSlot.setProgressBar(False, 0.0)
            if toItemStack.isEmpty():
                self.createFlyingItem(fromSlot, toSlot, self.clientSystem.serverCaller, "OnPickItemFromContainer", {"invSlot": toSlot.index, "containerSlot": fromSlot.index, "count": self.holdItemCount})
                if not (self.holdItemCount < fromItemStack.count):
                    fromSlot.setHide(True)
            else:
                itemComp = compFactory.CreateItem(levelId)
                if self.holdSlot.itemStack == toItemStack:
                    mergeCount = min(maxStackSize - toItemStack.count, self.holdItemCount)
                    if mergeCount > 0:
                        self.createFlyingItem(fromSlot, toSlot, self.clientSystem.serverCaller, "OnMergeContainerItemIntoInv", {"invSlot": toSlot.index, "containerSlot": fromSlot.index, "count": mergeCount})
                        if not (mergeCount < fromItemStack.count):
                            fromSlot.setHide(True)
        else:
            if fromItemStack == toItemStack:#堆叠容器内物品至物品栏
                itemComp = compFactory.CreateItem(levelId)
                maxStackSize = toItemStack.getMaxStackSize(itemComp)
                mergeCount = min(maxStackSize - toItemStack.count, fromItemStack.count)
                if mergeCount > 0:
                    self.createFlyingItem(fromSlot, toSlot, self.clientSystem.serverCaller, "OnMergeContainerItemIntoInv", {"invSlot": toSlot.index, "containerSlot": fromSlot.index, "count": mergeCount})
                    if not (mergeCount < fromItemStack.count):
                        fromSlot.setHide(True)
            else:
                if toItemStack.isEmpty():#移动容器内物品至物品栏
                    self.createFlyingItem(fromSlot, toSlot, self.clientSystem.serverCaller, "OnPickItemFromContainer", {"invSlot": toSlot.index, "containerSlot": fromSlot.index, "count": fromItemStack.count})
                    fromSlot.setHide(True)
                else:
                    self.createFlyingItem(fromSlot, toSlot, self.clientSystem.serverCaller, "OnExchangeItemFromContainer", {"invSlot": toSlot.index, "containerSlot": fromSlot.index})
                    self.createFlyingItem(toSlot, fromSlot)
                    fromSlot.setHide(True)
                    toSlot.setHide(True)

    def moveItemInContainer(self, fromSlot, toSlot):
        fromItemStack = fromSlot.itemStack
        toItemStack = toSlot.itemStack
        itemComp = compFactory.CreateItem(levelId)
        maxStackSize = toItemStack.getMaxStackSize(itemComp)
        if self.holdSlot == fromSlot:
            fromSlot.setProgressBar(False, 0.0)
            if toItemStack.isEmpty():
                self.createFlyingItem(fromSlot, toSlot, self.clientSystem.serverCaller, "OnMoveItemInContainer", {"fromSlot": fromSlot.index, "toSlot": toSlot.index, "count": self.holdItemCount})
                if not (self.holdItemCount < fromItemStack.count):
                    fromSlot.setHide(True)
            else:
                itemComp = compFactory.CreateItem(levelId)
                if self.holdSlot.itemStack == toItemStack:
                    mergeCount = min(maxStackSize - toItemStack.count, self.holdItemCount)
                    if mergeCount > 0:
                        self.createFlyingItem(fromSlot, toSlot, self.clientSystem.serverCaller, "OnMergeItemInContainer", {"fromSlot": fromSlot.index, "toSlot": toSlot.index, "count": mergeCount})
                        if not (mergeCount < fromItemStack.count):
                            fromSlot.setHide(True)
        else:
            if not (fromSlot.index == toSlot.index):
                if fromItemStack == toItemStack:
                    itemComp = compFactory.CreateItem(levelId)
                    maxStackSize = toItemStack.getMaxStackSize(itemComp)
                    mergeCount = min(maxStackSize - toItemStack.count, fromItemStack.count)
                    if mergeCount > 0:
                        self.createFlyingItem(fromSlot, toSlot, self.clientSystem.serverCaller, "OnMergeItemInContainer", {"fromSlot": fromSlot.index, "toSlot": toSlot.index, "count": mergeCount})
                        fromSlot.setHide(True)
                else:
                    if toItemStack.isEmpty():
                        self.createFlyingItem(fromSlot, toSlot, self.clientSystem.serverCaller, "OnMoveItemInContainer", {"fromSlot": fromSlot.index, "toSlot": toSlot.index, "count": fromItemStack.count})
                        fromSlot.setHide(True)
                    else:
                        self.createFlyingItem(fromSlot, toSlot, self.clientSystem.serverCaller, "OnExchangeItemInContainer", {"fromSlot": fromSlot.index, "toSlot": toSlot.index})
                        self.createFlyingItem(toSlot, fromSlot)
                        fromSlot.setHide(True)
                        toSlot.setHide(True)
    
    def inputItemToContainer(self, fromSlot, toSlot):
        fromItemStack = fromSlot.itemStack
        toItemStack = toSlot.itemStack
        itemComp = compFactory.CreateItem(levelId)
        maxStackSize = toItemStack.getMaxStackSize(itemComp)
        if self.holdSlot == fromSlot:
            fromSlot.setProgressBar(False, 0.0)
            if toItemStack.isEmpty():
                self.createFlyingItem(fromSlot, toSlot, self.clientSystem.serverCaller, "OnInputItemToContainer", {"fromSlot": fromSlot.index, "toSlot": toSlot.index, "count": self.holdItemCount})
                if not (self.holdItemCount < fromItemStack.count):
                    fromSlot.setHide(True)
            else:
                itemComp = compFactory.CreateItem(levelId)
                if self.holdSlot.itemStack == toItemStack:
                    mergeCount = min(maxStackSize - toItemStack.count, self.holdItemCount)
                    if mergeCount > 0:
                        self.createFlyingItem(fromSlot, toSlot, self.clientSystem.serverCaller, "OnMergeItemIntoContainerInput", {"fromSlot": fromSlot.index, "toSlot": toSlot.index, "count": mergeCount})
                        if not (mergeCount < fromItemStack.count):
                            fromSlot.setHide(True)
        else:
            if fromItemStack == toItemStack:
                itemComp = compFactory.CreateItem(levelId)
                maxStackSize = toItemStack.getMaxStackSize(itemComp)
                mergeCount = min(maxStackSize - toItemStack.count, fromItemStack.count)
                if mergeCount > 0:
                    self.createFlyingItem(fromSlot, toSlot, self.clientSystem.serverCaller, "OnMergeItemIntoContainerInput", {"fromSlot": fromSlot.index, "toSlot": toSlot.index, "count": mergeCount})
                    fromSlot.setHide(True)
            else:
                if toItemStack.isEmpty():
                    self.createFlyingItem(fromSlot, toSlot, self.clientSystem.serverCaller, "OnInputItemToContainer", {"fromSlot": fromSlot.index, "toSlot": toSlot.index, "count": fromItemStack.count})
                    fromSlot.setHide(True)
                else:
                    self.createFlyingItem(fromSlot, toSlot, self.clientSystem.serverCaller, "OnExchangeItemFromContainer", {"invSlot": fromSlot.index, "containerSlot": toSlot.index})
                    self.createFlyingItem(toSlot, fromSlot)
                    fromSlot.setHide(True)
                    toSlot.setHide(True)