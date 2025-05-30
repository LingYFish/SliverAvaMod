from ...util.itemStack import ItemStack
from ...client.core.api import extraClientApi as clientApi
from ...client.core.api import ScreenNode,SliverClientSystem
from ...util.unicodeUtils import UnicodeConvert
from ...util import minecraftEnum
ViewBinder = clientApi.GetViewBinderCls()
from itemSlot import ItemSlot
from hoverButton import hoverButton
from itertools import chain
from flyingItem import FlyingItem
from cursorSlot import cursorSlot
from ...util.tools import extract_numbers
import weakref
import uuid
import json
import math
import copy

compFactory = clientApi.GetEngineCompFactory()
levelId = clientApi.GetLevelId()

class Inventory(ScreenNode):
    screenContent = "/variables_button_mappings_and_controls/safezone_screen_matrix/inner_matrix/safezone_screen_panel/root_screen_panel"
    screenBackGround = screenContent + "/screen_background"
    bg = screenBackGround + "/bg"
    inventoryPanel = bg + "/inventory_panel"
    hotbarGrid = inventoryPanel + "/hotbar_grid"
    inventoryGrid = inventoryPanel + "/inventory_grid"
    flyItemRenderer = screenContent + "/fly_item_renderer"
    PATH_TO_CONTAINER = {}
    minHoldTime = 10
    maxHoldTime = 20

    def __init__(self, namespace, name, param=None):
        """
        初始化物品栏。
        :param namespace: 命名空间
        :param name: 名称
        :param param: 参数字典，包含客户端系统、玩家ID等信息
        """
        ScreenNode.__init__(self, namespace, name, param)
        self.clientSystem = param["clientSystem"]  # type:SliverClientSystem
        self.playerId = param["playerId"]
        self.pos = param.get("pos", None)
        self.playerViewComp = compFactory.CreatePlayerView(levelId)
        self.cursorSlot = None #type:cursorSlot
        self.slotHight = None
        self.itemSlots = {}
        self.containerSlots = {} #type: dict[str|int,ItemSlot]
        self.buttonPathToIndex = {}
        self.selectedSlot = None
        self.holdSlot = None
        self.infoText = ""
        self.infoAlpha = 0.0
        self.clickInterval = 0
        self.holdTime = None
        self.holdItemCount = 0
        self.flyingItems = {}
        self.stockpilesData = {} #type: dict[str|int,ItemSlot]
        self.isTouchDown = False
        self.LastTouchedSlot = None
        self.hoveredSlot = [] #type: list[ItemSlot]
        self.stockpilesSlot = [] #type: list[ItemSlot]
        self.splitData = {}
        self.hoverText = ''
        self.inputMode = None
        self.hoverButton = None
        self.mouse = False
        self.gridLoaded = False
        self.upCell = None
        self.reude = 0
        self.KEY_SHIFT = False
        self.clientSystem.addListenEventUi(self,self.GameRenderTickEvent,eventName='GameRenderTickEvent')
        self.clientSystem.addListenEventUi(self,self.OnKeyPressInGame,eventName='OnKeyPressInGame')

    def OnKeyPressInGame(self,arsg):
        if arsg['key'] == minecraftEnum.KeyBoardType.KEY_LSHIFT:
            if arsg['isDown'] == 1:
                self.KEY_SHIFT = True
            else:
                self.KEY_SHIFT = False

    def GameRenderTickEvent(self,args):
        self.updateFlyingItems()

    def Create(self):
        """
        创建物品栏。
        """
        compFactory.CreateGame(levelId).AddTimer(0.05, self.loadAfter)

    def Destroy(self):
        """
        销毁物品栏。
        """
        self.clientSystem.screen = None

    def getInputMode(self):
        """
        :rtype: int
        """
        return self.playerViewComp.GetToggleOption(minecraftEnum.OptionId.INPUT_MODE)

    def Update(self):
        """
        更新物品栏。
        """
        self.updateMode()
        self.updateInfoAlpha()
        self.updateClickInterval()
        self.updateHoldTime()

    def updateMode(self):
        inputMode = self.getInputMode()
        if self.inputMode == 0: #鼠标
            self.mouse = True
        elif self.inputMode == 1: #触屏
            self.mouse = False
        self.inputMode = inputMode
        return

    def updateHightSlot(self):
        _ = "此功能已经废弃 问就是石山"

    def updateInfoAlpha(self):
        """
        更新物品信息透明度。
        """
        if self.infoAlpha > 0:
            self.infoAlpha -= 0.04

    def updateClickInterval(self):
        """
        更新点击间隔。
        """
        self.clickInterval -= 1

    def updateHoldTime(self):
        """
        更新按住时间。
        """
        if self.holdTime is not None:
            self.holdTime += 1
            self.setHoldSlot(self.holdSlot, self.holdTime)

    def updateFlyingItems(self):
        """
        更新飞行物品。
        """
        for gen, flyItem in list(self.flyingItems.items()):
            flyItem.update()
            if flyItem.Finished:
                flyItem.Finish()
                del self.flyingItems[gen]

    def setHoldSlot(self, holdSlot, holdTime):
        """
        设置按住的物品槽。
        :param holdSlot: 按住的物品槽
        :param holdTime: 按住时间
        """
        maxCount = float(holdSlot.itemStack.count)
        if holdTime > self.minHoldTime and len(self.hoveredSlot) < 2:
            holdTime -= self.minHoldTime
            self.holdItemCount = int(math.ceil(maxCount * min(holdTime, self.maxHoldTime) / 20.0))
            holdSlot.setProgressBar(True, 1.0 - (self.holdItemCount / maxCount))
        else:
            self.holdItemCount = 0
    
    def createFlyingItem(self, fromSlot, toSlot, runLater=lambda *args: None, *args):
        """
        创建飞行物品。
        :param fromSlot: 来源物品槽
        :param toSlot: 目标物品槽
        :param runLater: 延迟执行的函数
        :param args: 参数
        :return: 飞行物品
        """
        if fromSlot.itemStack.isEmpty():
            return
        gen = str(uuid.uuid4())
        newFlyItemName = "fly_item_renderer_%s" % gen
        fromSize = fromSlot.itemRenderer.GetSize()
        toSize = toSlot.itemRenderer.GetSize()
        offset = ((fromSize[0] - toSize[0]) * -0.5, (fromSize[1] - toSize[1]) * -0.5)
        itemDict = fromSlot.itemStack.toItemDict()
        if not self.Clone(self.flyItemRenderer, self.screenContent, newFlyItemName, True, True):
            return
        self.flyingItems[gen] = FlyingItem(self, "%s/%s" % (self.screenContent, newFlyItemName), gen, fromSlot, toSlot, offset, itemDict, runLater, *args)
        return self.flyingItems[gen]

    def LoadInventory(self):
        """
        加载物品栏。
        """
        self.itemSlots = {i: ItemSlot(self, self.hotbarGrid + "/item_cell%s" % str(i + 1), i) for i in range(9)}
        self.itemSlots.update({i + 9: ItemSlot(self, self.inventoryGrid + "/item_cell%s" % str(i + 1), i + 9) for i in range(27)})
        self.buttonPathToIndex = {self.hotbarGrid + "/item_cell%s" % str(i + 1): i for i in range(9)}
        self.buttonPathToIndex.update({self.inventoryGrid + "/item_cell%s" % str(i + 1): i + 9 for i in range(27)})

    def LoadContainer(self):
        """
        加载容器。
        """
        pass

    def loadAfter(self):
        """
        加载完成后执行的操作。
        """
        try:
            self.LoadInventory()
            self.LoadContainer()
            self.cursorSlot = cursorSlot(self,"{}/cursor_renderer".format(self.screenContent),self.playerId)
            self.gridLoaded = True
            self.reloadInventory()
        except Exception as ExcptionInfo:
            print(ExcptionInfo)
            if not self.gridLoaded:
                compFactory.CreateGame(levelId).AddTimer(0.05, self.loadAfter)

    def reloadInventory(self):
        """
        重新加载物品栏。
        """
        itemComp = compFactory.CreateItem(self.playerId)
        playerAllItem = itemComp.GetPlayerAllItems(minecraftEnum.ItemPosType.INVENTORY, True)
        for i in range(36):
            self.itemSlots[i].setSlotItem(playerAllItem[i])

    def IsContainerSlot(self, itemSlot):
        """
        判断是否为容器槽。
        :param itemSlot: 物品槽
        :return: 是否为容器槽
        """
        return itemSlot.path in self.containerSlots

    def getSlotByPath(self, slotPath):
        #type: (str) -> ItemSlot
        """
        根据路径获取物品槽。
        :param slotPath: 物品槽路径
        :return: 物品槽
        """
        path = slotPath[slotPath.find('/'):slotPath.rfind('/')]
        slotId = self.buttonPathToIndex.get(path)
        return self.itemSlots.get(slotId) if isinstance(slotId, int) else self.containerSlots.get(path)

    def CanDrop(self, itemSlot):
        #type: (ItemSlot) -> bool
        """
        判断是否可以丢弃物品。
        :param itemStack: 物品堆
        :return: 是否可以丢弃
        """
        itemStack = itemSlot.itemStack
        return (itemStack.tag.get("minecraft:item_lock", {}).get("__value__", 0) == 0) and itemSlot.canOutput

    def CanMove(self, itemSlot):
        #type: (ItemSlot) -> bool
        """
        判断是否可以移动物品。
        :param itemStack: 物品堆
        :return: 是否可以移动
        """
        itemStack = itemSlot.itemStack
        return (not itemStack.tag.get("minecraft:item_lock", {}).get("__value__", 0) == 1) and itemSlot.canOutput
    
    def CanMoveStack(self, itemStack):
        #type: (ItemStack) -> bool
        """
        判断是否可以移动物品。
        :param itemStack: 物品堆
        :return: 是否可以移动
        """
        return not itemStack.tag.get("minecraft:item_lock", {}).get("__value__", 0) == 1

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
        #type: (ItemSlot,ItemSlot) -> None
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
                    if fromSlot.CanInput(toSlot):
                        self.createFlyingItem(fromSlot, toSlot, self.clientSystem.serverCaller, "OnExchangeItemFromContainer", {"invSlot": toSlot.index, "containerSlot": fromSlot.index})
                        self.createFlyingItem(toSlot, fromSlot)
                        fromSlot.setHide(True)
                        toSlot.setHide(True)

    def moveItemInContainer(self, fromSlot, toSlot):
        #type: (ItemSlot,ItemSlot) -> None
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
        #type: (ItemSlot,ItemSlot) -> None
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

    def exchangeInventorySlot(self, fromSlot, toSlot):
        #type: (ItemSlot,ItemSlot) -> None
        """
        交换物品栏槽。
        :param fromSlot: 来源物品槽
        :param toSlot: 目标物品槽
        """
        if not self.canExchangeSlots(fromSlot, toSlot):
            return

        if fromSlot == self.holdSlot:
            self.handleHoldSlotExchange(fromSlot, toSlot)
        elif self.isHoveredSlotValid():
            self.handleHoveredSlotExchange()
        else:
            self.handleNormalExchange(fromSlot, toSlot)

    def canExchangeSlots(self, fromSlot, toSlot):
        #type: (ItemSlot,ItemSlot) -> None
        """
        判断是否可以交换两个物品槽。
        :param fromSlot: 来源物品槽
        :param toSlot: 目标物品槽
        :return: 是否可以交换
        """
        return self.CanMove(fromSlot) and self.CanMove(toSlot)

    def handleHoldSlotExchange(self, fromSlot, toSlot):
        #type: (ItemSlot,ItemSlot) -> None
        """
        处理按住物品槽的交换逻辑。
        :param fromSlot: 来源物品槽
        :param toSlot: 目标物品槽
        """
        if toSlot.itemStack.isEmpty():
            self.createFlyingItem(fromSlot, toSlot, self.clientSystem.serverCaller, "OnSplitItemToSlotEvent", {"fromSlot": fromSlot.index, "toSlot": toSlot.index, "count": self.holdItemCount})
            if not (self.holdItemCount < fromSlot.itemStack.count):
                fromSlot.setHide(True)
        else:
            self.handleMergeItems(fromSlot, toSlot)

    def handleHoveredSlotExchange(self):
        """
        处理悬停物品槽的交换逻辑。
        :param fromSlot: 来源物品槽
        :param toSlot: 目标物品槽
        """
        for slot, data in self.splitData.items():
            if isinstance(slot.index, int):
                self.clientSystem.serverCaller("addCursorInvItem", {
                    "toSlot": slot.index,
                    "fromData": data
                })
            else:
                self.addCursorContainerItem(slot.index, data)
        if isinstance(self.selectedSlot.index, int):
            self.clientSystem.serverCaller("addCursorInvItem", {
                "toSlot": self.selectedSlot.index,
                "fromData": {"count":-self.reude}
            })
        else:
            self.addCursorContainerItem(self.selectedSlot.index, {"count":-self.reude})
        self.splitData = {}
        self.hoveredSlot = []

    def handleNormalExchange(self, fromSlot, toSlot):
        #type: (ItemSlot,ItemSlot) -> None
        """
        处理普通物品槽的交换逻辑。
        :param fromSlot: 来源物品槽
        :param toSlot: 目标物品槽
        """
        if fromSlot.itemStack == toSlot.itemStack:
            self.handleMergeItems(fromSlot, toSlot)
        else:
            self.handleExchangeItems(fromSlot, toSlot)

    def handleMergeItems(self, fromSlot, toSlot):
        #type: (ItemSlot,ItemSlot) -> None
        """
        处理物品合并逻辑。
        :param fromSlot: 来源物品槽
        :param toSlot: 目标物品槽
        """
        itemComp = compFactory.CreateItem(levelId)
        maxStackSize = toSlot.itemStack.getMaxStackSize(itemComp)
        mergeCount = min(maxStackSize - toSlot.itemStack.count, fromSlot.itemStack.count)
        if mergeCount > 0:
            self.createFlyingItem(fromSlot, toSlot, self.clientSystem.serverCaller, "OnMergeSlotEvent", {"from": fromSlot.index, "to": toSlot.index, "mergeCount": mergeCount})

    def handleExchangeItems(self, fromSlot, toSlot):
        #type: (ItemSlot,ItemSlot) -> None
        """
        处理物品交换逻辑。
        :param fromSlot: 来源物品槽
        :param toSlot: 目标物品槽
        """
        if toSlot.itemStack.isEmpty():
            self.createFlyingItem(fromSlot, toSlot, self.clientSystem.serverCaller, "OnExchangeSlotEvent", {"from": fromSlot.index, "to": toSlot.index})
            fromSlot.setHide(True)
        else:
            self.createFlyingItem(fromSlot, toSlot, self.clientSystem.serverCaller, "OnExchangeSlotEvent", {"from": fromSlot.index, "to": toSlot.index})
            self.createFlyingItem(toSlot, fromSlot)
            toSlot.setHide(True)
            fromSlot.setHide(True)

    def isHoveredSlotValid(self):
        """
        判断悬停的物品槽是否有效。
        :return: 是否有效
        """
        return len(self.hoveredSlot) > 0

    def OnItemCellTouchUp(self, buttonPath):
        """
        物品槽触摸抬起事件。
        :param buttonPath: 按钮路径
        """
        itemSlot = self.getSlotByPath(buttonPath)
        if self.selectedSlot:
            self.exchangeSlots(self.selectedSlot, itemSlot)
            self.resetSelectedSlot()
        else:
            self.setSelectSlot(itemSlot)
        self.resetTouchState()

    def exchangeSlots(self, fromSlot, toSlot):
        #type: (ItemSlot,ItemSlot) -> None
        """
        交换两个物品槽。
        :param fromSlot: 来源物品槽
        :param toSlot: 目标物品槽
        """
        if isinstance(fromSlot.index, int) and isinstance(toSlot.index, int):
            self.exchangeInventorySlot(fromSlot, toSlot)
        else:
            self.exchangeContainerSlot(fromSlot, toSlot)

    def resetSelectedSlot(self):
        """
        重置选中的物品槽。
        """
        if self.selectedSlot:
            self.selectedSlot.setProgressBar(False, 0.0)
            self.selectedSlot.setSelected(False)
        self.selectedSlot = None

    def resetTouchState(self):
        """
        重置触摸状态。
        """
        self.LastTouchedSlot = None
        self.holdTime = None
        if self.holdItemCount <= 0:
            self.holdSlot = None
        if self.isHoveredSlotValid():
            self.handleHoveredSlotExchange()
        self.hoveredSlot = []
        self.splitData.clear()

    def setSelectSlot(self, itemSlot):
        #type: (ItemSlot) -> None
        """
        设置选中的物品槽。
        :param itemSlot: 物品槽
        """
        if itemSlot.itemStack.isEmpty():
            return
        self.selectedSlot = itemSlot
        self.selectedSlot.setSelected(True)
        self.clickInterval = 10

    def ShowItemText(self, text):
        """
        显示物品信息文本。
        :param text: 文本
        """
        self.infoText = text
        self.infoAlpha = 2.0

    def OnItemCellTouchDown(self, buttonPath):
        """
        物品槽触摸按下事件。
        :param buttonPath: 按钮路径
        """
        itemSlot = self.getSlotByPath(buttonPath)
        self.LastTouchedSlot = itemSlot
        if self.selectedSlot and self.clickInterval > 0 and self.selectedSlot.index == itemSlot.index:
            self.mergeItems()
        elif not self.selectedSlot:
            self.holdTime = 0
            self.holdSlot = itemSlot
        self.showItemText(itemSlot)

    def mergeItems(self):
        """
        合并物品。
        """
        itemComp = compFactory.CreateItem(levelId)
        maxStackSize = self.selectedSlot.itemStack.getMaxStackSize(itemComp)
        maxMergeCount = maxStackSize - self.selectedSlot.itemStack.count
        mergedCount = 0
        mergeItemData = {}
        fullItemData = {}
        if not isinstance(self.selectedSlot.index,int):
            return
        for i in range(35, -1, -1):
            if mergedCount >= maxMergeCount:
                break
            if i != self.selectedSlot.index:
                newItemslot = self.itemSlots[i]
                if newItemslot.itemStack == self.selectedSlot.itemStack:
                    if newItemslot.itemStack.count == maxStackSize:
                        fullItemData[i] = newItemslot
                    else:
                        needMergeCount = min(maxMergeCount - mergedCount, newItemslot.itemStack.count)
                        self.createFlyingItem(newItemslot, self.selectedSlot)
                        mergeItemData[i] = newItemslot.itemStack.count - needMergeCount
                        mergedCount += needMergeCount
        for index, slot in fullItemData.items():
            if mergedCount >= maxMergeCount:
                break
            needMergeCount = min(maxMergeCount - mergedCount, slot.itemStack.count)
            self.createFlyingItem(slot, self.selectedSlot)
            mergeItemData[index] = slot.itemStack.count - needMergeCount
            mergedCount += needMergeCount
        mergeItemData[self.selectedSlot.index] = self.selectedSlot.itemStack.count + mergedCount
        self.resetSelectedSlot()
        self.clientSystem.serverCaller("OnMergeAllSlotEvent", {"mergeItemData": mergeItemData})

    def showItemText(self, itemSlot):
        #type: (ItemSlot) -> None
        """
        显示物品信息文本。
        :param itemSlot: 物品槽
        """
        if itemSlot.itemStack.isEmpty():
            return
        itemName = itemSlot.itemStack.identifier
        auxValue = itemSlot.itemStack.data
        userData = itemSlot.itemStack.tag
        text = compFactory.CreateItem(self.playerId).GetItemFormattedHoverText(itemName, auxValue, False, userData)
        text = self.replaceSpecialCharacters(text)
        if self.mouse == False:
            self.ShowItemText(text)

    def showItemhoverText(self, itemSlot):
        #type: (ItemSlot) -> None
        if itemSlot.itemStack.isEmpty():
            return
        itemName = itemSlot.itemStack.identifier
        auxValue = itemSlot.itemStack.data
        userData = itemSlot.itemStack.tag
        text = compFactory.CreateItem(self.playerId).GetItemFormattedHoverText(itemName, auxValue, False, userData)
        text = self.replaceSpecialCharacters(text)
        self.hoverText = text

    def replaceSpecialCharacters(self, text):
        """
        替换特殊字符。
        :param text: 文本
        :return: 替换后的文本
        """
        text = text.replace(':hollow_star:', '')
        text = text.replace(':solid_star:', '')
        return text

    def splitItems(self):
        """
        分割物品。
        """
        if not self.mouse:
            total = self.selectedSlot.itemStack.count
            slots = list(self.hoveredSlot)
            if total < len(slots):
                return
            splitCount = total // len(slots)
            itemName = self.selectedSlot.itemStack.identifier
            auxValue = self.selectedSlot.itemStack.data
            isEnchanted = len(self.selectedSlot.itemStack.getEnchantData()) > 0
            userData = self.selectedSlot.itemStack.tag
            reude = 0
            for slot in slots:
                reude += splitCount
                self.splitData[slot] = ItemStack(newItemName=itemName, newAuxValue=auxValue, count=splitCount, userData=userData).toItemDict() if slot.itemStack.isEmpty() else {"count":splitCount}
                slot.setShowItem(itemName=itemName,auxValue=auxValue,isEnchanted=isEnchanted,userData=userData)
                slot.setShowCount(splitCount)
            self.reude = reude
            if total - self.reude <= 0:
                all_count = 0
                for slot,itemDict in self.splitData.items():
                    all_count += itemDict['count']
                if all_count < total:
                    self.splitData[list(self.splitData.keys())[-1]]['count'] += total - all_count
            else:
                all_count = 0
                for slot,itemDict in self.splitData.items():
                    all_count += itemDict['count']
                self.reude = all_count
            self.selectedSlot.setShowCount(total-self.reude)
        else:
            total = self.cursorSlot.itemStack.count
            slots = self.stockpilesSlot #type: list[ItemSlot]
            if total < len(slots):
                return
            splitCount = total // len(slots)
            itemName = self.cursorSlot.itemStack.identifier
            auxValue = self.cursorSlot.itemStack.data
            isEnchanted = len(self.cursorSlot.itemStack.getEnchantData()) > 0
            userData = self.cursorSlot.itemStack.tag
            reude = 0
            for slot in slots:
                reude += splitCount
                self.stockpilesData[slot] = ItemStack(newItemName=itemName, newAuxValue=auxValue, count=splitCount, userData=userData).toItemDict() if slot.itemStack.isEmpty() else {"count":splitCount}
                slot.setShowItem(itemName=itemName,auxValue=auxValue,isEnchanted=isEnchanted,userData=userData)
                slot.setShowCount(splitCount)
            self.reude = reude
            if total - self.reude <= 0:
                all_count = 0
                for slot,itemDict in self.stockpilesData.items():
                    all_count += itemDict['count']
                if all_count < total:
                    self.reude -= total - all_count
            else:
                all_count = 0
                for slot,itemDict in self.stockpilesData.items():
                    all_count += itemDict['count']
                self.reude = all_count
            self.cursorSlot.setShowCount(total-self.reude)

    def OnItemCellHovered(self, buttonPath):
        """
        物品槽悬停事件。
        :param buttonPath: 按钮路径
        """
        if self.isTouchDown and self.selectedSlot:
            slot = self.getSlotByPath(buttonPath)
            if slot.index != self.selectedSlot.index and (slot.itemStack.isEmpty() or slot.itemStack == self.selectedSlot.itemStack) and (not self.holdItemCount > 0) and slot.index not in self.hoveredSlot and self.CanMove(slot):
                self.hoveredSlot.append(slot)
                self.splitItems()
        elif not self.isTouchDown and not self.selectedSlot:
            slot = self.getSlotByPath(buttonPath)
            self.slotHight = slot

    def OnCloseButtonClick(self):
        """
        关闭按钮点击事件。
        """
        if not self.cursorSlot.itemStack.isEmpty():
            self.dropItems()
        self.SetRemove()

    def OnDropButtonClick(self):
        """
        丢弃按钮点击事件。
        """
        if not self.mouse:
            if self.selectedSlot:
                self.dropItems()
        elif not self.cursorSlot.itemStack.isEmpty():
            self.dropItems()

    def dropItems(self):
        """
        丢弃物品。
        """
        if not self.mouse:
            if isinstance(self.selectedSlot.index, int):
                if self.holdSlot and isinstance(self.holdSlot.index, int):
                    if self.CanDrop(self.holdSlot):
                        self.clientSystem.serverCaller("OnDrop", {"slotId": self.holdSlot.index, "count": self.holdItemCount})
                        self.holdSlot = None
                else:
                    if self.CanDrop(self.selectedSlot):
                        self.clientSystem.serverCaller("OnDropAll", {"slotId": self.selectedSlot.index})
        else:
            self.clientSystem.serverCaller("DropCursorItem", {"itemDict": self.cursorSlot.itemStack.toItemDict()})
            self.cursorSlot.itemStack = ItemStack()
            self.cursorSlot.setSlotItem(ItemStack().toItemDict())
        self.resetSelectedSlot()

    def addCursorContainerItem(self,toSlot,fromData):
        #type: (ItemSlot,dict) -> None
        self.clientSystem.serverCaller("addCursorContainerItem",{
            "toSlot":toSlot,
            "fromData":fromData
        })

    def takeCursorContainerItem(self,toSlot):
        #type: (ItemSlot) -> None
        self.clientSystem.serverCaller("takeCursorContainerItem",{
            "containerSlot":toSlot
        })

    def CursorMergeItems(self,itemSlot):
        #type:(ItemSlot) -> None
        """
        合并物品。
        """
        itemComp = compFactory.CreateItem(levelId)
        maxStackSize = self.cursorSlot.itemStack.getMaxStackSize(itemComp)
        if not maxStackSize > 1:
            return
        if not itemSlot.itemStack.isEmpty():
            return
        maxMergeCount = maxStackSize - self.cursorSlot.itemStack.count
        mergeItemData = {}
        for slotid in range(36):
            itemDict = compFactory.CreateItem(self.playerId).GetPlayerItem(minecraftEnum.ItemPosType.INVENTORY, slotid, True)
            if maxMergeCount == 0:
                break
            if itemDict:
                slotStack = ItemStack(**itemDict)
                if slotStack != self.cursorSlot.itemStack or not (self.CanMoveStack(slotStack)):
                    continue
                if slotStack.count < maxMergeCount:
                    mergeItemData[slotid] = {"count":-slotStack.count}
                    maxMergeCount -= slotStack.count
                elif slotStack.count == maxMergeCount:
                    mergeItemData[slotid] = {"count":-slotStack.count}
                    maxMergeCount -= slotStack.count
                elif slotStack.count > maxMergeCount:
                    mergeItemData[slotid] = {"count":-maxMergeCount}
                    maxMergeCount = 0
        for i,newItemslot in self.containerSlots.items():
            if maxMergeCount == 0:
                break
            if newItemslot.itemStack != self.cursorSlot.itemStack or not self.CanMove(newItemslot):
                continue
            if newItemslot.itemStack.count < maxMergeCount:
                mergeItemData[i] = {"count":-newItemslot.itemStack.count}
                maxMergeCount -= newItemslot.itemStack.count
            elif newItemslot.itemStack.count == maxMergeCount:
                mergeItemData[i] = {"count":-newItemslot.itemStack.count}
                maxMergeCount -= newItemslot.itemStack.count
            elif newItemslot.itemStack.count > maxMergeCount:
                mergeItemData[i] = {"count":-maxMergeCount}
                maxMergeCount = 0
        for index,data in mergeItemData.items():
            if isinstance(index,int):
                self.clientSystem.serverCaller("addCursorInvItem",{
                    "toSlot":index,
                    "fromData":data
                })
            else:
                self.addCursorContainerItem(self.PATH_TO_CONTAINER[index],data)
        self.cursorSlot.itemStack.count = maxStackSize - maxMergeCount
        self.cursorSlot.setSlotItem(self.cursorSlot.itemStack.toItemDict())

    def OnCursorItemCellDown(self,buttonPath):
        itemComp = compFactory.CreateItem(levelId)
        itemSlot = self.getSlotByPath(buttonPath)
        if self.cursorSlot.itemStack.isEmpty() and itemSlot.itemStack.getMaxStackSize(itemComp) > 1 and not itemSlot.itemStack.isEmpty() and self.CanMove(itemSlot):
            self.holdSlot = itemSlot
            self.holdTime = 0
        
    def OnCursorCellHovered(self,buttonPath):
        itemComp = compFactory.CreateItem(levelId)
        itemSlot = self.getSlotByPath(buttonPath)
        self.upCell = itemSlot
        if (itemSlot.itemStack.isEmpty() or itemSlot.itemStack == self.cursorSlot.itemStack) and self.holdItemCount <= 0 and itemSlot.index not in self.stockpilesSlot and not self.cursorSlot.itemStack.isEmpty() and self.isTouchDown and self.CanMove(itemSlot):
            self.stockpilesSlot.append(itemSlot)
            self.splitItems()

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
        elif itemSlot.itemStack.isEmpty(): #放入
            self.handlePutItemIntoSlot(itemSlot)
        elif itemSlot.itemStack == self.cursorSlot.itemStack and self.CanMove(itemSlot): #合并
            self.handleMergeItemsWithCursor(itemSlot)

    def handlePutItemFlyToSlot(self,itemSlot):
        #type: (ItemSlot) -> None
        """
        处理快速放置
        """
        itemComp = compFactory.CreateItem(levelId)
        print (itemSlot)
        print (self.CanMove(itemSlot))
        if self.CanMove(itemSlot):
            if isinstance(itemSlot.index,int):
                for slot_index in sorted(self.containerSlots.keys(), key=extract_numbers):
                    data = self.containerSlots[slot_index]
                    maxStackSize = data.itemStack.getMaxStackSize(itemComp)
                    if data.CanInput(itemSlot) and data.itemStack == itemSlot.itemStack and data.itemStack.count < maxStackSize and self.CanMove(data) and not data.itemStack.isEmpty():
                        mergeCount = min(maxStackSize - data.itemStack.count,itemSlot.itemStack.count)
                        def _():
                            self.addCursorContainerItem(self.PATH_TO_CONTAINER[slot_index],{"count":+mergeCount})
                            self.clientSystem.serverCaller("addCursorInvItem", {
                                "toSlot": itemSlot.index,
                                "fromData": {"count":-mergeCount}
                            })
                        self.createFlyingItem(itemSlot,data,_)
                        return
                for slot_index in sorted(self.containerSlots.keys(), key=extract_numbers):
                    data = self.containerSlots[slot_index]
                    maxStackSize = data.itemStack.getMaxStackSize(itemComp)
                    if data.CanInput(itemSlot) and data.itemStack.isEmpty():
                        mergeCount = itemSlot.itemStack.count
                        def _():
                            self.addCursorContainerItem(self.PATH_TO_CONTAINER[slot_index],itemSlot.itemStack.toItemDict())
                            self.clientSystem.serverCaller("addCursorInvItem", {
                                "toSlot": itemSlot.index,
                                "fromData": {"count":-mergeCount}
                            })
                        self.createFlyingItem(itemSlot,data,_)
                        return
            else:
                for slot_index in sorted(self.itemSlots.keys()):
                    data = self.itemSlots[slot_index]
                    maxStackSize = data.itemStack.getMaxStackSize(itemComp)
                    if data.CanInput(itemSlot) and data.itemStack == itemSlot.itemStack and data.itemStack.count < maxStackSize and self.CanMove(data) and not data.itemStack.isEmpty():
                        mergeCount = min(maxStackSize - data.itemStack.count,itemSlot.itemStack.count)
                        def _():
                            self.addCursorContainerItem(itemSlot.index,{"count":-mergeCount})
                            self.clientSystem.serverCaller("addCursorInvItem", {
                                "toSlot": data.index,
                                "fromData": {"count":+mergeCount}
                            })
                        self.createFlyingItem(itemSlot,data,_)
                        return
                for slot_index in sorted(self.itemSlots.keys()):
                    data = self.itemSlots[slot_index]
                    if data.CanInput(itemSlot) and data.itemStack.isEmpty():
                        mergeCount = itemSlot.itemStack.count
                        def _():
                            self.addCursorContainerItem(itemSlot.index,{"count":-mergeCount})
                            self.clientSystem.serverCaller("addCursorInvItem", {
                                "toSlot": data.index,
                                "fromData": itemSlot.itemStack.toItemDict()
                            })
                        self.createFlyingItem(itemSlot,data,_)
                        return

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
        elif (itemSlot.itemStack.getMaxStackSize(itemComp) > 1 and  #合并
            not itemSlot.itemStack.isEmpty() and 
            not self.cursorSlot.itemStack.isEmpty()):
            self.handleMergeItemsWithCursorRight(itemSlot)
        elif itemSlot.itemStack.isEmpty() and not self.cursorSlot.itemStack.isEmpty(): #放入
            self.handlePutItemIntoSlotRight(itemSlot)

    def handleStockpiles(self):
        """
        处理库存堆
        """
        for slot, data in self.stockpilesData.items():
            if isinstance(slot.index, int):
                self.clientSystem.serverCaller("addCursorInvItem", {
                    "toSlot": slot.index,
                    "fromData": data
                })
            else:
                self.addCursorContainerItem(slot.index, data)
        self.cursorSlot.itemStack.count -= self.reude
        if self.cursorSlot.itemStack.count <= 0:
            self.cursorSlot.itemStack = ItemStack()
            self.cursorSlot.setSlotItem(ItemStack().toItemDict())
        self.stockpilesData = {}
        self.stockpilesSlot = []

    def handleHoldItem(self, itemSlot):
        #type: (ItemSlot) -> None
        """
        处理按住物品
        """
        self.clickInterval = 10
        self.cursorSlot.setHide(False)
        if isinstance(itemSlot.index, int):
            self.clientSystem.serverCaller("addCursorInvItem", {
                "toSlot": itemSlot.index,
                "fromData": {"count": -self.holdItemCount}
            })
            itemSlot.onButtonHoveInCallback(None)
        else:
            self.addCursorContainerItem(itemSlot.index, {"count": -self.holdItemCount})
            itemSlot.onButtonHoveInCallback(None)
        self.cursorSlot.setHide(False)
        self.cursorSlot.itemStack = ItemStack(**itemSlot.itemStack.toItemDict())
        self.cursorSlot.itemStack.count = self.holdItemCount
        itemSlot.itemStack.count -= self.holdItemCount
        self.cursorSlot.setSlotItem(self.cursorSlot.itemStack.toItemDict())
        itemSlot.setSlotItem(itemSlot.itemStack.toItemDict())
        self.holdTime = None
        self.holdSlot = None
        self.holdTime = None
        self.holdItemCount = 0

    def handleTakeItemFromSlot(self, itemSlot):
        #type: (ItemSlot) -> None
        """
        处理从物品槽拿取物品（左键）
        """
        if itemSlot.CanOutput():
            self.cursorSlot.setHide(False)
            self.cursorSlot.itemStack = itemSlot.itemStack
            self.cursorSlot.setSlotItem(self.cursorSlot.itemStack.toItemDict())
            itemSlot.setHide(True)
            if isinstance(itemSlot.index, int):
                self.clientSystem.serverCaller("addCursorInvItem", {
                    "toSlot": itemSlot.index,
                    "fromData": {"count": -itemSlot.itemStack.count}
                })
            else:
                self.addCursorContainerItem(itemSlot.index, {'count': -itemSlot.itemStack.count})

    def handlePutItemIntoSlot(self, itemSlot):
        #type: (ItemSlot) -> None
        """
        处理将光标物品放入物品槽（左键）
        """
        self.clickInterval = 10
        if itemSlot.CanInput(self.cursorSlot):
            if isinstance(itemSlot.index, int):
                self.clientSystem.serverCaller("addCursorInvItem", {
                    "toSlot": itemSlot.index,
                    "fromData": self.cursorSlot.itemStack.toItemDict()
                })
                itemSlot.setSlotItem(self.cursorSlot.itemStack.toItemDict())
                self.cursorSlot.itemStack = ItemStack()
                self.cursorSlot.setSlotItem(self.cursorSlot.itemStack.toItemDict())
                itemSlot.onButtonHoveInCallback(None)
            else:
                self.addCursorContainerItem(itemSlot.index, self.cursorSlot.itemStack.toItemDict())
                itemSlot.setSlotItem(self.cursorSlot.itemStack.toItemDict())
                self.cursorSlot.itemStack = ItemStack()
                self.cursorSlot.setSlotItem(self.cursorSlot.itemStack.toItemDict())
                itemSlot.onButtonHoveInCallback(None)

    def handleMergeItemsWithCursor(self, itemSlot):
        #type: (ItemSlot) -> None
        """
        处理光标物品与物品槽物品合并（左键）
        """
        maxStackSize = itemSlot.itemStack.getMaxStackSize(compFactory.CreateItem(levelId))
        mergeCount = min(maxStackSize - itemSlot.itemStack.count, self.cursorSlot.itemStack.count)
        if itemSlot.CanInput(self.cursorSlot):
            if mergeCount > 0:
                if isinstance(itemSlot.index, int):
                    self.clientSystem.serverCaller("addCursorInvItem", {
                        "toSlot": itemSlot.index,
                        "fromData": {"count": mergeCount}
                    })
                    itemSlot.itemStack.count += mergeCount
                    itemSlot.setSlotItem(itemSlot.itemStack.toItemDict())
                    self.cursorSlot.itemStack.count -= mergeCount
                    self.cursorSlot.setSlotItem(self.cursorSlot.itemStack.toItemDict())
                    itemSlot.onButtonHoveInCallback(None)
                else:
                    self.addCursorContainerItem(itemSlot.index, {"count": mergeCount})
                    itemSlot.itemStack.count += mergeCount
                    itemSlot.setSlotItem(itemSlot.itemStack.toItemDict())
                    self.cursorSlot.itemStack.count -= mergeCount
                    self.cursorSlot.setSlotItem(self.cursorSlot.itemStack.toItemDict())
                    itemSlot.onButtonHoveInCallback(None)

    def handleTakeItemFromSlotRight(self, itemSlot):
        #type: (ItemSlot) -> None
        """
        处理从物品槽拿取物品（右键）
        """
        self.cursorSlot.setHide(False)
        if itemSlot.CanInput(self.cursorSlot):
            if itemSlot.itemStack.count == 1:
                self.cursorSlot.itemStack = itemSlot.itemStack
                self.cursorSlot.setSlotItem(itemSlot.itemStack.toItemDict())
                itemSlot.setSlotItem(ItemStack().toItemDict())
                if isinstance(itemSlot.index, int):
                    self.clientSystem.serverCaller("addCursorInvItem", {
                        "toSlot": itemSlot.index,
                        "fromData": {"count": -1}
                    })
                else:
                    self.addCursorContainerItem(itemSlot.index, {'count': -1})
            else:
                splitCount = itemSlot.itemStack.count // 2
                self.cursorSlot.itemStack = itemSlot.itemStack.clone()
                self.cursorSlot.itemStack.count = splitCount
                itemSlot.itemStack.count -= splitCount
                itemSlot.setSlotItem(itemSlot.itemStack.toItemDict())
                self.cursorSlot.setSlotItem(self.cursorSlot.itemStack.toItemDict())
                if isinstance(itemSlot.index, int):
                    self.clientSystem.serverCaller("addCursorInvItem", {
                        "toSlot": itemSlot.index,
                        "fromData": {"count": -splitCount}
                    })
                else:
                    self.addCursorContainerItem(itemSlot.index, {'count': -splitCount})

    def handleMergeItemsWithCursorRight(self, itemSlot):
        #type: (ItemSlot) -> None
        """
        处理光标物品与物品槽物品合并（右键）
        """
        if itemSlot.CanInput(self.cursorSlot):
            if itemSlot.itemStack == self.cursorSlot.itemStack and itemSlot.itemStack.count < itemSlot.itemStack.getMaxStackSize(compFactory.CreateItem(levelId)):
                self.cursorSlot.itemStack.count -= 1
                itemSlot.itemStack.count += 1
                itemSlot.setSlotItem(itemSlot.itemStack.toItemDict())
                self.cursorSlot.setSlotItem(self.cursorSlot.itemStack.toItemDict())
                if isinstance(itemSlot.index, int):
                    self.clientSystem.serverCaller("addCursorInvItem", {
                        "toSlot": itemSlot.index,
                        "fromData": {"count": 1}
                    })
                else:
                    self.addCursorContainerItem(itemSlot.index, {'count': 1})

    def handlePutItemIntoSlotRight(self, itemSlot):
        #type: (ItemSlot) -> None
        """
        处理将光标物品放入物品槽（右键）
        """
        if itemSlot.CanInput(self.cursorSlot):
            itemSlot.itemStack = self.cursorSlot.itemStack.clone()
            itemSlot.itemStack.count = 1
            self.cursorSlot.itemStack.count -= 1
            itemSlot.setSlotItem(itemSlot.itemStack.toItemDict())
            self.cursorSlot.setSlotItem(self.cursorSlot.itemStack.toItemDict())
            if isinstance(itemSlot.index, int):
                self.clientSystem.serverCaller("addCursorInvItem", {
                    "toSlot": itemSlot.index,
                    "fromData": itemSlot.itemStack.toItemDict()
                })
            else:
                self.addCursorContainerItem(itemSlot.index, itemSlot.itemStack.toItemDict())

    @ViewBinder.binding(ViewBinder.BF_BindString, "#ItemInfo")
    def itemInfoText(self):
        """
        绑定物品信息文本。
        """
        return self.infoText

    @ViewBinder.binding(ViewBinder.BF_BindString, "#HoveredText")
    def HoveredText(self):
        """
        绑定物品信息文本。
        """
        return self.hoverText

    @ViewBinder.binding(ViewBinder.BF_BindFloat, "#ItemInfoAlpha")
    def itemInfoAlpha(self):
        """
        绑定物品信息透明度。
        """
        return min(self.infoAlpha, 1.0)

    @ViewBinder.binding(ViewBinder.BF_ButtonClick, "#CloseButtonClick")
    def closeButtonClick(self, args):
        """
        关闭按钮点击事件绑定。
        :param args: 参数
        """
        touchState = args["TouchEvent"]
        if touchState == minecraftEnum.TouchEvent.TouchDown:
            self.OnCloseButtonClick()

    @ViewBinder.binding(ViewBinder.BF_ButtonClick, "#ItemCellClick")
    def itemCellClick(self, args):
        """
        物品槽点击事件绑定。
        :param args: 参数
        """
        touchState = args["TouchEvent"]
        if not self.mouse:
            if touchState == minecraftEnum.TouchEvent.TouchDown:
                self.isTouchDown = True
                self.OnItemCellTouchDown(args["ButtonPath"])
            elif touchState == minecraftEnum.TouchEvent.TouchUp:
                self.isTouchDown = False
                self.OnItemCellTouchUp(args["ButtonPath"])
        else:
            if touchState == minecraftEnum.TouchEvent.TouchDown:
                self.isTouchDown = True
                self.OnCursorItemCellDown(args['ButtonPath'])
            elif touchState == minecraftEnum.TouchEvent.TouchUp:
                self.isTouchDown = False
                self.OnCursorItemCellUp(args["ButtonPath"])

    @ViewBinder.binding(ViewBinder.BF_ButtonClick, "#sortAllClick")
    def sortAllClick(self, args):
        """
        整理点击事件绑定。
        :param args: 参数
        """
        touchState = args["TouchEvent"]
        if touchState == minecraftEnum.TouchEvent.TouchUp:
            slots = []
            for path,slot in self.containerSlots.items():
                slotId = self.PATH_TO_CONTAINER[path]
                if self.CanMove(slot):
                    slots.append(slotId)
            if len(slots) > 0:
                self.clientSystem.serverCaller('sortAllItem',{'slots':map(str,slots)})

    @ViewBinder.binding(ViewBinder.BF_ButtonClick, "#moveOutClick")
    def moveOutClick(self, args):
        """
        一键移出点击事件绑定。
        :param args: 参数
        """
        touchState = args["TouchEvent"]
        if touchState == minecraftEnum.TouchEvent.TouchUp:
            pass

    @ViewBinder.binding(ViewBinder.BF_ButtonClick, "#moveInClick")
    def moveInClick(self, args):
        """
        一键移入点击事件绑定。
        :param args: 参数
        """
        touchState = args["TouchEvent"]
        if touchState == minecraftEnum.TouchEvent.TouchUp:
            pass

    @ViewBinder.binding(ViewBinder.BF_ButtonClick, "#CellAutoPlace")
    def CellAutoPlace(self, args):
        """
        快捷放置点击事件绑定。
        :param args: 参数
        """
        touchState = args["TouchEvent"]
        if touchState == minecraftEnum.TouchEvent.TouchUp:
            self.handlePutItemFlyToSlot(self.getSlotByPath(args["ButtonPath"]))

    @ViewBinder.binding(ViewBinder.BF_ButtonClick, "#DropAll")
    def DropAll(self, args):
        """
        丢出全部事件绑定。
        :param args: 参数
        """
        touchState = args["TouchEvent"]
        if touchState == minecraftEnum.TouchEvent.TouchUp:
            if self.cursorSlot.itemStack.isEmpty():
                itemSlot = self.getSlotByPath(args["ButtonPath"])
                if self.CanDrop(itemSlot):
                    self.clientSystem.serverCaller("OnDropAll", {"slotId": itemSlot.index})

    @ViewBinder.binding(ViewBinder.BF_ButtonClick, "#DropOne")
    def DropOne(self, args):
        """
        丢出一个事件绑定。
        :param args: 参数
        """
        touchState = args["TouchEvent"]
        if touchState == minecraftEnum.TouchEvent.TouchUp:
            if self.cursorSlot.itemStack.isEmpty():
                itemSlot = self.getSlotByPath(args["ButtonPath"])
                if self.CanDrop(itemSlot):
                    self.clientSystem.serverCaller("OnDrop", {"slotId": itemSlot.index, "count": 1})
            
    @ViewBinder.binding(ViewBinder.BF_ButtonClick, "#ItemRightClick")
    def RitemCellClick(self, args):
        """
        物品槽点击事件绑定。
        :param args: 参数
        """
        touchState = args["TouchEvent"]
        if self.mouse:
            if touchState == minecraftEnum.TouchEvent.TouchDown:
                pass
            elif touchState == minecraftEnum.TouchEvent.TouchUp:
                self.OnCursorItemCellRightUp(args["ButtonPath"])

    @ViewBinder.binding(ViewBinder.BF_ButtonClick, "#ItemCellHovered")
    def itemCellHovered(self, args):
        """
        物品槽悬停事件绑定。
        :param args: 参数
        """
        if not self.mouse:
            self.OnItemCellHovered(args["ButtonPath"])
        if self.mouse:
            self.OnCursorCellHovered(args["ButtonPath"])

    @ViewBinder.binding(ViewBinder.BF_ButtonClick, "#otherHovered")
    def otherHovered(self, args):
        """
        取消悬浮选择
        :param args: 参数
        """
        self.hoverButton = None
        self.hoverText = ''

    @ViewBinder.binding(ViewBinder.BF_ButtonClick, "#DropButtonClick")
    def dropButtonClick(self, args):
        """
        丢弃按钮点击事件绑定。
        :param args: 参数
        """
        touchState = args["TouchEvent"]
        if touchState == minecraftEnum.TouchEvent.TouchDown:
            self.OnDropButtonClick()