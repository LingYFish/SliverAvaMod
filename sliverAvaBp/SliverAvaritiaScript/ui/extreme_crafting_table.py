import mod.client.extraClientApi as clientApi
from SliverAvaritiaScript.container.Inventory import Inventory
from SliverAvaritiaScript.container.itemSlot import ItemSlot
from SliverAvaritiaScript.recipe.recipeHelper import extremeCraftingTable
from SliverAvaritiaScript.api.lib.itemStack import ItemStack
from SliverAvaritiaScript import modConfig
import json
import math
ViewBinder = clientApi.GetViewBinderCls()
compFactory = clientApi.GetEngineCompFactory()
levelId = clientApi.GetLevelId()
minecraftEnum = clientApi.GetMinecraftEnum()

class extreme_crafting_table(Inventory):
    PATH_TO_CONTAINER = {}
    inventoryPanel = Inventory.bg + "/inventory_panel"
    hotbarGrid = inventoryPanel + "/hotbar_grid"
    inventoryGrid = inventoryPanel + "/inventory_grid"

    def __init__(self, namespace, name, param = None):
        Inventory.__init__(self, namespace, name, param)
        self.data = {}

    def LoadContainer(self):
        path = self.bg + '/output'
        self.PATH_TO_CONTAINER[path] = "output"
        self.containerSlots[path] = ItemSlot(self, path, path)

        for i in xrange(25):
            slot = i + 1
            path = self.bg + '/recipe/grid/item_cell{}'.format(slot)
            self.PATH_TO_CONTAINER[path] = 'recipe_slot{}'.format(slot)
            self.containerSlots[path] = ItemSlot(self, path, path)
            try:
                self.containerSlots[path].setSlotItem(extremeCraftingTable.recipeItems[i])
            except:
                pass

        for i in xrange(len(extremeCraftingTable.recipeItems)):
            slot = i + 1
            path = self.bg + '/recipe/grid/item_cell{}'.format(slot)
            self.PATH_TO_CONTAINER[path] = 'recipe_slot{}'.format(slot)
            self.containerSlots[path] = ItemSlot(self, path, path)
            self.containerSlots[path].setSlotItem(extremeCraftingTable.recipeItems[i])

        for i in xrange(81):
            slot = i + 1
            path = self.bg + '/crafting/grid/item_cell{}'.format(slot)
            self.PATH_TO_CONTAINER[path] = 'crafting_slot{}'.format(slot)
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
        if exData != self.data:
            self.reloadContainer(exData)
        for i in xrange(len(extremeCraftingTable.recipeItems)):
            slot = i + 1
            path = self.bg + '/recipe/grid/item_cell{}'.format(slot)
            self.containerSlots[path].setSlotItem(extremeCraftingTable.recipeItems[i])

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
        self.clientSystem.serverCaller("requestRecipe", {})

    def setSelectSlot(self, itemSlot):
        if self.isRecipeSlot(itemSlot):
            self.clientSystem.serverCaller("requestRecipeId", {"itemName": itemSlot.itemStack.identifier})
        else:
            Inventory.setSelectSlot(self, itemSlot)

    def isOutputSlot(self,fromSlot):
        #type: (ItemSlot) -> bool
        return fromSlot.path == self.bg+"/output"
    
    def isRecipeSlot(self,fromSlot):
        #type: (ItemSlot) -> bool
        return "recipe_slot" in self.PATH_TO_CONTAINER.get(fromSlot.path,"")

    def exchangeContainerSlot(self, fromSlot, toSlot):
        fromItemStack = fromSlot.itemStack
        toItemStack = toSlot.itemStack
        if not (self.CanDrop(fromItemStack) and self.CanDrop(toItemStack)):
            return
        if self.isRecipeSlot(fromSlot) or self.isRecipeSlot(toSlot):
            return
        if self.isOutputSlot(toSlot):
            return
        if self.IsContainerSlot(fromSlot) and not self.IsContainerSlot(toSlot):#从容器内拿取物品
            self.pickItemFromContainer(fromSlot, toSlot)
        elif not self.IsContainerSlot(fromSlot) and self.IsContainerSlot(toSlot):#输入物品到容器
            self.inputItemToContainer(fromSlot, toSlot)
        elif self.IsContainerSlot(fromSlot) and self.IsContainerSlot(toSlot):#移动容器中物品
            self.moveItemInContainer(fromSlot, toSlot)

    def clearTable(self,eventName,Data):
        self.clientSystem.serverCaller(eventName,Data)
        compFactory.CreateGame(levelId).AddTimer(0.01, lambda:self.clientSystem.serverCaller('clearTable',{}))
    
    def pickItemFromContainer(self, fromSlot, toSlot):
        fromItemStack = fromSlot.itemStack
        toItemStack = toSlot.itemStack
        itemComp = compFactory.CreateItem(levelId)
        maxStackSize = toItemStack.getMaxStackSize(itemComp)
        if self.holdSlot == fromSlot:#长按容器内物品后再次点击
            fromSlot.setProgressBar(False, 0.0)
            if toItemStack.isEmpty():
                if self.isOutputSlot(fromSlot):
                    self.createFlyingItem(fromSlot, toSlot, self.clearTable, "OnPickItemFromContainer", {"invSlot": toSlot.index, "containerSlot": fromSlot.index, "count": self.holdItemCount})
                else:
                    self.createFlyingItem(fromSlot, toSlot, self.clientSystem.serverCaller, "OnPickItemFromContainer", {"invSlot": toSlot.index, "containerSlot": fromSlot.index, "count": self.holdItemCount})
                if not (self.holdItemCount < fromItemStack.count):
                    fromSlot.setHide(True)
            else:
                itemComp = compFactory.CreateItem(levelId)
                if self.holdSlot.itemStack == toItemStack:
                    mergeCount = min(maxStackSize - toItemStack.count, self.holdItemCount)
                    if mergeCount > 0:
                        if self.isOutputSlot(fromSlot):
                            self.createFlyingItem(fromSlot, toSlot, self.clearTable, "OnMergeContainerItemIntoInv", {"invSlot": toSlot.index, "containerSlot": fromSlot.index, "count": mergeCount})
                        else:
                            self.createFlyingItem(fromSlot, toSlot, self.clientSystem.serverCaller, "OnMergeContainerItemIntoInv", {"invSlot": toSlot.index, "containerSlot": fromSlot.index, "count": mergeCount})
                        if not (mergeCount < fromItemStack.count):
                            fromSlot.setHide(True)
        else:
            if fromItemStack == toItemStack:#堆叠容器内物品至物品栏
                itemComp = compFactory.CreateItem(levelId)
                maxStackSize = toItemStack.getMaxStackSize(itemComp)
                mergeCount = min(maxStackSize - toItemStack.count, fromItemStack.count)
                if mergeCount > 0:
                    if self.isOutputSlot(fromSlot):
                        self.createFlyingItem(fromSlot, toSlot, self.clearTable, "OnMergeContainerItemIntoInv", {"invSlot": toSlot.index, "containerSlot": fromSlot.index, "count": mergeCount})
                    else:
                        self.createFlyingItem(fromSlot, toSlot, self.clientSystem.serverCaller, "OnMergeContainerItemIntoInv", {"invSlot": toSlot.index, "containerSlot": fromSlot.index, "count": mergeCount})
                    if not (mergeCount < fromItemStack.count):
                        fromSlot.setHide(True)
            else:
                if toItemStack.isEmpty():#移动容器内物品至物品栏
                    if self.isOutputSlot(fromSlot):
                        self.createFlyingItem(fromSlot, toSlot, self.clearTable, "OnPickItemFromContainer", {"invSlot": toSlot.index, "containerSlot": fromSlot.index, "count": fromItemStack.count})
                    else:
                        self.createFlyingItem(fromSlot, toSlot, self.clientSystem.serverCaller, "OnPickItemFromContainer", {"invSlot": toSlot.index, "containerSlot": fromSlot.index, "count": fromItemStack.count})
                    fromSlot.setHide(True)
                else:
                    if self.isOutputSlot(fromSlot):
                        self.createFlyingItem(fromSlot, toSlot, self.clearTable, "OnExchangeItemFromContainer", {"invSlot": toSlot.index, "containerSlot": fromSlot.index})
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