from core import api
from ..util.itemStack import ItemStack
from ..util import minecraftEnum

def clearSlotItem(playerId, posType, slot):
    #type: (str,int,int) -> ItemStack
    """
    | 清空玩家某个槽位的物品

    ----------------

    - str playerId: 玩家ID
    - int posType: 槽位类型
    - int slot: 槽位编号
    - dict|None return: 清除前的物品ItemStack

    """
    itemComp = api.compFactory.CreateItem(playerId)
    item = itemComp.GetPlayerItem(posType, slot, True)
    itemComp.SetPlayerAllItems({(posType, slot): None})
    return ItemStack(**item) if type(item) is dict else ItemStack()

def getItemSlotPos(entityId, posType, itemId, itemAux=-1145, count=-1145):
    #type: (str,int,str,int,str) -> list[int]
    """
    | 获取物品所在实体的槽位。

    ----------------

    - str entityId: 生物的实体ID
    - int posType: ItemPosType枚举
    - str itemId: 物品ID
    - int itemAux: 物品附加值 默认为任意附加值
    - int count: 搜索的物品数量 不填写默认全部
    - list[int] return: 物品所在槽位的列表，获取不到返回空列表 

    """
    isPlayer = (api.compFactory.CreateEngineType(entityId).GetEngineTypeStr() == "minecraft:player")
    itemComp = api.compFactory.CreateItem(entityId)
    result = []
    for slot in range(minecraftEnum.ItemPosType.POS_SIZE[posType]):
        if len(result) >= count and count != -1145:break
        itemDict = itemComp.GetPlayerItem(posType, slot) if isPlayer else itemComp.GetEntityItem(posType, slot)
        itemStack = ItemStack(**itemDict) if isinstance(itemDict, dict) else None
        if itemDict and itemStack and itemStack.identifier == itemId and (itemAux == -1145 or itemStack.data == itemAux):
            result.append(slot)
    return result

def changeSlotItemCount(playerId, posType=minecraftEnum.ItemPosType.CARRIED, slot=0, changeCount=1):
    #type: (str,int,int,str) -> None
    """
    | 改变玩家槽位的物品数量

    ----------------

    - str playerId: 玩家ID
    - int posType: 槽位类型 默认为 CARRIED
    - int slot: 槽位默认为0
    - int changeCount: 改变数量默认为1
    - None return: 无

    """
    itemComp = api.compFactory.CreateItem(playerId)
    item = itemComp.GetPlayerItem(posType, slot, True)
    item['count'] += changeCount
    if item['count'] <= 0:
        item = None
    itemComp.SetPlayerAllItems({(posType, slot): item})

def deductSlotItem(playerId, itemId, itemAux=-1145, count=1):
    #type: (str,str,int,int) -> bool
    """
    | 扣除玩家背包中指定数量的物品

    ----------------

    - str playerId: 玩家ID
    - str itemId: 物品ID
    - int itemAux: 物品附加值
    - int count: 扣除数量
    - bool return: 扣除是否成功

    """
    comp,items_dict_map = api.compFactory.CreateItem(playerId),{}
    items = comp.GetPlayerAllItems(minecraftEnum.ItemPosType.INVENTORY, True)
    for i, item in enumerate(items):
        if not item:continue
        itemStack = ItemStack(**item)
        if itemStack.identifier != itemId or (itemAux != -1145 and itemStack.data != itemAux):continue
        c = min(itemStack.count, count)
        itemStack.count -= c
        count -= c
        items_dict_map[(minecraftEnum.ItemPosType.INVENTORY, i)] = itemStack.__dict__ if itemStack.count > 0 else None
        if count <= 0:break
    if items_dict_map:comp.SetPlayerAllItems(items_dict_map)
    return count <= 0

def carriedIsItem(entityId,itemId,itemAux=-1145):
    #type: (str,str,int) -> bool
    """
    | 实体主手是否是指定物品

    ----------------

    - str entityId: 实体ID
    - str itemId: 物品ID
    - int itemAux: 物品附加值
    - bool return: 是否是当前物品

    """
    itemComp = api.compFactory.CreateItem(entityId)
    itemDict = itemComp.GetEntityItem(minecraftEnum.ItemPosType.CARRIED, 0)
    if not itemDict:
        return False
    itemStack = ItemStack(**itemDict)
    return itemStack.identifier == itemId and (itemAux== -1145 or itemStack.data == itemAux)

def hasItem(entityId,itemId,itemAux=-1145):
    #type: (str,str,int) -> bool
    """
    | 实体是否拥有指定物品

    ----------------

    - str entityId: 实体ID
    - str itemId: 物品ID
    - int itemAux: 物品附加值
    - bool return: 是否是当前物品

    """
    isPlayer = (api.compFactory.CreateEngineType(entityId).GetEngineTypeStr() == "minecraft:player")
    itemComp = api.compFactory.CreateItem(entityId)
    for slot in range(minecraftEnum.ItemPosType.POS_SIZE[minecraftEnum.ItemPosType.INVENTORY]):
        itemDict = itemComp.GetPlayerItem(minecraftEnum.ItemPosType.INVENTORY, slot) if isPlayer else itemComp.GetEntityItem(minecraftEnum.ItemPosType.INVENTORY, slot)
        itemStack = ItemStack(**itemDict) if isinstance(itemDict, dict) else None
        if itemDict and itemStack and itemStack.identifier == itemId and (itemAux == -1145 or itemStack.data == itemAux):return True
    for slot in range(minecraftEnum.ItemPosType.POS_SIZE[minecraftEnum.ItemPosType.ARMOR]):
        itemDict = itemComp.GetPlayerItem(minecraftEnum.ItemPosType.ARMOR, slot) if isPlayer else itemComp.GetEntityItem(minecraftEnum.ItemPosType.ARMOR, slot)
        itemStack = ItemStack(**itemDict) if isinstance(itemDict, dict) else None
        if itemDict and itemStack and itemStack.identifier == itemId and (itemAux == -1145 or itemStack.data == itemAux):return True
    itemDict = itemComp.GetPlayerItem(minecraftEnum.ItemPosType.OFFHAND, slot) if isPlayer else itemComp.GetEntityItem(minecraftEnum.ItemPosType.OFFHAND, slot)
    itemStack = ItemStack(**itemDict) if isinstance(itemDict, dict) else None
    if itemDict and itemStack and itemStack.identifier == itemId and (itemAux == -1145 or itemStack.data == itemAux):return True
    return False