import copy
import random
from . import nbt
"""感谢男娘AlwnRrr提供的ItemStack"""
class ItemStack(object):
    _itemMaxDamage = {}
    _itemMaxStackSize = {}

    def __init__(self, **kwargs):
        self.identifier = kwargs.get('newItemName', 'minecraft:air') #type: str
        self.data = kwargs.get('newAuxValue', 0) #type: int
        self.count = kwargs.get('count', 1) #type: int
        self.tag = kwargs.get('userData', None) or {} #type: dict[str:dict]
        self.extraId = kwargs.get('extraId', '') #type: str
        self.durability = kwargs.get('durability',0) #type: int
        self._tagConvert()

    def __eq__(self, other):
        return (isinstance(other, ItemStack) and self.identifier == other.identifier and self.data == other.data and self.tag == other.tag)

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash('{}:{}'.format(self.identifier,self.data))

    def isEmpty(self):
        return self.identifier == 'minecraft:air' or self.count <= 0

    def clone(self, **kwargs):
        return ItemStack(
            newItemName=kwargs.get('newItemName', self.identifier),
            newAuxValue=kwargs.get('newAuxValue', self.data),
            count=kwargs.get('count', self.count),
            userData=copy.deepcopy(kwargs.get('userData', self.tag))
        )

    def toItemDict(self):
        if self.isEmpty():
            return {}
        self._removeZeroDamage()
        itemDict = {
            'newAuxValue': self.data,
            'count': self.count,
            'userData': self.tag if self.tag else None,
            'extraId' : self.extraId
        }
        if self.getTag('ModId') and self.getTag('ModItemId'):
            itemDict['modId'] = self.getTag('ModId')
            itemDict['modItemId'] = self.getTag('ModItemId')
        else:
            itemDict['newItemName'] = self.identifier
        if not self.isDisplayShowInHand():
            itemDict['showInHand'] = False
        return itemDict

    def toSimplestItemDict(self):
        if self.isEmpty():
            return {}
        self._removeZeroDamage()
        return {
            'newItemName': self.identifier,
            'newAuxValue': self.data,
            'count': self.count,
            'userData': self.tag if self.tag else None,
            'extraId' : self.extraId
        }

    def hasTag(self, key):
        return key in self.tag

    def getTag(self, key, default=None):
        return self.tag.get(key, {}).get('__value__', default)

    def setTag(self, key, tagType, value):
        self.tag[key] = {'__type__': tagType, '__value__': value}

    def delTag(self, key):
        self.tag.pop(key, None)

    def getDamage(self):
        return self.getTag('Damage', 0)

    def setDamage(self, damage):
        self.setTag('Damage', nbt.TAG_Int, damage)

    def delDamage(self):
        self.delTag('Damage')

    def isUnbreakable(self):
        return bool(self.getTag('Unbreakable', 0))

    def setUnbreakable(self, isUnbreakable=True):
        self.setTag('Unbreakable', nbt.TAG_Byte, int(isUnbreakable))

    def delUnbreakable(self):
        self.delTag('Unbreakable')

    def getRepairCost(self):
        return self.getTag('RepairCost', 0)

    def setRepairCost(self, repairCost):
        self.setTag('RepairCost', nbt.TAG_Int, repairCost)

    def delRepairCost(self):
        self.delTag('RepairCost')

    def getEnchantData(self):
        return [(ench.get('id', {}).get('__value__', 0),
                 ench.get('lvl', {}).get('__value__', 0),
                 ench.get('modEnchant', {}).get('__value__', ''))
                for ench in self.tag.get('ench', [])]

    def setEnchantData(self, enchantData):
        self.tag['ench'] = [
            {'id': {'__type__': nbt.TAG_Short, '__value__': enchId},
             'lvl': {'__type__': nbt.TAG_Short, '__value__': enchLevel},
             'modEnchant': {'__type__': nbt.TAG_String, '__value__': enchIdentifier}}
            for enchId, enchLevel, enchIdentifier in enchantData
        ]

    def delEnchantData(self):
        self.delTag('ench')

    def hasDisplayAttr(self, key):
        return 'display' in self.tag and key in self.tag['display']

    def getDisplayAttr(self, key, default):
        return self.tag.get('display', {}).get(key, {}).get('__value__', default)

    def setDisplayAttr(self, key, tagType, value):
        self.tag.setdefault('display', {})[key] = {'__type__': tagType, '__value__': value}

    def delDisplayAttr(self, key):
        if 'display' in self.tag and key in self.tag['display']:
            self.tag['display'].pop(key)
            if not self.tag['display']:
                self.tag.pop('display')

    def getDisplayName(self):
        return self.getDisplayAttr('Name', '')

    def setDisplayName(self, name):
        self.setDisplayAttr('Name', nbt.TAG_String, name)

    def delDisplayName(self):
        self.delDisplayAttr('Name')

    def getDisplayLore(self):
        return [i['__value__'] for i in self.tag.get('display', {}).get('Lore', [])]

    def setDisplayLore(self, lore):
        self.tag.setdefault('display', {})['Lore'] = [
            {'__type__': nbt.TAG_String, '__value__': i} for i in lore
        ]

    def delDisplayLore(self):
        self.delDisplayAttr('Lore')

    def isDisplayShowInHand(self):
        return bool(self.getDisplayAttr('ShowInHand', 1))

    def setDisplayShowInHand(self, isShowInHand):
        self.setDisplayAttr('ShowInHand', nbt.TAG_Byte, int(isShowInHand))

    def delDisplayShowInHand(self):
        self.delDisplayAttr('ShowInHand')

    def getItemLock(self):
        return self.getTag('minecraft:item_lock', 0)

    def setItemLock(self, lockType):
        self.setTag('minecraft:item_lock', nbt.TAG_Byte, lockType)

    def delItemLock(self):
        self.delTag('minecraft:item_lock')

    def isLockInSlot(self):
        return self.getItemLock() == 1

    def isLockInInventory(self):
        return self.getItemLock() == 2

    def setLockInSlot(self):
        self.setItemLock(1)

    def setLockInInventory(self):
        self.setItemLock(2)

    def isKeepOnDeath(self):
        return bool(self.getTag('minecraft:keep_on_death', 0))

    def setKeepOnDeath(self, keepOnDeath):
        self.setTag('minecraft:keep_on_death', nbt.TAG_Byte, int(keepOnDeath))

    def delKeepOnDeath(self):
        self.delTag('minecraft:keep_on_death')

    def getItemCustomTips(self):
        return self.getTag('ItemCustomTips', '')

    def setItemCustomTips(self, customTips):
        self.setTag('ItemCustomTips', nbt.TAG_String, customTips)

    def delItemCustomTips(self):
        self.delTag('ItemCustomTips')

    def getItemExtraId(self):
        return self.extraId

    def setItemExtraId(self, extraId):
        self.extraId = extraId

    def delItemExtraId(self):
        self.extraId = ''

    def getModTierLevel(self):
        return self.getTag('ModTierLevel')

    def setModTierLevel(self, tierLevel):
        self.setTag('ModTierLevel', nbt.TAG_Int, tierLevel)

    def delModTierLevel(self):
        self.delTag('ModTierLevel')

    def getModTierSpeed(self):
        return self.getTag('ModTierSpeed')

    def setModTierSpeed(self, tierSpeed):
        self.setTag('ModTierSpeed', nbt.TAG_Float, tierSpeed)

    def delModTierSpeed(self):
        self.delTag('ModTierSpeed')

    def getModAttackDamage(self):
        return self.getTag('ModAttackDamage')

    def setModAttackDamage(self, attackDamage):
        self.setTag('ModAttackDamage', nbt.TAG_Int, attackDamage)

    def delModAttackDamage(self):
        self.delTag('ModAttackDamage')

    def getModMaxStackSize(self):
        return self.getTag('ModMaxStackSize')

    def setModMaxStackSize(self, maxStackSize):
        self.setTag('ModMaxStackSize', nbt.TAG_Byte, maxStackSize)

    def delModMaxStackSize(self):
        self.delTag('ModMaxStackSize')

    def getModMaxDamage(self):
        return self.getTag('ModMaxDamage')

    def setModMaxDamage(self, maxDamage):
        self.setTag('ModMaxDamage', nbt.TAG_Short, maxDamage)

    def delModMaxDamage(self):
        self.delTag('ModMaxDamage')

    def getModShieldDefenceAngle(self):
        return (self.getTag('ModShieldDefenceAngleLeft'), self.getTag('ModShieldDefenceAngleRight'))

    def setModShieldDefenceAngle(self, angleLeft, angleRight):
        self.setTag('ModShieldDefenceAngleLeft', nbt.TAG_Float, angleLeft)
        self.setTag('ModShieldDefenceAngleRight', nbt.TAG_Float, angleRight)

    def delModShieldDefenceAngle(self):
        self.delTag('ModShieldDefenceAngleLeft')
        self.delTag('ModShieldDefenceAngleRight')

    def split(self, amount):
        i = min(amount, self.count)
        itemStack = self.clone(count=i)
        self.count -= i
        return itemStack

    def addEnchant(self, enchId, enchLevel, enchIdentifier=''):
        enchantData = self.getEnchantData()
        enchantData = [i for i in enchantData if not (i[0] == enchId and i[2] == enchIdentifier)]
        enchantData.append((enchId, enchLevel, enchIdentifier))
        self.setEnchantData(enchantData)

    def removeEnchant(self, enchId, enchIdentifier=''):
        enchantData = self.getEnchantData()
        enchantData = [i for i in enchantData if not (i[0] == enchId and i[2] == enchIdentifier)]
        self.setEnchantData(enchantData) if enchantData else self.delEnchantData()

    def hasEnchant(self, enchId, enchIdentifier=''):
        return any(i[0] == enchId and i[2] == enchIdentifier for i in self.getEnchantData())

    def getEnchantLevel(self, enchId, enchIdentifier=''):
        for i in self.getEnchantData():
            if i[0] == enchId and i[2] == enchIdentifier:
                return i[1]
        return None

    def getMaxDamage(self, itemComp):
        maxDamage = self.getModMaxDamage()
        if maxDamage is not None:
            return maxDamage
        key = (self.identifier, self.data)
        if key not in self._itemMaxDamage:
            basicInfo = itemComp.GetItemBasicInfo(self.identifier, self.data)
            self._itemMaxDamage[key] = basicInfo['maxDurability'] if basicInfo else 0
        return self._itemMaxDamage[key]

    def getMaxStackSize(self, itemComp):
        maxStackSize = self.getModMaxStackSize()
        if maxStackSize is not None:
            return maxStackSize
        key = (self.identifier, self.data)
        if key not in self._itemMaxStackSize:
            basicInfo = itemComp.GetItemBasicInfo(self.identifier, self.data)
            self._itemMaxStackSize[key] = basicInfo['maxStackSize'] if basicInfo else 64
        return self._itemMaxStackSize[key]

    def addDamage(self, amount, itemComp, durabilityEnchId=17, ignoreUnbreakable=False):
        if not ignoreUnbreakable and self.isUnbreakable():
            return
        damage = self.getDamage()
        maxDamage = self.getMaxDamage(itemComp)
        if maxDamage <= 0:
            return
        enchLvl = self.getEnchantLevel(durabilityEnchId)
        if enchLvl is not None and enchLvl > 0:
            for _ in range(amount):
                if random.random() < 1.0 / (enchLvl + 1):
                    damage += 1
        else:
            damage += amount
        self.setDamage(damage)
        if damage >= maxDamage:
            self.count -= 1
            self.setDamage(0)

    def _tagConvert(self):
        if not isinstance(self.tag, dict):
            self.tag = {}

    def _removeZeroDamage(self):
        if self.getDamage() == 0:
            self.delDamage()