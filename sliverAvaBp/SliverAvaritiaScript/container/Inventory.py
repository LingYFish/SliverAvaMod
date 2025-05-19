import mod.client.extraClientApi as clientApi
from mod.client.ui.screenNode import ScreenNode
ViewBinder = clientApi.GetViewBinderCls()
from SliverAvaritiaScript.container.InventoryClientSystem import InventoryBlockClientSystem
from SliverAvaritiaScript.api.lib.itemStack import ItemStack
from itemSlot import ItemSlot
from hoverButton import hoverButton
from SliverAvaritiaScript import modConfig
from flyingItem import FlyingItem
import weakref
import uuid
import json
import math

compFactory = clientApi.GetEngineCompFactory()
levelId = clientApi.GetLevelId()
minecraftEnum = clientApi.GetMinecraftEnum()

class Inventory(ScreenNode):
    screenContent = "/variables_button_mappings_and_controls/safezone_screen_matrix/inner_matrix/safezone_screen_panel/root_screen_panel"
    screenBackGround = screenContent + "/screen_background"
    bg = screenBackGround + "/bg"
    inventoryPanel = bg + "/inventory_panel"
    hotbarGrid = inventoryPanel + "/hotbar_grid"
    inventoryGrid = inventoryPanel + "/inventory_grid"
    flyItemRenderer = screenContent + "/fly_item_renderer"
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
        self.clientSystem = param["clientSystem"]  # type:InventoryBlockClientSystem
        self.playerId = param["playerId"]
        self.pos = param.get("pos", None)
        self.playerViewComp = compFactory.CreatePlayerView(levelId)
        self.cursorSlot = None
        self.slotHight = None
        self.itemSlots = {}
        self.HightTime = 20.0
        self.containerSlots = {}
        self.buttonPathToIndex = {}
        self.selectedSlot = None
        self.holdSlot = None
        self.infoText = ""
        self.infoAlpha = 0.0
        self.clickInterval = 0
        self.holdTime = None
        self.holdItemCount = 0
        self.flyingItems = {}
        self.isTouchDown = False
        self.LastTouchedSlot = None
        self.hoveredSlot = set()
        self.splitData = {}
        self.hoverText = ''
        self.takeInfo = {}
        self.inputMode = None
        self.hoverButton = None
        self.mouse = False
        self.gridLoaded = False
        self.clientSystem.addListenEventUi(self,self.GameRenderTickEvent,eventName='GameRenderTickEvent')

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
        #self.updateHightSlot()

    def updateMode(self):
        inputMode = self.getInputMode()
        if inputMode == self.inputMode:
            return
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
        if self.clickInterval > 0:
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
            # 如果来源物品槽为空，直接返回
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
        """
        根据路径获取物品槽。
        :param slotPath: 物品槽路径
        :return: 物品槽
        """
        path = slotPath[slotPath.find('/'):slotPath.rfind('/')]
        slotId = self.buttonPathToIndex.get(path)
        return self.itemSlots.get(slotId) if isinstance(slotId, int) else self.containerSlots.get(path)

    def CanDrop(self, itemStack):
        """
        判断是否可以丢弃物品。
        :param itemStack: 物品堆
        :return: 是否可以丢弃
        """
        return itemStack.tag.get("minecraft:item_lock", {}).get("__value__", 0) == 0

    def CanMove(self, itemStack):
        """
        判断是否可以移动物品。
        :param itemStack: 物品堆
        :return: 是否可以移动
        """
        return not itemStack.tag.get("minecraft:item_lock", {}).get("__value__", 0) == 1

    def exchangeContainerSlot(self, fromSlot, toSlot):
        """
        交换容器槽。
        :param fromSlot: 来源物品槽
        :param toSlot: 目标物品槽
        """
        pass

    def exchangeInventorySlot(self, fromSlot, toSlot):
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
            self.handleHoveredSlotExchange(fromSlot, toSlot)
        else:
            self.handleNormalExchange(fromSlot, toSlot)

    def canExchangeSlots(self, fromSlot, toSlot):
        """
        判断是否可以交换两个物品槽。
        :param fromSlot: 来源物品槽
        :param toSlot: 目标物品槽
        :return: 是否可以交换
        """
        return self.CanMove(fromSlot.itemStack) and self.CanMove(toSlot.itemStack)

    def handleHoldSlotExchange(self, fromSlot, toSlot):
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

    def handleHoveredSlotExchange(self, fromSlot, toSlot):
        """
        处理悬停物品槽的交换逻辑。
        :param fromSlot: 来源物品槽
        :param toSlot: 目标物品槽
        """
        inventoryData = {(minecraftEnum.ItemPosType.INVENTORY, slotId): itemStack.toItemDict() for slotId, itemStack in self.splitData.items()}
        self.clientSystem.serverCaller("OnSplitSlotEvent", {"inventoryDict": inventoryData})

    def handleNormalExchange(self, fromSlot, toSlot):
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
        self.hoveredSlot.clear()
        self.splitData.clear()

    def setSelectSlot(self, itemSlot):
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
        self.LastTouchedSlot = itemSlot.index
        if self.selectedSlot and self.clickInterval > 0 and self.selectedSlot.index == itemSlot.index:
            self.mergeItems()
        elif not self.selectedSlot:
            self.holdTime = 0
            self.holdSlot = itemSlot
        if not self.mouse:
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
        self.ShowItemText(text)

    def showItemhoverText(self, itemSlot):
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
        total = self.selectedSlot.itemStack.count
        slots = [self.LastTouchedSlot] + list(self.hoveredSlot)
        if total < len(slots):
            return
        splitCount = total // len(slots)
        leftCount = total % len(slots)
        itemName = self.selectedSlot.itemStack.identifier
        auxValue = self.selectedSlot.itemStack.data
        isEnchanted = len(self.selectedSlot.itemStack.getEnchantData()) > 0
        userData = self.selectedSlot.itemStack.tag
        for index,slot_path in enumerate(slots):
            slot = self.itemSlots[slot_path]
            if (index+1) == len(slots):
                slot.setShowItem(itemName, auxValue, isEnchanted, userData)
                slot.setShowCount(splitCount*2)
                self.splitData[slot_path] = ItemStack(newItemName=itemName, newAuxValue=auxValue, count=splitCount*2, userData=userData)
            else:
                slot.setShowItem(itemName, auxValue, isEnchanted, userData)
                slot.setShowCount(splitCount)
                self.splitData[slot_path] = ItemStack(newItemName=itemName, newAuxValue=auxValue, count=splitCount, userData=userData)
        if leftCount > 0:
            self.selectedSlot.setShowItem(itemName, auxValue, isEnchanted, userData)
            self.selectedSlot.setShowCount(leftCount)
            self.splitData[self.selectedSlot.index] = ItemStack(newItemName=itemName, newAuxValue=auxValue, count=leftCount, userData=userData)
        else:
            self.selectedSlot.setHide(True)
            self.splitData[self.selectedSlot.index] = ItemStack()

    def OnItemCellHovered(self, buttonPath):
        """
        物品槽悬停事件。
        :param buttonPath: 按钮路径
        """
        if self.isTouchDown and self.selectedSlot and isinstance(self.selectedSlot.index, int):
            slot = self.getSlotByPath(buttonPath)
            if slot.index != self.LastTouchedSlot and slot.index != self.selectedSlot.index and slot.itemStack.isEmpty() and (not self.holdItemCount > 0):
                self.hoveredSlot.add(slot.index)
                self.splitItems()
        elif not self.isTouchDown and not self.selectedSlot:
            slot = self.getSlotByPath(buttonPath)
            self.slotHight = slot
            self.HightTime = 30.0

    def OnCloseButtonClick(self):
        """
        关闭按钮点击事件。
        """
        self.SetRemove()

    def OnDropButtonClick(self):
        """
        丢弃按钮点击事件。
        """
        if self.selectedSlot:
            self.dropItems()

    def dropItems(self):
        """
        丢弃物品。
        """
        if isinstance(self.selectedSlot.index, int):
            if self.holdSlot and isinstance(self.holdSlot.index, int):
                if self.CanDrop(self.holdSlot.itemStack):
                    self.clientSystem.serverCaller("OnDrop", {"slotId": self.holdSlot.index, "count": self.holdItemCount})
                    self.holdSlot = None
            else:
                if self.CanDrop(self.selectedSlot.itemStack):
                    self.clientSystem.serverCaller("OnDropAll", {"slotId": self.selectedSlot.index})
        self.resetSelectedSlot()

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
        if touchState == minecraftEnum.TouchEvent.TouchDown:
            self.isTouchDown = True
            self.OnItemCellTouchDown(args["ButtonPath"])
        elif touchState == minecraftEnum.TouchEvent.TouchUp:
            self.isTouchDown = False
            self.OnItemCellTouchUp(args["ButtonPath"])

    @ViewBinder.binding(ViewBinder.BF_ButtonClick, "#ItemCellHovered")
    def itemCellHovered(self, args):
        """
        物品槽悬停事件绑定。
        :param args: 参数
        """
        self.OnItemCellHovered(args["ButtonPath"])

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