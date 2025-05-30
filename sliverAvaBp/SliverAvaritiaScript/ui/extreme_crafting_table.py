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

class Pagination:
    def __init__(self, items):
        """
        初始化分页器
        :param items: 列表，包含所有元素
        """
        self.items = items
        self.page_size = 25

    def CanPrevious(self,current_page):
        """
        判断是否可以向上翻页
        :return: bool
        """
        return current_page > 1

    def CanNext(self,current_page):
        """
        判断是否可以向下翻页
        :return: bool
        """
        total_pages = (len(self.items) + self.page_size - 1) // self.page_size
        return current_page < total_pages


class extreme_crafting_table(Inventory):
    PATH_TO_CONTAINER = {}
    inventoryPanel = Inventory.bg + "/inventory_panel"
    hotbarGrid = inventoryPanel + "/hotbar_grid"
    inventoryGrid = inventoryPanel + "/inventory_grid"

    def __init__(self, namespace, name, param = None):
        Inventory.__init__(self, namespace, name, param)
        self.data = {}
        self.index = 1
        self.recipeItems = param['recipeItems']
        self.pagination = Pagination(self.recipeItems)

    def LoadContainer(self):
        path = self.bg + '/output'
        self.PATH_TO_CONTAINER[path] = "output"
        self.containerSlots[path] = ItemSlot(self, path, path,True,False)

        for i in range(25*self.index):
            slot = i + 1
            if i*self.index > len(self.recipeItems) - 1:
                path = self.bg + '/recipe/grid/item_cell{}'.format(slot)
                self.PATH_TO_CONTAINER[path] = 'recipe_slot{}'.format(slot)
                self.containerSlots[path] = ItemSlot(self, path, path,False,False)
                continue
            path = self.bg + '/recipe/grid/item_cell{}'.format(slot)
            self.PATH_TO_CONTAINER[path] = 'recipe_slot{}'.format(slot)
            self.containerSlots[path] = ItemSlot(self, path, path,False,False)
            self.containerSlots[path].setSlotItem(self.recipeItems[i*self.index])

        for i in range(81):
            slot = i + 1
            path = self.bg + '/crafting/grid/item_cell{}'.format(slot)
            self.PATH_TO_CONTAINER[path] = 'crafting_slot{}'.format(slot)
            self.containerSlots[path] = ItemSlot(self, path, path,True,True)

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
        for i in range(25*self.index):
            slot = i + 1
            if i*self.index > len(self.recipeItems) - 1:
                break
            path = self.bg + '/recipe/grid/item_cell{}'.format(slot)
            self.PATH_TO_CONTAINER[path] = 'recipe_slot{}'.format(slot)
            self.containerSlots[path] = ItemSlot(self, path, path,False,False)
            self.containerSlots[path].setSlotItem(self.recipeItems[i*self.index])

    @ViewBinder.binding(ViewBinder.BF_ButtonClick, "#previousClick")
    def previousClick(self, args):
        touchState = args["TouchEvent"]
        if touchState == minecraftEnum.TouchEvent.TouchDown:
            if self.pagination.CanPrevious(self.index):
                self.index -= 1
            else:
                self.ShowItemText("没有上一页了!!!")

    @ViewBinder.binding(ViewBinder.BF_ButtonClick, "#nextClick")
    def nextClick(self, args):
        touchState = args["TouchEvent"]
        if touchState == minecraftEnum.TouchEvent.TouchDown:
            if self.pagination.CanNext(self.index):
                self.index += 1
            else:
                self.ShowItemText("没有下一页了!!!")

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

    def setSelectSlot(self, itemSlot):
        if self.isRecipeSlot(itemSlot):
            self.clientSystem.serverCaller("requestRecipeId", {"itemName": itemSlot.itemStack.identifier})
        else:
            if itemSlot.itemStack.isEmpty():
                return
            self.selectedSlot = itemSlot
            self.selectedSlot.setSelected(True)
            self.clickInterval = 10
        compFactory.CreateGame(levelId).AddTimer(0.2, self.clientSystem.serverCaller,"requestRecipe", {})
    
    def isRecipeSlot(self,fromSlot):
        #type: (ItemSlot) -> bool
        return "recipe_slot" in self.PATH_TO_CONTAINER.get(fromSlot.path,"")
    
    def isOutputSlot(self,fromSlot):
        #type: (ItemSlot) -> bool
        return fromSlot.path == self.bg+"/output"
    
    def clearTable(self,eventName,Data):
        self.clientSystem.serverCaller(eventName,Data)
        compFactory.CreateGame(levelId).AddTimer(0.01, lambda:self.clientSystem.serverCaller('clearTable',{}))

    def exchangeContainerSlot(self, fromSlot, toSlot):
        #type: (ItemSlot,ItemSlot) -> None
        """
        交换容器槽。
        :param fromSlot: 来源物品槽
        :param toSlot: 目标物品槽
        """
        if not (self.CanDrop(fromSlot) and self.CanDrop(toSlot)):
            return
        if not fromSlot.CanOutput():
            return
        if not toSlot.CanInput(fromSlot):
            return
        if self.isHoveredSlotValid():
            self.handleHoveredSlotExchange()
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

    def OnCursorItemCellUp(self, buttonPath):
        """
        鼠标抬起事件（左键）
        """
        itemComp = compFactory.CreateItem(levelId)  # 创建物品组件
        itemSlot = self.getSlotByPath(buttonPath)  # 获取目标物品槽
        if len(self.stockpilesData) > 1:
            self.handleStockpiles()
            return
        self.stockpilesData = {}
        self.stockpilesSlot = []
        if self.clickInterval >= -10 and self.upCell == itemSlot and not self.cursorSlot.itemStack.isEmpty() and self.cursorSlot.itemStack.count < self.cursorSlot.itemStack.getMaxStackSize(itemComp):
            self.reloadInventory()
            compFactory.CreateGame(levelId).AddTimer(0.2,self.CursorMergeItems,itemSlot)
            return
        if self.holdItemCount > 0 and self.holdSlot.index == itemSlot.index and self.CanMove(itemSlot):
            self.handleHoldItem(itemSlot)
            return
        else:
            self.holdSlot = None
            self.holdTime = None
            self.holdItemCount = 0
        if self.cursorSlot.itemStack.isEmpty(): #拿取
            if itemSlot.itemStack.isEmpty():
                return
            else:
                self.handleTakeItemFromSlot(itemSlot)
            if self.isOutputSlot(itemSlot):
                compFactory.CreateGame(levelId).AddTimer(0.01, lambda:self.clientSystem.serverCaller('clearTable',{}))
        elif itemSlot.itemStack.isEmpty(): #放入
            self.handlePutItemIntoSlot(itemSlot)
        elif itemSlot.itemStack == self.cursorSlot.itemStack and self.CanMove(itemSlot): #合并
            self.handleMergeItemsWithCursor(itemSlot)
    
    def OnCursorItemCellRightUp(self, buttonPath):
        """
        鼠标右键抬起事件
        """
        itemComp = compFactory.CreateItem(levelId)
        itemSlot = self.getSlotByPath(buttonPath)

        if (itemSlot.itemStack.getMaxStackSize(itemComp) > 1 and  #拿取
            not itemSlot.itemStack.isEmpty() and 
            self.CanMove(itemSlot) and 
            self.cursorSlot.itemStack.isEmpty()):
            self.handleTakeItemFromSlotRight(itemSlot)
            if self.isOutputSlot(itemSlot):
                compFactory.CreateGame(levelId).AddTimer(0.01, lambda:self.clientSystem.serverCaller('clearTable',{}))
        elif (itemSlot.itemStack.getMaxStackSize(itemComp) > 1 and  #合并
            not itemSlot.itemStack.isEmpty() and 
            not self.cursorSlot.itemStack.isEmpty()):
            self.handleMergeItemsWithCursorRight(itemSlot)
        elif itemSlot.itemStack.isEmpty() and not self.cursorSlot.itemStack.isEmpty(): #放入
            self.handlePutItemIntoSlotRight(itemSlot)