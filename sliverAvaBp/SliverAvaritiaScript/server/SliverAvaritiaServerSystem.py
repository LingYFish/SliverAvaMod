from SliverAvaritiaScript.api.server.BaseServerSystem import BaseServerSystem
from SliverAvaritiaScript.modConfig import *
from SliverAvaritiaScript.api.lib.unicodeUtils import UnicodeConvert
from SliverAvaritiaScript.api.lib.itemStack import ItemStack
from SliverAvaritiaScript.modConfig import ItemType
from SliverAvaritiaScript.api.lib import nbt
import mod.server.extraServerApi as serverApi
import json
import uuid
compFactory = serverApi.GetEngineCompFactory()
levelId = serverApi.GetLevelId()
minecraftEnum = serverApi.GetMinecraftEnum()
class Armor:

    def __init__(self,System):
        self.server = System
        self.PlayerflyState = {}
        self.equipedArmors = {}

    def helmetEquipped(self, entityId):
        allEquip = self.equipedArmors.get(entityId)
        if allEquip:
            ret = ItemType.INFINITY_HELMET in allEquip
            if ret:
                return ret
        itemComp = compFactory.CreateItem(entityId)
        item = itemComp.GetEntityItem(minecraftEnum.ItemPosType.ARMOR, 0)
        if item and item["newItemName"] == ItemType.INFINITY_HELMET:
            return True
        return False
    
    def chestplateEquipped(self, entityId):
        allEquip = self.equipedArmors.get(entityId)
        if allEquip:
            ret = ItemType.INFINITY_CHESTPLATE in allEquip
            if ret:
                return ret
        itemComp = compFactory.CreateItem(entityId)
        item = itemComp.GetEntityItem(minecraftEnum.ItemPosType.ARMOR, 1)
        if item and item["newItemName"] == ItemType.INFINITY_CHESTPLATE:
            return True
        return False
    
    def leggingsEquipped(self, entityId):
        allEquip = self.equipedArmors.get(entityId)
        if allEquip:
            ret = ItemType.INFINITY_LEGGINGS in allEquip
            if ret:
                return ret
        itemComp = compFactory.CreateItem(entityId)
        item = itemComp.GetEntityItem(minecraftEnum.ItemPosType.ARMOR, 2)
        if item and item["newItemName"] == ItemType.INFINITY_LEGGINGS:
            return True
        return False
    
    def bootsEquipped(self, entityId):
        allEquip = self.equipedArmors.get(entityId)
        if allEquip:
            ret = ItemType.INFINITY_BOOTS in allEquip
            if ret:
                return ret
        itemComp = compFactory.CreateItem(entityId)
        item = itemComp.GetEntityItem(minecraftEnum.ItemPosType.ARMOR, 3)
        if item and item["newItemName"] == ItemType.INFINITY_BOOTS:
            return True
        return False
    
    def setEquipItem(self, entityId, armorName):
        if entityId not in self.equipedArmors:
            self.equipedArmors[entityId] = set()
        self.equipedArmors[entityId].add(armorName)
    
    def setUnequipItem(self, entityId, armorName):
        if entityId not in self.equipedArmors:
            self.equipedArmors[entityId] = set()
        self.equipedArmors[entityId].discard(armorName)

class SliverAvaritiaServerSystem(BaseServerSystem):
    gameComp = compFactory.CreateGame(levelId)
    remove_effect = ("wither","bad_omen","nausea","slowness","hunger","levitation","blindness","instant_damage","mining_fatigue","poison","weakness","fatal_poison","empty")
    chestplate_damage_cancel = ('stalagmite', 'fall')
    leggings_damage_cancel = ('fire', 'fire_tick', 'magma', 'lava')

    def __init__(self, namespace, systemName):
        BaseServerSystem.__init__(self, namespace, systemName)
        self.armor = Armor(self)
        self.addListenEvent(self.OnScriptTickServer, eventName="OnScriptTickServer")
        self.addListenEvent(self.OnNewArmorExchangeServerEvent, eventName="OnNewArmorExchangeServerEvent")
        self.addListenEvent(self.DamageEvent, eventName="DamageEvent")
        self.addListenEvent(self.HealthChangeBeforeServerEvent, eventName="HealthChangeBeforeServerEvent")
        self.addListenEvent(self.requestFlyState, modName, "SliverAvaritiaClientSystem", "requestFlyState")

    def DamageEvent(self, args):
        entityId = args['entityId']
        cause = args['cause']
        if self.isAllEquipped(entityId):
            args['knock'] = False
            args['ignite'] = False
            args['damage'] = 0
            args['damage_f'] = 0.0
        if self.armor.chestplateEquipped(entityId):
            if cause in self.chestplate_damage_cancel: #盔甲免疫的伤害
                args['knock'] = False
                args['damage'] = 0
                args['damage_f'] = 0.0
        if self.armor.leggingsEquipped(entityId):
            if cause in self.leggings_damage_cancel: #护腿免疫的伤害
                args['knock'] = False
                args['damage'] = 0
                args['damage_f'] = 0.0
    
    def HealthChangeBeforeServerEvent(self, args):
        entityId = args['entityId']
        if self.isAllEquipped(entityId):
            if args['from'] - args['to'] > 0:
                args["cancel"] = True
    
    def isAllEquipped(self, entityId):
        return self.armor.helmetEquipped(entityId) and self.armor.chestplateEquipped(entityId) and self.armor.leggingsEquipped(entityId) and self.armor.bootsEquipped(entityId)
    
    def OnNewArmorExchangeServerEvent(self, args):
        playerId = args["playerId"]
        slot = args["slot"]
        oldArmorDict = args["oldArmorDict"]
        newArmorDict = args["newArmorDict"]
        if slot == minecraftEnum.ArmorSlotType.HEAD:
            if oldArmorDict and oldArmorDict["newItemName"] == ItemType.INFINITY_HELMET:
                self.unequipHelmet(playerId)
            if newArmorDict and newArmorDict["newItemName"] == ItemType.INFINITY_HELMET:
                self.equipHelmet(playerId)
        elif slot == minecraftEnum.ArmorSlotType.BODY:
            if oldArmorDict and oldArmorDict["newItemName"] == ItemType.INFINITY_CHESTPLATE:
                self.unequipChestplate(playerId)
            if newArmorDict and newArmorDict["newItemName"] == ItemType.INFINITY_CHESTPLATE:
                self.equipChestplate(playerId)
        elif slot == minecraftEnum.ArmorSlotType.LEG:
            if oldArmorDict and oldArmorDict["newItemName"] == ItemType.INFINITY_LEGGINGS:
                self.unequipLeggings(playerId)
            if newArmorDict and newArmorDict["newItemName"] == ItemType.INFINITY_LEGGINGS:
                self.equipLeggings(playerId)
        elif slot == minecraftEnum.ArmorSlotType.FOOT:
            if oldArmorDict and oldArmorDict["newItemName"] == ItemType.INFINITY_BOOTS:
                self.unequipBoots(playerId)
            if newArmorDict and newArmorDict["newItemName"] == ItemType.INFINITY_BOOTS:
                self.equipBoots(playerId)
        if self.isAllEquipped(playerId):
            pass
    
    def equipHelmet(self, playerId):
        self.armor.setEquipItem(playerId, ItemType.INFINITY_HELMET)

    def unequipHelmet(self, playerId):
        self.armor.setUnequipItem(playerId, ItemType.INFINITY_HELMET)

    def equipChestplate(self, playerId):
        self.armor.setEquipItem(playerId, ItemType.INFINITY_CHESTPLATE)

    def unequipChestplate(self, playerId):
        self.armor.setUnequipItem(playerId, ItemType.INFINITY_CHESTPLATE)
        flyComp = compFactory.CreateFly(playerId)
        gameComp = compFactory.CreateGame(levelId)
        if flyComp.IsPlayerCanFly() and gameComp.GetPlayerGameType(playerId) != minecraftEnum.GameType.Creative:
            flyComp.ChangePlayerFlyState(False, False)

    def equipLeggings(self, playerId):
        self.armor.setEquipItem(playerId, ItemType.INFINITY_LEGGINGS)

    def unequipLeggings(self, playerId):
        self.armor.setUnequipItem(playerId, ItemType.INFINITY_LEGGINGS)

    def equipBoots(self, playerId):
        self.armor.setEquipItem(playerId, ItemType.INFINITY_BOOTS)

    def unequipBoots(self, playerId):
        self.armor.setUnequipItem(playerId, ItemType.INFINITY_BOOTS)
        attrComp = compFactory.CreateAttr(playerId)
        gravityComp = compFactory.CreateGravity(playerId)
        attrComp.SetStepHeight(0.5625)
        gravityComp.SetJumpPower(0.42)
        attrComp.SetAttrValue(minecraftEnum.AttrType.SPEED, 0.1)
    
    def requestFlyState(self, args):
        playerId = args["__id__"]
        self.clientCaller(playerId, "syncFlyState", {"state": self.flyState})
    
    def OnScriptTickServer(self):
        for playerId in serverApi.GetPlayerList():
            flyComp = compFactory.CreateFly(playerId)
            isFlying = flyComp.IsPlayerFlying()
            self.armor.PlayerflyStateflyState[playerId] = isFlying
        self.CallAllclient("syncFlyState", {"state": self.armor.PlayerflyStateflyState})
        for entityId in self.armor.equipedArmors:
            armors = self.armor.equipedArmors[entityId]
            if ItemType.INFINITY_HELMET in armors:
                attrComp = compFactory.CreateAttr(entityId)
                breathComp = compFactory.CreateBreath(entityId)
                effectComp = compFactory.CreateEffect(entityId)
                breathComp.SetCurrentAirSupply(300)
                attrComp.SetAttrValue(minecraftEnum.AttrType.HUNGER, 20)
                attrComp.SetAttrValue(minecraftEnum.AttrType.SATURATION, 20)
                effectComp.AddEffectToEntity(minecraftEnum.EffectType.NIGHT_VISION, 15, 0, False)
            if ItemType.INFINITY_CHESTPLATE in armors:
                effectComp = compFactory.CreateEffect(entityId)
                flyComp = compFactory.CreateFly(entityId)
                for effect in self.remove_effect:
                    if effectComp.HasEffect(effect):
                        effectComp.RemoveEffectFromEntity(effect)
                if not flyComp.IsPlayerCanFly():
                    flyComp.ChangePlayerFlyState(True, False)
            if ItemType.INFINITY_BOOTS in armors:
                attrComp = compFactory.CreateAttr(entityId)
                gravityComp = compFactory.CreateGravity(entityId)
                attrComp.SetStepHeight(1.0625)
                attrComp.SetAttrValue(minecraftEnum.AttrType.SPEED, 0.2)
                gravityComp.SetJumpPower(0.82)