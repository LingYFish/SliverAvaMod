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