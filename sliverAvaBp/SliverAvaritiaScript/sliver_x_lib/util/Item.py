from . import minecraftEnum
air = ("minecraft:air", "air")

def isItem(item1, item2):
    """辅助功能 -- 判断是否是同一个物品"""
    if not item1 or not item2:
        return False
    if item1.get('newItemName', 'item1') != item2.get('newItemName', 'item2'):
        return False
    if item1.get('newAuxValue') != item2.get('newAuxValue'):
        return False
    if item1.get('userData') != item2.get('userData'):
        return False
    return True

def setNamespace(name, namespace="minecraft"):
    """
    设置物品的命名空间
    """
    if not name:
        return ""
    name_lst = name.split(":")
    if ":" not in name:
        name_lst.insert(0, "")
    name_lst[0] = namespace
    return ":".join(name_lst)

def getItemCount(player_id, name,compfactory, aux=-1):
    count = 0
    items = compfactory.CreateItem(player_id).GetPlayerAllItems(minecraftEnum.ItemPosType.INVENTORY)
    for item in items:
        if isEmpty(item):
            continue
        if item['newItemName'] == name and (aux == -1 or item['newAuxValue'] == aux):
            count += item['count']
    return count

def isEmpty(item, zero_is_emp=True):
    """
    是否是空物品s
    """
    return (not item or ('newItemName' not in item and 'itemName' not in item) or (zero_is_emp and item.get('count', 1) <= 0) or item.get('newItemName') in air or item.get('itemName') in air )