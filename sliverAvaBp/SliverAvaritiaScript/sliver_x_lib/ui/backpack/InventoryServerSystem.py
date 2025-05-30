from ...server.core.api import extraServerApi as serverApi
from ...server.core import api as sApi
from ...server.core.api import SliverServerSystem as BaseServerSystem
from ...util.itemStack import ItemStack
from ...util.unicodeUtils import UnicodeConvert
from ...util import minecraftEnum
from ...util.sort import ItemSorter
from ...util.Item import isItem
from ...util import nbt
from ...util.tools import extract_numbers
from ... import config as modConfig
import json
import copy
import math
import re

compFactory = serverApi.GetEngineCompFactory()
levelId = serverApi.GetLevelId()

#属于背包的容器 半自动
class InventoryServerSystem(BaseServerSystem):
    """ 背包服务系统 """
    CLIENT_NAME = '' #对应客户端的名称
    
    def __init__(self, namespace, systemName):
        BaseServerSystem.__init__(self, namespace, systemName)
        self.itemsEntitysTouchCool = {} #丢出去物品拾取的冷却时间
        self.CoolDown = {} #触发打开Ui界面的冷却时间
        self.PlayerContainer = {} #玩家打开的容器信息
        self.listenEvent()

    def listenEvent(self):
        """可覆盖的注册事件"""
        compFactory.CreateGame(levelId).AddRepeatedTimer(0.05, self._OnTick)
        self.addListenEvent(self._OnCancelTouchItem, eventName="ServerPlayerTryTouchEvent")
        self.addListenEvent(self._OnExchangeSlotEvent, self.modName, self.CLIENT_NAME, "OnExchangeSlotEvent")
        self.addListenEvent(self._OnSplitSlotEvent, self.modName, self.CLIENT_NAME, "OnSplitSlotEvent")
        self.addListenEvent(self._OnMergeSlotEvent, self.modName, self.CLIENT_NAME, "OnMergeSlotEvent")
        self.addListenEvent(self._OnMergeAllSlotEvent, self.modName, self.CLIENT_NAME, "OnMergeAllSlotEvent")
        self.addListenEvent(self._OnSplitItemToSlotEvent, self.modName, self.CLIENT_NAME, "OnSplitItemToSlotEvent")
        self.addListenEvent(self._OnSplitAndMergeItemEvent, self.modName, self.CLIENT_NAME, "OnSplitAndMergeItemEvent")
        self.addListenEvent(self._Drop, self.modName, self.CLIENT_NAME, "OnDrop")
        self.addListenEvent(self._DropAll, self.modName, self.CLIENT_NAME, "OnDropAll")
        self.addListenEvent(self._closeContainer, self.modName, self.CLIENT_NAME, "OnCloseContainer")

        self.addListenEvent(self._DropCursorItem, self.modName, self.CLIENT_NAME, "DropCursorItem") #鼠标丢弃物品

        self.addListenEvent(self._takeCursorInvItem, self.modName, self.CLIENT_NAME, "takeCursorInvItem") #背包的 鼠标拿取物品
        self.addListenEvent(self._addCursorInvItem, self.modName, self.CLIENT_NAME, "addCursorInvItem") #背包的 鼠标右键添加物品 或者 鼠标放置物品

    def _addCursorInvItem(self,args):
        playerId = args['__id__']
        itemComp = compFactory.CreateItem(playerId)
        toSlot = args['toSlot']
        fromData = args['fromData']
        itemDict = itemComp.GetPlayerItem(minecraftEnum.ItemPosType.INVENTORY, toSlot, True)
        if itemDict:
            itemComp.SetInvItemNum(toSlot, itemDict['count'] + fromData['count'])
        else:
            itemComp.SpawnItemToPlayerInv(fromData,playerId,toSlot)

    def _takeCursorInvItem(self,args):
        invSlot = args['invSlot']
        playerId = args['__id__']
        itemComp = compFactory.CreateItem(playerId)
        itemComp.SetInvItemNum(invSlot, 0)

    def _DropCursorItem(self,args):
        itemDict = args['itemDict']
        self.__DropItem(args['__id__'],itemDict)

    def _OnTick(self):
        """ 20t/s """
        for ItemEntityId in self.itemsEntitysTouchCool.keys():
            self.itemsEntitysTouchCool[ItemEntityId] -= 1
            if self.itemsEntitysTouchCool[ItemEntityId] <= 0:
                del self.itemsEntitysTouchCool[ItemEntityId]
        for playerId in self.CoolDown.keys():
            self.CoolDown[playerId] -= 1
            if self.CoolDown[playerId] <= 0:
                del self.CoolDown[playerId]

    def _OpenContainer(self,playerId):
        """打开容器"""
        self.clientCaller(playerId, "openContainer", {})#发送事件给客户端，在客户端打开ui界面
        self.CoolDown[playerId] = 10

    def _OnCancelTouchItem(self,args):
        """对于拥有冷却的掉落物不拾取"""
        if args["entityId"] in self.itemsEntitysTouchCool:
            args["cancel"] = True

    def _OnExchangeSlotEvent(self,args):
        """物品交换事件"""
        compFactory.CreateItem(args["__id__"]).SetInvItemExchange(args["from"], args["to"])

    def _OnSplitSlotEvent(self, args):
        """分堆事件"""
        playerId = args["__id__"]
        inventoryData = args["inventoryDict"]
        itemComp = compFactory.CreateItem(playerId)
        itemComp.SetPlayerAllItems(inventoryData)
    
    def _OnMergeSlotEvent(self, args):
        playerId = args["__id__"]
        fromSlot = args["from"]
        toSlot = args["to"]
        mergeCount = args["mergeCount"]
        itemComp = compFactory.CreateItem(playerId)
        count = itemComp.GetPlayerItem(minecraftEnum.ItemPosType.INVENTORY, fromSlot)["count"]
        itemComp.SetInvItemNum(fromSlot, itemComp.GetPlayerItem(minecraftEnum.ItemPosType.INVENTORY, fromSlot)["count"] - mergeCount)
        itemdict = itemComp.GetPlayerItem(minecraftEnum.ItemPosType.INVENTORY, toSlot)
        if itemdict and itemdict.get('count'):
            itemComp.SetInvItemNum(toSlot, itemComp.GetPlayerItem(minecraftEnum.ItemPosType.INVENTORY, toSlot)["count"] + mergeCount)
        else:
            itemComp.SetInvItemNum(toSlot, count)
    
    def _OnMergeAllSlotEvent(self, args):
        playerId = args["__id__"]
        mergeItemData = args["mergeItemData"]
        itemComp = compFactory.CreateItem(playerId)
        for slotId, count in mergeItemData.items():
            itemComp.SetInvItemNum(slotId, count)
    
    def _OnSplitItemToSlotEvent(self, args):
        """分堆事件到其他物品上"""
        playerId = args["__id__"]
        fromSlot = args["fromSlot"]
        toSlot = args["toSlot"]
        count = args["count"]
        itemComp = compFactory.CreateItem(playerId)
        itemStack = ItemStack(**itemComp.GetPlayerItem(minecraftEnum.ItemPosType.INVENTORY, fromSlot, True))
        data = {
            (minecraftEnum.ItemPosType.INVENTORY, toSlot): itemStack.split(count).toItemDict(),
            (minecraftEnum.ItemPosType.INVENTORY, fromSlot): itemStack.toItemDict(),
        }
        itemComp.SetPlayerAllItems(data)

    def _OnSplitAndMergeItemEvent(self, args):
        """分堆合并事件"""
        playerId = args["__id__"]
        fromSlot = args["fromSlot"]
        toSlot = args["toSlot"]
        count = args["count"]
        itemComp = compFactory.CreateItem(playerId)
        fromItemStack = itemComp.GetPlayerItem(minecraftEnum.ItemPosType.INVENTORY, fromSlot, True)
        toItemStack = itemComp.GetPlayerItem(minecraftEnum.ItemPosType.INVENTORY, toSlot, True)
        itemComp.SetInvItemNum(fromSlot, fromItemStack["count"] - count)
        itemComp.SetInvItemNum(toSlot, toItemStack["count"] + count)

    def _Drop(self, args):
        """丢弃部分物品"""
        playerId = args["__id__"]
        slotId = args["slotId"]
        count = args["count"]
        itemComp = compFactory.CreateItem(playerId)
        itemDict = itemComp.GetPlayerItem(minecraftEnum.ItemPosType.INVENTORY, slotId, True)
        leftCount = itemDict["count"] - count
        itemDict["count"] = count
        itemComp.SetInvItemNum(slotId, leftCount)
        self.__DropItem(playerId, itemDict)

    def _DropAll(self, args):
        """丢弃全部的物品"""
        playerId = args["__id__"]
        slotId = args["slotId"]
        itemComp = compFactory.CreateItem(playerId)
        itemDict = itemComp.GetPlayerItem(minecraftEnum.ItemPosType.INVENTORY, slotId, True)
        itemComp.SetInvItemNum(slotId, 0)
        self.__DropItem(playerId, itemDict)

    def __DropItem(self, playerId, itemDict):
        """模拟玩家丢弃"""
        dimensionComp, posComp, rotComp = compFactory.CreateDimension(playerId),compFactory.CreatePos(playerId),compFactory.CreateRot(playerId)
        dimensionId = dimensionComp.GetEntityDimensionId()
        pos = posComp.GetPos()
        dir = serverApi.GetDirFromRot(rotComp.GetRot())
        itemEntityId = self.CreateEngineItemEntity(itemDict, dimensionId, pos)
        if itemEntityId:
            mainSystem = serverApi.GetSystem(self.modName, "ruguServer")
            getattr(mainSystem, "clientCaller")(playerId, "swing", {})
            actorMotionComp = compFactory.CreateActorMotion(itemEntityId)
            actorMotionComp.SetMotion(tuple(i * 0.35 for i in dir))
            self.itemsEntitysTouchCool[itemEntityId] = 40

    def _closeContainer(self, args):
        """关闭容器"""
        playerId = args["__id__"]
        if playerId in self.PlayerContainer:
            del self.PlayerContainer[playerId]

#属于方块的容器 全自动
class InventoryBlockServerSystem(BaseServerSystem):
    """ 方块服务系统 """
    OPEN_BLOCK_NAME = '' #要打开的方块名称
    CLIENT_NAME = '' #对应客户端的名称
    
    def __init__(self, namespace, systemName):
        BaseServerSystem.__init__(self, namespace, systemName)
        self.itemsEntitysTouchCool = {} #丢出去物品拾取的冷却时间
        self.CoolDown = {} #触发打开Ui界面的冷却时间
        self.PlayerContainer = {} #玩家打开的容器信息
        self.BlockInfo = {} #方块信息
        self.FromHopperTick = 0
        self.MaxFromHopperTick = 8
        self.HopperInfo = {}
        self.HopperInfo = None
        self.blockInfoComp = sApi.compFactory.CreateBlockInfo(sApi.levelId)
        self.blockStateComp = sApi.compFactory.CreateBlockState(sApi.levelId)
        self.blockEntityDataComp = sApi.compFactory.CreateBlockEntityData(sApi.levelId)
        self.gameComp = sApi.compFactory.CreateGame(sApi.levelId)
        self.itemComp = sApi.compFactory.CreateItem(sApi.levelId)
        self.listenEvent()

    def listenEvent(self):
        """可覆盖的注册事件"""
        compFactory.CreateGame(levelId).AddRepeatedTimer(0.05, self._OnTick)
        self.addListenEvent(self._OpenContainer, eventName="ServerBlockUseEvent")
        self.addListenEvent(self._OnSneaKingOnUse, eventName="ServerItemUseOnEvent")
        self.addListenEvent(self._OnCancelTouchItem, eventName="ServerPlayerTryTouchEvent")
        self.addListenEvent(self._OnBlockRemoveEvent, eventName="BlockRemoveServerEvent")
        self.addListenEvent(self._OnScriptTickServer,eventName='OnScriptTickServer')
        self.addListenEvent(self._OnBlockTickServer, eventName="ServerBlockEntityTickEvent")
        self.addListenEvent(self._OnExchangeSlotEvent, self.modName, self.CLIENT_NAME, "OnExchangeSlotEvent")
        self.addListenEvent(self._OnSplitSlotEvent, self.modName, self.CLIENT_NAME, "OnSplitSlotEvent")
        self.addListenEvent(self._OnMergeSlotEvent, self.modName, self.CLIENT_NAME, "OnMergeSlotEvent")
        self.addListenEvent(self._OnMergeAllSlotEvent, self.modName, self.CLIENT_NAME, "OnMergeAllSlotEvent")
        self.addListenEvent(self._OnSplitItemToSlotEvent, self.modName, self.CLIENT_NAME, "OnSplitItemToSlotEvent")
        self.addListenEvent(self._OnSplitAndMergeItemEvent, self.modName, self.CLIENT_NAME, "OnSplitAndMergeItemEvent")
        self.addListenEvent(self._Drop, self.modName, self.CLIENT_NAME, "OnDrop")
        self.addListenEvent(self._DropAll, self.modName, self.CLIENT_NAME, "OnDropAll")
        self.addListenEvent(self._closeContainer, self.modName, self.CLIENT_NAME, "OnCloseContainer")
        self.addListenEvent(self._OnInputItemToContainer, self.modName, self.CLIENT_NAME, "OnInputItemToContainer")
        self.addListenEvent(self._OnPickItemFromContainer, self.modName, self.CLIENT_NAME, "OnPickItemFromContainer")
        self.addListenEvent(self._OnExchangeItemFromContainer, self.modName, self.CLIENT_NAME, "OnExchangeItemFromContainer")
        self.addListenEvent(self._OnMergeItemIntoContainerInput, self.modName, self.CLIENT_NAME, "OnMergeItemIntoContainerInput")
        self.addListenEvent(self._OnMergeContainerItemIntoInv, self.modName, self.CLIENT_NAME, "OnMergeContainerItemIntoInv")
        self.addListenEvent(self._OnMoveItemInContainer, self.modName, self.CLIENT_NAME, "OnMoveItemInContainer")
        self.addListenEvent(self._OnMergeItemInContainer, self.modName, self.CLIENT_NAME, "OnMergeItemInContainer")
        self.addListenEvent(self._OnExchangeItemInContainer, self.modName, self.CLIENT_NAME, "OnExchangeItemInContainer")

        self.addListenEvent(self._DropCursorItem, self.modName, self.CLIENT_NAME, "DropCursorItem") #鼠标丢弃物品
        self.addListenEvent(self._takeCursorContainerItem, self.modName, self.CLIENT_NAME, "takeCursorContainerItem") #容器的 鼠标拿取物品
        self.addListenEvent(self._addCursorContainerItem, self.modName, self.CLIENT_NAME, "addCursorContainerItem") #容器的 鼠标右键添加物品 或者 鼠标放置物品

        self.addListenEvent(self._takeCursorInvItem, self.modName, self.CLIENT_NAME, "takeCursorInvItem") #背包的 鼠标拿取物品
        self.addListenEvent(self._addCursorInvItem, self.modName, self.CLIENT_NAME, "addCursorInvItem") #背包的 鼠标右键添加物品 或者 鼠标放置物品

        self.addListenEvent(self._sortAllItem, self.modName, self.CLIENT_NAME, "sortAllItem") #整理容器

    def _sortAllItem(self, args):
        """
        Sort all items in the specified slots for the given player.
        :type args: dict
        """
        playerId = args['__id__']
        blockInfo = self.PlayerContainer.get(playerId)
        if not blockInfo:
            return
        dimensionId = blockInfo["dimensionId"]
        pos = blockInfo["pos"]
        slots = sorted(args['slots'], key=extract_numbers)
        items = self.collectItems(dimensionId, pos, slots)
        sorted_items = self.sortItems(items)
        merged_items = self.mergeStacks(sorted_items)
        itemSet = self.fillSlots(merged_items, slots)
        self.updateContainerSlots(playerId, dimensionId, pos, slots, itemSet)

    def collectItems(self, dimensionId, pos, slots):
        """
        Collect items from the specified slots.
        :type dimensionId: int
        :type pos: (int, int, int)
        :type slots: list[str]
        :rtype: list[ItemStack]
        """
        items = []
        for slotId in slots:
            data = self.GetContainerItem(dimensionId, pos, 'container_slot', slotId)
            if data is None or data == {} or ItemStack(**data).isEmpty():
                continue
            items.append(ItemStack(**data))
        return items

    def sortItems(self, items):
        """
        Sort the collected items.
        :type items: list[ItemStack]
        :rtype: list[ItemStack]
        """
        items.sort(key=ItemSorter.sortBy)
        return items

    def mergeStacks(self, items):
        """
        Merge stacks of the same item type.
        :type items: list[ItemStack]
        :rtype: list[ItemStack]
        """
        i = 0
        while i + 1 < len(items):
            fromStack = items[i + 1]
            toStack = items[i]
            if fromStack != toStack.getMaxStackSize(self.itemComp):
                i += 1
                continue
            maxCount = toStack.getMaxStackSize(self.itemComp)
            if toStack.count >= maxCount:
                i += 1
                continue
            j = min(fromStack.count, maxCount - toStack.count)
            toStack.count += j
            fromStack.count -= j
            if fromStack.isEmpty():
                del items[i + 1]
            else:
                i += 1
        return items

    def fillSlots(self, items, slots):
        """
        Fill the slots with the sorted and merged items.
        :type items: list[ItemStack]
        :type slots: list[str]
        :rtype: dict[str, ItemStack]
        """
        while len(items) < len(slots):
            items.append(ItemStack())
        return dict(zip(slots, items))

    def updateContainerSlots(self, playerId, dimensionId, pos, slots, itemSet):
        """
        Update the container slots with the sorted items.
        :type playerId: str
        :type dimensionId: int
        :type pos: (int, int, int)
        :type slots: list[str]
        :type itemSet: dict[str, ItemStack]
        """
        for slotId, data in itemSet.items():
            self.SetContainerItem(playerId, dimensionId, pos, 'container_slot', slotId, data.toItemDict())

    def _addCursorInvItem(self,args):
        playerId = args['__id__']
        itemComp = compFactory.CreateItem(playerId)
        toSlot = args['toSlot']
        fromData = args['fromData']
        itemDict = itemComp.GetPlayerItem(minecraftEnum.ItemPosType.INVENTORY, toSlot, True)
        if itemDict:
            itemComp.SetInvItemNum(toSlot, itemDict['count'] + fromData['count'])
        else:
            itemComp.SpawnItemToPlayerInv(fromData,playerId,toSlot)

    def _takeCursorInvItem(self,args):
        invSlot = args['invSlot']
        playerId = args['__id__']
        itemComp = compFactory.CreateItem(playerId)
        itemComp.SetInvItemNum(invSlot, 0)

    def _DropCursorItem(self,args):
        itemDict = args['itemDict']
        self.__DropItem(args['__id__'],itemDict)

    def _takeCursorContainerItem(self,args):
        containerSlot = args['containerSlot']
        playerId = args['__id__']
        blockInfo = self.PlayerContainer.get(playerId)
        if not blockInfo:
            return
        dimensionId = blockInfo["dimensionId"]
        pos = blockInfo["pos"]
        self.SetContainerItem(None,dimensionId,pos,'container_slot',containerSlot,{})

    def _addCursorContainerItem(self,args):
        playerId = args['__id__']
        toSlot = args['toSlot']
        fromData = args['fromData']
        blockInfo = self.PlayerContainer.get(playerId)
        if not blockInfo:
            return
        dimensionId = blockInfo["dimensionId"]
        pos = blockInfo["pos"]
        toData = self.GetContainerItem(dimensionId,pos,'container_slot',toSlot)
        if toData is None or toData == {} or ItemStack(**toData).isEmpty():
            self.SetContainerItem(None,dimensionId,pos,'container_slot',toSlot,fromData)
        else:
            toData['count']+=fromData['count']
            self.SetContainerItem(None,dimensionId,pos,'container_slot',toSlot,toData)

    def _OnTick(self):
        """ 20t/s """
        for ItemEntityId in self.itemsEntitysTouchCool.keys():
            self.itemsEntitysTouchCool[ItemEntityId] -= 1
            if self.itemsEntitysTouchCool[ItemEntityId] <= 0:
                del self.itemsEntitysTouchCool[ItemEntityId]
        for playerId in self.CoolDown.keys():
            self.CoolDown[playerId] -= 1
            if self.CoolDown[playerId] <= 0:
                del self.CoolDown[playerId]

    def _OpenContainer(self,args):
        """打开容器"""
        blockName = args["blockName"] #type: str
        aux = args["aux"] #type: int
        dimensionId = args["dimensionId"] #type: int
        pos = (args["x"], args["y"], args["z"]) #type: tuple
        playerId = args["playerId"] #type: str
        if blockName == self.OPEN_BLOCK_NAME and playerId not in self.CoolDown:
            self.clientCaller(playerId, "openContainer", {"pos": pos})#发送事件给客户端，在客户端打开ui界面
            self.PlayerContainer[playerId] = {"pos": pos, "dimensionId": dimensionId, "blockName": self.OPEN_BLOCK_NAME, "auxValue": aux}
            self.CoolDown[playerId] = 10
            args["cancel"] = True
    
    def _OnSneaKingOnUse(self, args):
        """取消物品的使用"""
        entityId = args["entityId"]
        blockName = args["blockName"]
        if blockName == self.OPEN_BLOCK_NAME and compFactory.CreatePlayer(entityId).isSneaking():
            args["ret"] = True

    def _OnCancelTouchItem(self,args):
        """对于拥有冷却的掉落物不拾取"""
        if args["entityId"] in self.itemsEntitysTouchCool:
            args["cancel"] = True

    def _OnBlockRemoveEvent(self, args):
        """删除数据"""
        pos =  (args["x"], args["y"], args["z"])
        fullName = args["fullName"]
        auxValue = args["auxValue"]
        dimensionId =  args["dimension"]
        for playerId, blockData in self.PlayerContainer.items():
            if fullName == blockData["blockName"] and pos == blockData["pos"] and auxValue == blockData["auxValue"] and dimensionId == blockData["dimensionId"]:
                self.clientCaller(playerId, "closeContainer", {})
        if not fullName == self.OPEN_BLOCK_NAME:
            return
        if 'container_slot' in self.BlockInfo[(dimensionId, pos)]:
            for slot,vaule in self.BlockInfo[(dimensionId, pos)]['container_slot'].items():
                self.CreateEngineItemEntity(json.loads(vaule), dimensionId, pos)
        if (dimensionId, pos) in self.BlockInfo:
            del self.BlockInfo[(dimensionId, pos)]
        blockEntityDataComp = compFactory.CreateBlockEntityData(levelId)
        blockData = blockEntityDataComp.GetBlockEntityData(dimensionId, pos)
        blockEntityDataComp.CleanExtraData(dimensionId, pos)
    
    def _OnScriptTickServer(self):
        '''for playerId, blockData in self.PlayerContainer.items():
            posComp = compFactory.CreatePos(playerId)
            pos = tuple(map(lambda i: i + 0.5, blockData['pos']))
            PlayerPos = posComp.GetPos()
            distance = math.sqrt(pos[0] - PlayerPos[0] ** 2 + pos[1] - PlayerPos[1] ** 2 + pos[2] - PlayerPos[2] ** 2)
            if distance > 7.0:
                """距离过远自动关闭容器交互"""
                self.clientCaller(playerId, "closeContainer", {})'''

    def _OnBlockTickServer(self,args):
        if args["blockName"] != self.OPEN_BLOCK_NAME:
            return
        dimensionId = args["dimension"]
        pos = (args["posX"], args["posY"], args["posZ"])
        blockEntityDataComp = compFactory.CreateBlockEntityData(levelId)
        blockData = blockEntityDataComp.GetBlockEntityData(dimensionId,pos)
        if not blockData['_container_']:
            blockData['_container_'] = {}
        if (dimensionId, pos) not in self.BlockInfo:
            print ("初始化容器信息成功 - {}".format(blockData['_container_']))
            self.BlockInfo[(dimensionId, pos)] = blockData['_container_']
        if self.HopperInfo:
            self.FromHopperTick += 1
            if self.FromHopperTick >= self.MaxFromHopperTick:
                self.OnWithHopper(dimensionId,pos)
                self.FromHopperTick = 0

    def OnWithHopper(self,dimensionId,pos):
        for side in range(1, 6):
            nextpos = minecraftEnum.BlockPos.move_next(pos, side)
            self.setHopperToContainer(nextpos,side,dimensionId,pos)
        nextpos = minecraftEnum.BlockPos.move_up(pos, 1)
        self.setHopperToContainer(nextpos,side,dimensionId,pos)
        nextpos = minecraftEnum.BlockPos.move_down(pos, 1)
        self.setItemToHopper(nextpos,side,dimensionId,pos)

    def setHopperToContainer(self,nextpos,side,dimensionId,pos):
        block = self.blockInfoComp.GetBlockNew(nextpos, dimensionId)
        if block['name'] != 'minecraft:hopper':
            return
        states = self.blockStateComp.GetBlockStatesFromAuxValue(block['name'], block['aux'])
        if not minecraftEnum.hopperType.can_take_out(states, minecraftEnum.hopperType.side_to_face(side)):
            return
        size = self.itemComp.GetContainerSize(nextpos, dimensionId)
        _ItemList = [] #type: list[tuple[str,ItemStack]]
        for slotId in self.HopperInfo['toinSlot']:
            itemDict = self.GetContainerItem(dimensionId, pos,'container_slot',slotId)
            if itemDict is None or itemDict == {} or ItemStack(**itemDict).isEmpty():
                _ItemList.append((slotId,ItemStack()))
                continue
            _ItemList.append((slotId,ItemStack(**itemDict)))
        if len(_ItemList) == 0:
            return
        for HopperSlotId in range(size):
            for slotId,itemStack in _ItemList:
                itemDict = self.itemComp.GetContainerItem(nextpos, HopperSlotId, dimensionId, True)
                if not itemStack.isEmpty():
                    if itemDict:
                        if itemStack == ItemStack(**itemDict):
                            hopperItemStack = ItemStack(**itemDict)
                            if itemStack.count < itemStack.getMaxStackSize(self.itemComp):
                                itemStack.count += 1
                                hopperItemStack.count -= 1
                                self.SetContainerItem(None,dimensionId,pos,'container_slot',slotId,itemStack.toItemDict())
                                self.itemComp.SpawnItemToContainer(hopperItemStack.toItemDict(), HopperSlotId, nextpos, dimensionId)
                                return
                else:
                    if itemDict:
                        hopperItemStack = ItemStack(**itemDict)
                        newIItemStack = hopperItemStack.clone()
                        hopperItemStack.count -= 1
                        newIItemStack.count = 1
                        self.SetContainerItem(None,dimensionId,pos,'container_slot',slotId,newIItemStack.toItemDict())
                        self.itemComp.SpawnItemToContainer(hopperItemStack.toItemDict(), HopperSlotId, nextpos, dimensionId)
                        return
    
    def setItemToHopper(self,nextpos,side,dimensionId,pos):
        block = self.blockInfoComp.GetBlockNew(nextpos, dimensionId)
        if block['name'] != 'minecraft:hopper':
            return
        states = self.blockStateComp.GetBlockStatesFromAuxValue(block['name'], block['aux'])
        if not minecraftEnum.hopperType.can_take_in(states):
            return
        size = self.itemComp.GetContainerSize(nextpos, dimensionId)
        _ItemList = [] #type: list[tuple[str,ItemStack]]
        for slotId in self.HopperInfo['ouptinSlot']:
            itemDict = self.GetContainerItem(dimensionId, pos,'container_slot',slotId)
            if itemDict is None or itemDict == {} or ItemStack(**itemDict).isEmpty():
                continue
            _ItemList.append((slotId,ItemStack(**itemDict)))
        if len(_ItemList) == 0:
            return
        for HopperSlotId in range(size):
            for slotId,itemStack in _ItemList:
                itemDict = self.itemComp.GetContainerItem(nextpos, HopperSlotId, dimensionId, True)
                if itemDict:
                    if itemStack == ItemStack(**itemDict):
                        hopperItemStack = ItemStack(**itemDict)
                        if hopperItemStack.count < hopperItemStack.getMaxStackSize(self.itemComp):
                            itemStack.count -= 1
                            hopperItemStack.count += 1
                            self.SetContainerItem(None,dimensionId,pos,'container_slot',slotId,itemStack.toItemDict())
                            self.itemComp.SpawnItemToContainer(hopperItemStack.toItemDict(), HopperSlotId, nextpos, dimensionId)
                            return
                else:
                    hopperItemStack = itemStack.clone()
                    itemStack.count -= 1
                    hopperItemStack.count = 1
                    self.SetContainerItem(None,dimensionId,pos,'container_slot',slotId,itemStack.toItemDict())
                    self.itemComp.SpawnItemToContainer(hopperItemStack.toItemDict(), HopperSlotId, nextpos, dimensionId)
                    return

    def _OnExchangeSlotEvent(self,args):
        """物品交换事件"""
        compFactory.CreateItem(args["__id__"]).SetInvItemExchange(args["from"], args["to"])

    def _OnSplitSlotEvent(self, args):
        """分堆事件"""
        playerId = args["__id__"]
        inventoryData = args["inventoryDict"]
        itemComp = compFactory.CreateItem(playerId)
        itemComp.SetPlayerAllItems(inventoryData)
    
    def _OnMergeSlotEvent(self, args):
        playerId = args["__id__"]
        fromSlot = args["from"]
        toSlot = args["to"]
        mergeCount = args["mergeCount"]
        itemComp = compFactory.CreateItem(playerId)
        count = itemComp.GetPlayerItem(minecraftEnum.ItemPosType.INVENTORY, fromSlot)["count"]
        itemComp.SetInvItemNum(fromSlot, itemComp.GetPlayerItem(minecraftEnum.ItemPosType.INVENTORY, fromSlot)["count"] - mergeCount)
        itemdict = itemComp.GetPlayerItem(minecraftEnum.ItemPosType.INVENTORY, toSlot)
        if itemdict and itemdict.get('count'):
            itemComp.SetInvItemNum(toSlot, itemComp.GetPlayerItem(minecraftEnum.ItemPosType.INVENTORY, toSlot)["count"] + mergeCount)
        else:
            itemComp.SetInvItemNum(toSlot, count)

    def _OnMergeAllSlotEvent(self, args):
        playerId = args["__id__"]
        mergeItemData = args["mergeItemData"]
        itemComp = compFactory.CreateItem(playerId)
        for slotId, count in mergeItemData.items():
            itemComp.SetInvItemNum(slotId, count)
    
    def _OnSplitItemToSlotEvent(self, args):
        """分堆事件到其他物品上"""
        playerId = args["__id__"]
        fromSlot = args["fromSlot"]
        toSlot = args["toSlot"]
        count = args["count"]
        itemComp = compFactory.CreateItem(playerId)
        itemStack = ItemStack(**itemComp.GetPlayerItem(minecraftEnum.ItemPosType.INVENTORY, fromSlot, True))
        data = {
            (minecraftEnum.ItemPosType.INVENTORY, toSlot): itemStack.split(count).toItemDict(),
            (minecraftEnum.ItemPosType.INVENTORY, fromSlot): itemStack.toItemDict(),
        }
        itemComp.SetPlayerAllItems(data)

    def _OnSplitAndMergeItemEvent(self, args):
        """分堆合并事件"""
        playerId = args["__id__"]
        fromSlot = args["fromSlot"]
        toSlot = args["toSlot"]
        count = args["count"]
        itemComp = compFactory.CreateItem(playerId)
        fromItemStack = itemComp.GetPlayerItem(minecraftEnum.ItemPosType.INVENTORY, fromSlot, True)
        toItemStack = itemComp.GetPlayerItem(minecraftEnum.ItemPosType.INVENTORY, toSlot, True)
        itemComp.SetInvItemNum(fromSlot, fromItemStack["count"] - count)
        itemComp.SetInvItemNum(toSlot, toItemStack["count"] + count)

    def _Drop(self, args):
        """丢弃部分物品"""
        playerId = args["__id__"]
        slotId = args["slotId"]
        count = args["count"]
        if isinstance(slotId,int):
            itemComp = compFactory.CreateItem(playerId)
            itemDict = itemComp.GetPlayerItem(minecraftEnum.ItemPosType.INVENTORY, slotId, True)
            leftCount = itemDict["count"] - count
            itemDict["count"] = count
            itemComp.SetInvItemNum(slotId, leftCount)
        else:
            blockInfo = self.PlayerContainer.get(playerId)
            if not blockInfo:
                return
            dimensionId = blockInfo["dimensionId"]
            pos = blockInfo["pos"]
            itemDict = self.GetContainerItem(dimensionId,pos,'container_slot',slotId)
            leftCount = itemDict["count"] - count
            itemDict["count"] = count
            bockitemDict = copy.deepcopy(itemDict)
            bockitemDict['count'] = leftCount
            self.SetContainerItem(None,dimensionId,pos,'container_slot',slotId,bockitemDict)
        self.__DropItem(playerId, itemDict)

    def _DropAll(self, args):
        """丢弃全部的物品"""
        playerId = args["__id__"]
        slotId = args["slotId"]
        if isinstance(slotId,int):
            itemComp = compFactory.CreateItem(playerId)
            itemDict = itemComp.GetPlayerItem(minecraftEnum.ItemPosType.INVENTORY, slotId, True)
            itemComp.SetInvItemNum(slotId, 0)
        else:
            blockInfo = self.PlayerContainer.get(playerId)
            if not blockInfo:
                return
            dimensionId = blockInfo["dimensionId"]
            pos = blockInfo["pos"]
            itemDict = self.GetContainerItem(dimensionId,pos,'container_slot',slotId)
            bockitemDict = copy.deepcopy(itemDict)
            bockitemDict['count'] = 0
            self.SetContainerItem(None,dimensionId,pos,'container_slot',slotId,bockitemDict)
        self.__DropItem(playerId, itemDict)

    def __DropItem(self, playerId, itemDict):
        """模拟玩家丢弃"""
        dimensionComp, posComp, rotComp = compFactory.CreateDimension(playerId),compFactory.CreatePos(playerId),compFactory.CreateRot(playerId)
        dimensionId = dimensionComp.GetEntityDimensionId()
        pos = posComp.GetPos()
        dir = serverApi.GetDirFromRot(rotComp.GetRot())
        itemEntityId = self.CreateEngineItemEntity(itemDict, dimensionId, pos)
        if itemEntityId:
            actorMotionComp = compFactory.CreateActorMotion(itemEntityId)
            actorMotionComp.SetMotion(tuple(i * 0.35 for i in dir))
            self.itemsEntitysTouchCool[itemEntityId] = 40

    def _closeContainer(self, args):
        """关闭容器"""
        playerId = args["__id__"]
        if playerId in self.PlayerContainer:
            del self.PlayerContainer[playerId]

    def GetContainerItem(self, dimensionId, pos, name, key):
        """
        获取容器内的物品
        - dimensionId 维度
        - pos 坐标
        - name 保存名
        - key 键名
        """
        data = self.BlockInfo.get((dimensionId, pos))
        if data and data.get(name) and data.get(name).get(key):
            return UnicodeConvert(json.loads(data[name][key]))
        return None
    
    def SetContainerItem(self, playerId, dimensionId, pos, name, key, value):
        """
        设置容器内的物品
        - dimensionId 维度
        - pos 坐标
        - name 保存名
        - key 键名
        - vaule 键值
        """
        blockEntityDataComp = compFactory.CreateBlockEntityData(levelId)
        data = self.BlockInfo.get((dimensionId, pos))
        if data is None:
            self.BlockInfo[(dimensionId, pos)] = blockEntityDataComp.GetBlockEntityData(dimensionId, pos)['_container_']
        data = self.BlockInfo.get((dimensionId, pos))
        if isinstance(data, dict):
            blockData = blockEntityDataComp.GetBlockEntityData(dimensionId, pos)
            if not blockData['_container_']:
                 blockData['_container_'] = {}
            if name not in blockData['_container_']:
                _dict = copy.deepcopy(blockData['_container_'])
                _dict[name] = {}
                blockData['_container_'] = _dict
            if name not in data:
                data[name] = {}
            data[name][key] = json.dumps(value)
            _dict = copy.deepcopy(blockData['_container_'])
            _dict[name][key] = data[name][key]
            blockData['_container_'] = _dict

    def _OnExchangeItemInContainer(self, args):
        """交换容器内的物品"""
        playerId = args["__id__"]
        fromSlot = args["fromSlot"]
        toSlot = args["toSlot"]
        blockInfo = self.PlayerContainer.get(playerId)
        if not blockInfo:
            return
        dimensionId = blockInfo["dimensionId"]
        pos = blockInfo["pos"]
        fromItem = self.GetContainerItem(dimensionId, pos,'container_slot', fromSlot)
        toItem = self.GetContainerItem(dimensionId, pos,'container_slot', toSlot)
        self.SetContainerItem(playerId, dimensionId, pos, 'container_slot', fromSlot, toItem)
        self.SetContainerItem(playerId, dimensionId, pos, 'container_slot', toSlot, fromItem)
    
    def _OnMergeItemInContainer(self, args):
        """合并容器内的物品"""
        playerId = args["__id__"]
        fromSlot = args["fromSlot"]
        toSlot = args["toSlot"]
        count = args["count"]
        blockInfo = self.PlayerContainer.get(playerId)
        if not blockInfo:
            return
        dimensionId = blockInfo["dimensionId"]
        pos = blockInfo["pos"]
        fromItem = self.GetContainerItem(dimensionId, pos, 'container_slot', fromSlot)
        toItem = self.GetContainerItem(dimensionId, pos, 'container_slot', toSlot)
        fromItem["count"] -= count
        self.SetContainerItem(playerId, dimensionId, pos, 'container_slot', fromSlot, fromItem)
        toItem["count"] += count
        self.SetContainerItem(playerId, dimensionId, pos, 'container_slot', toSlot, toItem)
    
    def _OnMoveItemInContainer(self, args):
        """移动容器内的物品"""
        playerId = args["__id__"]
        fromSlot = args["fromSlot"]
        toSlot = args["toSlot"]
        count = args["count"]
        blockInfo = self.PlayerContainer.get(playerId)
        if not blockInfo:
            return
        dimensionId = blockInfo["dimensionId"]
        pos = blockInfo["pos"]
        fromItem = self.GetContainerItem(dimensionId, pos, 'container_slot', fromSlot)
        toItem = self.GetContainerItem(dimensionId, pos, 'container_slot', toSlot)
        fromItem["count"] -= count
        toItem = fromItem
        self.SetContainerItem(playerId, dimensionId, pos, 'container_slot', fromSlot, fromItem)
        toItem["count"] = count
        self.SetContainerItem(playerId, dimensionId, pos, 'container_slot', toSlot, toItem)
    
    def _OnMergeContainerItemIntoInv(self, args):
        """移动容器内的物品到玩家背包"""
        playerId = args["__id__"]
        containerSlot = args["containerSlot"]
        invSlot = args["invSlot"]
        count = args["count"]
        itemComp = compFactory.CreateItem(playerId)
        blockInfo = self.PlayerContainer.get(playerId)
        if not blockInfo:
            return
        dimensionId = blockInfo["dimensionId"]
        pos = blockInfo["pos"]
        containerItem = self.GetContainerItem(dimensionId, pos, 'container_slot', containerSlot)
        itemDict = itemComp.GetPlayerItem(minecraftEnum.ItemPosType.INVENTORY, invSlot, True)
        count = min(count, containerItem["count"])
        containerItem["count"] -= count
        self.SetContainerItem(playerId, dimensionId, pos, 'container_slot', containerSlot, containerItem)
        itemComp.SetInvItemNum(invSlot, itemDict["count"] + count)
    
    def _OnInputItemToContainer(self, args):
        """移动背包物品到容器"""
        playerId = args["__id__"]
        fromSlot = args["fromSlot"]
        toSlot = args["toSlot"]
        count = args["count"]
        itemComp = compFactory.CreateItem(playerId)
        blockInfo = self.PlayerContainer.get(playerId)
        if not blockInfo:
            return
        dimensionId = blockInfo["dimensionId"]
        pos = blockInfo["pos"]
        itemDict = itemComp.GetPlayerItem(minecraftEnum.ItemPosType.INVENTORY, fromSlot, True)
        itemDict["count"] -= count
        itemComp.SetInvItemNum(fromSlot, itemDict["count"])
        itemDict["count"] = count
        self.SetContainerItem(playerId, dimensionId, pos, 'container_slot', toSlot, itemDict)
    
    def _OnExchangeItemFromContainer(self, args):
        """交换容器和背包的物品"""
        playerId = args["__id__"]
        containerSlot = args["containerSlot"]
        invSlot = args["invSlot"]
        itemComp = compFactory.CreateItem(playerId)
        blockInfo = self.PlayerContainer.get(playerId)
        if not blockInfo:
            return
        dimensionId = blockInfo["dimensionId"]
        pos = blockInfo["pos"]
        containerItem = self.GetContainerItem(dimensionId, pos, 'container_slot', containerSlot)
        invItem = itemComp.GetPlayerItem(minecraftEnum.ItemPosType.INVENTORY, invSlot, True)
        self.SetContainerItem(playerId, dimensionId, pos, 'container_slot', containerSlot, invItem)
        itemComp.SpawnItemToPlayerInv(containerItem, playerId, invSlot)
    
    def _OnPickItemFromContainer(self, args):
        """移动容器内物品到物品栏"""
        playerId = args["__id__"]
        containerSlot = args["containerSlot"]
        invSlot = args["invSlot"]
        count = args["count"]
        itemComp = compFactory.CreateItem(playerId)
        blockInfo = self.PlayerContainer.get(playerId)
        if not blockInfo:
            return
        dimensionId = blockInfo["dimensionId"]
        pos = blockInfo["pos"]
        containerItem = self.GetContainerItem(dimensionId, pos, 'container_slot', containerSlot)
        invItem = containerItem.copy()
        count = min(count, containerItem["count"])
        containerItem["count"] -= count
        invItem["count"] = count
        self.SetContainerItem(playerId, dimensionId, pos, 'container_slot', containerSlot, containerItem)
        itemComp.SpawnItemToPlayerInv(invItem, playerId, invSlot)
    
    def _OnMergeItemIntoContainerInput(self, args):
        """合并物品到容器内"""
        playerId = args["__id__"]
        fromSlot = args["fromSlot"]
        toSlot = args["toSlot"]
        count = args["count"]
        itemComp = compFactory.CreateItem(playerId)
        blockInfo = self.PlayerContainer.get(playerId)
        if not blockInfo:
            return
        dimensionId = blockInfo["dimensionId"]
        pos = blockInfo["pos"]
        itemDict = itemComp.GetPlayerItem(minecraftEnum.ItemPosType.INVENTORY, fromSlot, True)
        itemStack = ItemStack(**itemDict)
        itemComp.SetInvItemNum(fromSlot, itemStack.count - count)
        containerItem = self.GetContainerItem(dimensionId, 'container_slot', pos, toSlot)
        if containerItem:
            containerItem["count"] += count
        else:
            containerItem = itemStack.toItemDict()
        self.SetContainerItem(playerId, dimensionId, pos, 'container_slot', toSlot, containerItem)

#属于玩家实体数据的容器 全自动
class InventoryEntityserverSystem(BaseServerSystem):
    """ 实体背包服务系统 """
    CLIENT_NAME = '' #对应客户端的名称
    
    def __init__(self, namespace, systemName):
        BaseServerSystem.__init__(self, namespace, systemName)
        self.itemsEntitysTouchCool = {} #丢出去物品拾取的冷却时间
        self.CoolDown = {} #触发打开Ui界面的冷却时间
        self.PlayerContainer = {} #玩家打开的容器信息
        self.listenEvent()

    def listenEvent(self):
        """可覆盖的注册事件"""
        compFactory.CreateGame(levelId).AddRepeatedTimer(0.05, self._OnTick)
        self.addListenEvent(self._OpenContainer, self.modName, self.CLIENT_NAME, "openContainer")
        self.addListenEvent(self._OnCancelTouchItem, eventName="ServerPlayerTryTouchEvent")
        self.addListenEvent(self._OnExchangeSlotEvent, self.modName, self.CLIENT_NAME, "OnExchangeSlotEvent")
        self.addListenEvent(self._OnSplitSlotEvent, self.modName, self.CLIENT_NAME, "OnSplitSlotEvent")
        self.addListenEvent(self._OnMergeSlotEvent, self.modName, self.CLIENT_NAME, "OnMergeSlotEvent")
        self.addListenEvent(self._OnMergeAllSlotEvent, self.modName, self.CLIENT_NAME, "OnMergeAllSlotEvent")
        self.addListenEvent(self._OnSplitItemToSlotEvent, self.modName, self.CLIENT_NAME, "OnSplitItemToSlotEvent")
        self.addListenEvent(self._OnSplitAndMergeItemEvent, self.modName, self.CLIENT_NAME, "OnSplitAndMergeItemEvent")
        self.addListenEvent(self._Drop, self.modName, self.CLIENT_NAME, "OnDrop")
        self.addListenEvent(self._DropAll, self.modName, self.CLIENT_NAME, "OnDropAll")
        self.addListenEvent(self._closeContainer, self.modName, self.CLIENT_NAME, "OnCloseContainer")
        self.addListenEvent(self._OnInputItemToContainer, self.modName, self.CLIENT_NAME, "OnInputItemToContainer")
        self.addListenEvent(self._OnPickItemFromContainer, self.modName, self.CLIENT_NAME, "OnPickItemFromContainer")
        self.addListenEvent(self._OnExchangeItemFromContainer, self.modName, self.CLIENT_NAME, "OnExchangeItemFromContainer")
        self.addListenEvent(self._OnMergeItemIntoContainerInput, self.modName, self.CLIENT_NAME, "OnMergeItemIntoContainerInput")
        self.addListenEvent(self._OnMergeContainerItemIntoInv, self.modName, self.CLIENT_NAME, "OnMergeContainerItemIntoInv")
        self.addListenEvent(self._OnMoveItemInContainer, self.modName, self.CLIENT_NAME, "OnMoveItemInContainer")
        self.addListenEvent(self._OnMergeItemInContainer, self.modName, self.CLIENT_NAME, "OnMergeItemInContainer")
        self.addListenEvent(self._OnExchangeItemInContainer, self.modName, self.CLIENT_NAME, "OnExchangeItemInContainer")
        self.addListenEvent(self._OnCarriedNewItemChangedServerEvent,eventName='OnCarriedNewItemChangedServerEvent')
        self.addListenEvent(self._DropCursorItem, self.modName, self.CLIENT_NAME, "DropCursorItem") #鼠标丢弃物品
        self.addListenEvent(self._takeCursorContainerItem, self.modName, self.CLIENT_NAME, "takeCursorContainerItem") #容器的 鼠标拿取物品
        self.addListenEvent(self._addCursorContainerItem, self.modName, self.CLIENT_NAME, "addCursorContainerItem") #容器的 鼠标右键添加物品 或者 鼠标放置物品

        self.addListenEvent(self._takeCursorInvItem, self.modName, self.CLIENT_NAME, "takeCursorInvItem") #背包的 鼠标拿取物品
        self.addListenEvent(self._addCursorInvItem, self.modName, self.CLIENT_NAME, "addCursorInvItem") #背包的 鼠标右键添加物品 或者 鼠标放置物品

    def _addCursorInvItem(self,args):
        playerId = args['__id__']
        itemComp = compFactory.CreateItem(playerId)
        toSlot = args['toSlot']
        fromData = args['fromData']
        itemDict = itemComp.GetPlayerItem(minecraftEnum.ItemPosType.INVENTORY, toSlot, True)
        if itemDict:
            itemComp.SetInvItemNum(toSlot, itemDict['count'] + fromData['count'])
        else:
            itemComp.SpawnItemToPlayerInv(fromData,playerId,toSlot)

    def _takeCursorInvItem(self,args):
        invSlot = args['invSlot']
        playerId = args['__id__']
        itemComp = compFactory.CreateItem(playerId)
        itemComp.SetInvItemNum(invSlot, 0)

    def _DropCursorItem(self,args):
        itemDict = args['itemDict']
        self.__DropItem(args['__id__'],itemDict)

    def _takeCursorContainerItem(self,args):
        containerSlot = args['containerSlot']
        playerId = args['__id__']
        itemInfo = self.PlayerContainer.get(playerId)
        if not itemInfo:
            return
        itemSlot = itemInfo["itemSlot"]
        self.SetContainerItem(playerId,itemSlot,'container_slot',containerSlot,{})

    def _addCursorContainerItem(self,args):
        playerId = args['__id__']
        toSlot = args['toSlot']
        fromData = args['fromData']
        itemInfo = self.PlayerContainer.get(playerId)
        if not itemInfo:
            return
        itemSlot = itemInfo["itemSlot"]
        toData = self.GetContainerItem(playerId,itemSlot,'container_slot',toSlot)
        if toData is None or toData == {} or ItemStack(**toData).isEmpty():
            self.SetContainerItem(playerId,itemSlot,'container_slot',toSlot,fromData)
        else:
            toData['count']+=fromData['count']
            self.SetContainerItem(playerId,itemSlot,'container_slot',toSlot,toData)

    def _OnTick(self):
        """ 20t/s """
        for ItemEntityId in self.itemsEntitysTouchCool.keys():
            self.itemsEntitysTouchCool[ItemEntityId] -= 1
            if self.itemsEntitysTouchCool[ItemEntityId] <= 0:
                del self.itemsEntitysTouchCool[ItemEntityId]
        for playerId in self.CoolDown.keys():
            self.CoolDown[playerId] -= 1
            if self.CoolDown[playerId] <= 0:
                del self.CoolDown[playerId]

    def _OnCarriedNewItemChangedServerEvent(self,args):
        pass

    def _OpenContainer(self,args):
        """打开容器"""
        playerId = args["playerId"] #type: str
        if not compFactory.CreateExtraData(playerId).GetExtraData("SliverXentityData"):
            compFactory.CreateExtraData(playerId).SetExtraData("SliverXentityData",json.dumps({'container_slot':{}}))
        self.clientCaller(playerId, "openContainer", {'data':UnicodeConvert(json.loads(compFactory.CreateExtraData(playerId).GetExtraData("SliverXentityData"))['container_slot'])})#发送事件给客户端，在客户端打开ui界面
        self.PlayerContainer[playerId] = {"itemSlot":-1}
        self.CoolDown[playerId] = 10
        
    def _OnCancelTouchItem(self,args):
        """对于拥有冷却的掉落物不拾取"""
        if args["entityId"] in self.itemsEntitysTouchCool:
            args["cancel"] = True
    
    def _OnExchangeSlotEvent(self,args):
        """物品交换事件"""
        compFactory.CreateItem(args["__id__"]).SetInvItemExchange(args["from"], args["to"])

    def _OnSplitSlotEvent(self, args):
        """分堆事件"""
        playerId = args["__id__"]
        inventoryData = args["inventoryDict"]
        itemComp = compFactory.CreateItem(playerId)
        itemComp.SetPlayerAllItems(inventoryData)
    
    def _OnMergeSlotEvent(self, args):
        playerId = args["__id__"]
        fromSlot = args["from"]
        toSlot = args["to"]
        mergeCount = args["mergeCount"]
        itemComp = compFactory.CreateItem(playerId)
        count = itemComp.GetPlayerItem(minecraftEnum.ItemPosType.INVENTORY, fromSlot)["count"]
        itemComp.SetInvItemNum(fromSlot, itemComp.GetPlayerItem(minecraftEnum.ItemPosType.INVENTORY, fromSlot)["count"] - mergeCount)
        itemdict = itemComp.GetPlayerItem(minecraftEnum.ItemPosType.INVENTORY, toSlot)
        if itemdict and itemdict.get('count'):
            itemComp.SetInvItemNum(toSlot, itemComp.GetPlayerItem(minecraftEnum.ItemPosType.INVENTORY, toSlot)["count"] + mergeCount)
        else:
            itemComp.SetInvItemNum(toSlot, count)
    
    def _OnMergeAllSlotEvent(self, args):
        playerId = args["__id__"]
        mergeItemData = args["mergeItemData"]
        itemComp = compFactory.CreateItem(playerId)
        for slotId, count in mergeItemData.items():
            itemComp.SetInvItemNum(slotId, count)
    
    def _OnSplitItemToSlotEvent(self, args):
        """分堆事件到其他物品上"""
        playerId = args["__id__"]
        fromSlot = args["fromSlot"]
        toSlot = args["toSlot"]
        count = args["count"]
        itemComp = compFactory.CreateItem(playerId)
        itemStack = ItemStack(**itemComp.GetPlayerItem(minecraftEnum.ItemPosType.INVENTORY, fromSlot, True))
        data = {
            (minecraftEnum.ItemPosType.INVENTORY, toSlot): itemStack.split(count).toItemDict(),
            (minecraftEnum.ItemPosType.INVENTORY, fromSlot): itemStack.toItemDict(),
        }
        itemComp.SetPlayerAllItems(data)

    def _OnSplitAndMergeItemEvent(self, args):
        """分堆合并事件"""
        playerId = args["__id__"]
        fromSlot = args["fromSlot"]
        toSlot = args["toSlot"]
        count = args["count"]
        itemComp = compFactory.CreateItem(playerId)
        fromItemStack = itemComp.GetPlayerItem(minecraftEnum.ItemPosType.INVENTORY, fromSlot, True)
        toItemStack = itemComp.GetPlayerItem(minecraftEnum.ItemPosType.INVENTORY, toSlot, True)
        itemComp.SetInvItemNum(fromSlot, fromItemStack["count"] - count)
        itemComp.SetInvItemNum(toSlot, toItemStack["count"] + count)

    def _Drop(self, args):
        """丢弃部分物品"""
        playerId = args["__id__"]
        slotId = args["slotId"]
        count = args["count"]
        if isinstance(slotId,int):
            itemComp = compFactory.CreateItem(playerId)
            itemDict = itemComp.GetPlayerItem(minecraftEnum.ItemPosType.INVENTORY, slotId, True)
            leftCount = itemDict["count"] - count
            itemDict["count"] = count
            itemComp.SetInvItemNum(slotId, leftCount)
        else:
            itemInfo = self.PlayerContainer.get(playerId)
            if not itemInfo:
                return
            itemSlot = itemInfo["itemSlot"]
            itemDict = self.GetContainerItem(playerId,itemSlot,'container_slot',slotId)
            leftCount = itemDict["count"] - count
            itemDict["count"] = count
            bockitemDict = copy.deepcopy(itemDict)
            bockitemDict['count'] = leftCount
            self.SetContainerItem(playerId,itemSlot,'container_slot',slotId,bockitemDict)
        self.__DropItem(playerId, itemDict)

    def _DropAll(self, args):
        """丢弃全部的物品"""
        playerId = args["__id__"]
        slotId = args["slotId"]
        if isinstance(slotId,int):
            itemComp = compFactory.CreateItem(playerId)
            itemDict = itemComp.GetPlayerItem(minecraftEnum.ItemPosType.INVENTORY, slotId, True)
            itemComp.SetInvItemNum(slotId, 0)
        else:
            itemInfo = self.PlayerContainer.get(playerId)
            if not itemInfo:
                return
            itemSlot = itemInfo["itemSlot"]
            itemDict = self.GetContainerItem(playerId,itemSlot,'container_slot',slotId)
            bockitemDict = copy.deepcopy(itemDict)
            bockitemDict['count'] = 0
            self.SetContainerItem(playerId,itemSlot,'container_slot',slotId,bockitemDict)
        self.__DropItem(playerId, itemDict)

    def __DropItem(self, playerId, itemDict):
        """模拟玩家丢弃"""
        dimensionComp, posComp, rotComp = compFactory.CreateDimension(playerId),compFactory.CreatePos(playerId),compFactory.CreateRot(playerId)
        dimensionId = dimensionComp.GetEntityDimensionId()
        pos = posComp.GetPos()
        dir = serverApi.GetDirFromRot(rotComp.GetRot())
        itemEntityId = self.CreateEngineItemEntity(itemDict, dimensionId, pos)
        if itemEntityId:
            actorMotionComp = compFactory.CreateActorMotion(itemEntityId)
            actorMotionComp.SetMotion(tuple(i * 0.35 for i in dir))
            self.itemsEntitysTouchCool[itemEntityId] = 40

    def _closeContainer(self, args):
        """关闭容器"""
        playerId = args["__id__"]
        if playerId in self.PlayerContainer:
            del self.PlayerContainer[playerId]

    def GetContainerItem(self, playerId, slot, name, key):
        """
        获取容器内的物品
        - playerId 玩家id
        - slot 格子
        - name 保存名
        - key 键名
        """
        data = UnicodeConvert(json.loads(compFactory.CreateExtraData(playerId).GetExtraData("SliverXentityData")))
        if data.get(name) and data.get(name).get(key):
            return json.loads(data[name][key])
        return {}
        
    def SetContainerItem(self, playerId, slot, name, key, value):
        """
        设置容器内的物品
        - playerId 玩家Id
        - slot 格子
        - name 保存名
        - key 键名
        - vaule 键值
        """
        data = json.loads(compFactory.CreateExtraData(playerId).GetExtraData("SliverXentityData"))
        if name not in data:
            data[name] = {}
        data[name][key] = json.dumps(value)
        compFactory.CreateExtraData(playerId).SetExtraData("SliverXentityData",(json.dumps(data)))
        self.clientCaller(playerId,'reloadContainer',{
            'data' : UnicodeConvert(json.loads(compFactory.CreateExtraData(playerId).GetExtraData("SliverXentityData"))['container_slot'])
        })

    def _OnExchangeItemInContainer(self, args):
        """交换容器内的物品"""
        playerId = args["__id__"]
        fromSlot = args["fromSlot"]
        toSlot = args["toSlot"]
        itemInfo = self.PlayerContainer.get(playerId)
        if not itemInfo:
            return
        itemSlot = itemInfo["itemSlot"]
        fromItem = self.GetContainerItem(playerId, itemSlot, 'container_slot', fromSlot)
        toItem = self.GetContainerItem(playerId, itemSlot, 'container_slot', toSlot)
        self.SetContainerItem(playerId, itemSlot, 'container_slot', fromSlot, toItem)
        self.SetContainerItem(playerId, itemSlot, 'container_slot', toSlot, fromItem)
    
    def _OnMergeItemInContainer(self, args):
        """合并容器内的物品"""
        playerId = args["__id__"]
        fromSlot = args["fromSlot"]
        toSlot = args["toSlot"]
        count = args["count"]
        itemInfo = self.PlayerContainer.get(playerId)
        if not itemInfo:
            return
        itemSlot = itemInfo["itemSlot"]
        fromItem = self.GetContainerItem(playerId, itemSlot, 'container_slot', fromSlot)
        toItem = self.GetContainerItem(playerId, itemSlot, 'container_slot', toSlot)
        fromItem["count"] -= count
        self.SetContainerItem(playerId, itemSlot, 'container_slot', fromSlot, fromItem)
        toItem["count"] += count
        self.SetContainerItem(playerId, itemSlot, 'container_slot', toSlot, toItem)
    
    def _OnMoveItemInContainer(self, args):
        """移动容器内的物品"""
        playerId = args["__id__"]
        fromSlot = args["fromSlot"]
        toSlot = args["toSlot"]
        count = args["count"]
        itemInfo = self.PlayerContainer.get(playerId)
        if not itemInfo:
            return
        itemSlot = itemInfo['itemSlot']
        fromItem = self.GetContainerItem(playerId, itemSlot, 'container_slot', fromSlot)
        toItem = self.GetContainerItem(playerId, itemSlot, 'container_slot', toSlot)
        fromItem["count"] -= count
        toItem = fromItem
        self.SetContainerItem(playerId, itemSlot, 'container_slot', fromSlot, fromItem)
        toItem["count"] = count
        self.SetContainerItem(playerId, itemSlot, 'container_slot', toSlot, toItem)
    
    def _OnMergeContainerItemIntoInv(self, args):
        """移动容器内的物品到玩家背包"""
        playerId = args["__id__"]
        containerSlot = args["containerSlot"]
        invSlot = args["invSlot"]
        count = args["count"]
        itemComp = compFactory.CreateItem(playerId)
        itemInfo = self.PlayerContainer.get(playerId)
        if not itemInfo:
            return
        itemSlot = itemInfo['itemSlot']
        containerItem = self.GetContainerItem(playerId, itemSlot, 'container_slot', containerSlot)
        itemDict = itemComp.GetPlayerItem(minecraftEnum.ItemPosType.INVENTORY, invSlot, True)
        count = min(count, containerItem["count"])
        containerItem["count"] -= count
        self.SetContainerItem(playerId, itemSlot, 'container_slot', containerSlot, containerItem)
        itemComp.SetInvItemNum(invSlot, itemDict["count"] + count)
    
    def _OnInputItemToContainer(self, args):
        """移动背包物品到容器"""
        playerId = args["__id__"]
        fromSlot = args["fromSlot"]
        toSlot = args["toSlot"]
        count = args["count"]
        itemComp = compFactory.CreateItem(playerId)
        itemInfo = self.PlayerContainer.get(playerId)
        if not itemInfo:
            return
        itemSlot = itemInfo['itemSlot']
        itemDict = itemComp.GetPlayerItem(minecraftEnum.ItemPosType.INVENTORY, fromSlot, True)
        itemDict["count"] -= count
        itemComp.SetInvItemNum(fromSlot, itemDict["count"])
        itemDict["count"] = count
        self.SetContainerItem(playerId, itemSlot, 'container_slot', toSlot, itemDict)
    
    def _OnExchangeItemFromContainer(self, args):
        """交换容器和背包的物品"""
        playerId = args["__id__"]
        containerSlot = args["containerSlot"]
        invSlot = args["invSlot"]
        itemComp = compFactory.CreateItem(playerId)
        itemInfo = self.PlayerContainer.get(playerId)
        if not itemInfo:
            return
        itemSlot = itemInfo['itemSlot']
        containerItem = self.GetContainerItem(playerId, itemSlot, 'container_slot', containerSlot)
        invItem = itemComp.GetPlayerItem(minecraftEnum.ItemPosType.INVENTORY, invSlot, True)
        self.SetContainerItem(playerId, itemSlot, 'container_slot', containerSlot, invItem)
        itemComp.SpawnItemToPlayerInv(containerItem, playerId, invSlot)
    
    def _OnPickItemFromContainer(self, args):
        """移动容器内物品到物品栏"""
        playerId = args["__id__"]
        containerSlot = args["containerSlot"]
        invSlot = args["invSlot"]
        count = args["count"]
        itemComp = compFactory.CreateItem(playerId)
        itemInfo = self.PlayerContainer.get(playerId)
        if not itemInfo:
            return
        itemSlot = itemInfo['itemSlot']
        containerItem = self.GetContainerItem(playerId, itemSlot, 'container_slot', containerSlot)
        invItem = containerItem.copy()
        count = min(count, containerItem["count"])
        containerItem["count"] -= count
        invItem["count"] = count
        self.SetContainerItem(playerId, itemSlot, 'container_slot', containerSlot, containerItem)
        itemComp.SpawnItemToPlayerInv(invItem, playerId, invSlot)
    
    def _OnMergeItemIntoContainerInput(self, args):
        """合并物品到容器内"""
        playerId = args["__id__"]
        fromSlot = args["fromSlot"]
        toSlot = args["toSlot"]
        count = args["count"]
        itemComp = compFactory.CreateItem(playerId)
        itemInfo = self.PlayerContainer.get(playerId)
        if not itemInfo:
            return
        itemSlot = itemInfo['itemSlot']
        itemDict = itemComp.GetPlayerItem(minecraftEnum.ItemPosType.INVENTORY, fromSlot, True)
        itemStack = ItemStack(**itemDict)
        itemComp.SetInvItemNum(fromSlot, itemStack.count - count)
        containerItem = self.GetContainerItem(playerId, itemSlot, 'container_slot', toSlot)
        if containerItem:
            containerItem["count"] += count
        else:
            containerItem = itemStack.toItemDict()
        self.SetContainerItem(playerId, itemSlot, 'container_slot', toSlot, containerItem)
