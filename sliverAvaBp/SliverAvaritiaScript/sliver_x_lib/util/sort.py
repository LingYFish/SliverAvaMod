from itemStack import ItemStack
from ..server.core import api as sApi

class ItemSorter(object):
    """
    物品排序插件
    """
    _itemComp = sApi.compFactory.CreateItem(sApi.levelId)

    @classmethod
    def sortBy(cls, stack):
        #type:(ItemStack) -> list
        """
        :type stack: ItemStack
        :rtype: list
        """
        ret = []
        item, data = stack.identifier, stack.data
        namespace, path = item.split(':')
        ret.append(namespace == 'minecraft' or namespace)
        info = cls._itemComp.GetItemBasicInfo(item, data) or {}
        category = info.get('itemCategory')
        ret.append(cls._categoryToIndex.get(category, 99))
        itemType = info.get('itemType')
        ret.append(cls._itemTypeToIndex.get(itemType, 99))
        if itemType is None:
            pass
        elif itemType == 'block':
            ret.append(path.split('_')[-1])
        elif itemType == 'armor':
            ret.append((info['armorSlot'],
             info['armorDefense'],
             info['armorToughness'],
             info['armorKnockbackResistance']))
        elif itemType == 'food':
            ret.append((info['foodNutrition'], info['foodSaturation']))
        elif itemType == '':
            ret.append((info['customItemType'], path.split('_')[-1]))
        elif itemType in cls._tools:
            ret.append((info['itemTierLevel'], info['weaponDamage']))
        idAux = info.get('id_aux', 0)
        if itemType == 'block':
            ret.append(idAux if idAux > 0 else abs(idAux) + 16711680)
        else:
            ret.append(idAux)
        ret.append(stack.tag)
        ret.append(stack.count)
        return ret

    _categoryList = ['construction','nature','equipment','items','custom']
    _categoryToIndex = {_v:_index for _index, _v in enumerate(_categoryList)}
    _itemTypeList = ['block','armor','sword','axe','pickaxe','shovel','hoe','crossbow','trident','fishing_rod','custom_ranged_weapon','clock','compass','shears','food','book','bucket','dye','potion']
    _itemTypeToIndex = {_v:_index for _index, _v in enumerate(_itemTypeList)}
    _tools = {'sword','axe','pickaxe','shovel','hoe'}