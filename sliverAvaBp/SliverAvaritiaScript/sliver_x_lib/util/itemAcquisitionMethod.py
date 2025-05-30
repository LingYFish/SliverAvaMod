# Embedded file name: mod/common/itemAcquisitionMethod.py


class ItemAcquisitionMethod(object):
    """
    @description 获得物品的方法枚举值
    """
    Unknown = -1
    MethodNone = 0
    PickedUp = 1
    Crafted = 2
    TakenFromChest = 3
    TakenFromEnderchest = 4
    Bought = 5
    Anvil = 6
    Smelted = 7
    Brewed = 8
    Filled = 9
    Trading = 10
    Fishing = 11
    Container = 13
    Feeding = 14