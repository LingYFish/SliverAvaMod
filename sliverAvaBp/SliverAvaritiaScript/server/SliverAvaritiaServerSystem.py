from SliverAvaritiaScript.api.server.BaseServerSystem import BaseServerSystem
from SliverAvaritiaScript.modConfig import *
from SliverAvaritiaScript.api.lib.unicodeUtils import UnicodeConvert
from SliverAvaritiaScript.api.lib.itemStack import ItemStack
from SliverAvaritiaScript.modConfig import ItemType
from SliverAvaritiaScript.api.lib import nbt
import random
import mod.server.extraServerApi as serverApi
import json
import math
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
            if ret:return ret
        itemComp = compFactory.CreateItem(entityId)
        item = itemComp.GetEntityItem(minecraftEnum.ItemPosType.ARMOR, 0)
        if item and item["newItemName"] == ItemType.INFINITY_HELMET:return True
        return False
    
    def chestplateEquipped(self, entityId):
        allEquip = self.equipedArmors.get(entityId)
        if allEquip:
            ret = ItemType.INFINITY_CHESTPLATE in allEquip
            if ret:return ret
        itemComp = compFactory.CreateItem(entityId)
        item = itemComp.GetEntityItem(minecraftEnum.ItemPosType.ARMOR, 1)
        if item and item["newItemName"] == ItemType.INFINITY_CHESTPLATE:return True
        return False
    
    def leggingsEquipped(self, entityId):
        allEquip = self.equipedArmors.get(entityId)
        if allEquip:
            ret = ItemType.INFINITY_LEGGINGS in allEquip
            if ret:return ret
        itemComp = compFactory.CreateItem(entityId)
        item = itemComp.GetEntityItem(minecraftEnum.ItemPosType.ARMOR, 2)
        if item and item["newItemName"] == ItemType.INFINITY_LEGGINGS:return True
        return False
    
    def bootsEquipped(self, entityId):
        allEquip = self.equipedArmors.get(entityId)
        if allEquip:
            ret = ItemType.INFINITY_BOOTS in allEquip
            if ret:return ret
        itemComp = compFactory.CreateItem(entityId)
        item = itemComp.GetEntityItem(minecraftEnum.ItemPosType.ARMOR, 3)
        if item and item["newItemName"] == ItemType.INFINITY_BOOTS:return True
        return False
    
    def setEquipItem(self, entityId, armorName):
        if entityId not in self.equipedArmors:self.equipedArmors[entityId] = set()
        self.equipedArmors[entityId].add(armorName)
    
    def setUnequipItem(self, entityId, armorName):
        if entityId not in self.equipedArmors:self.equipedArmors[entityId] = set()
        self.equipedArmors[entityId].discard(armorName)

class SliverAvaritiaServerSystem(BaseServerSystem):
    gameComp = compFactory.CreateGame(levelId)
    remove_effect = ("wither","bad_omen","nausea","slowness","hunger","levitation","blindness","instant_damage","mining_fatigue","poison","weakness","fatal_poison","empty")

    def __init__(self, namespace, systemName):
        BaseServerSystem.__init__(self, namespace, systemName)
        self.armor = Armor(self)
        self.cooldown = {}
        self.search = []
        self.destroyBlockQueue = [] # LIFO
        self.replaceBlockQueue = {}
        itemComp = compFactory.CreateItem(levelId)
        itemComp.GetUserDataInEvent("InventoryItemChangedServerEvent")
        compFactory.CreateGame(levelId).AddRepeatedTimer(0.05, self.coolDownUpdate)
        serverApi.AddEntityTickEventWhiteList(EntityType.GAPING_VOID)
        self.search = []
        self.addListenEvent(self.OnScriptTickServer, eventName="OnScriptTickServer")
        self.addListenEvent(self.LIFO, eventName="OnScriptTickServer")
        self.addListenEvent(self.OnNewArmorExchangeServerEvent, eventName="OnNewArmorExchangeServerEvent")
        self.addListenEvent(self.DamageEvent, eventName="DamageEvent")
        self.addListenEvent(self.HealthChangeBeforeServerEvent, eventName="HealthChangeBeforeServerEvent")
        self.addListenEvent(self.requestFlyState, modName, "SliverAvaritiaClientSystem", "requestFlyState")
        self.addListenEvent(self.inventoryItemChangedServer, eventName="InventoryItemChangedServerEvent")
        self.addListenEvent(self.EntityDieLootTableServer, eventName="EntityDieLoottableServerEvent")
        self.addListenEvent(self.playerAttackEntity, eventName="PlayerAttackEntityEvent")
        self.addListenEvent(self.ProjectileDoHitEffectEvent, eventName="ProjectileDoHitEffectEvent")
        self.addListenEvent(self.EntityTickServerEvent,eventName='EntityTickServerEvent')
        self.addListenEvent(self.ServerItemTryUseEvent,eventName='ServerItemTryUseEvent')
        self.addListenEvent(self.startUsingBow, modName, "SliverAvaritiaClientSystem", "startUsingBow")
        self.addListenEvent(self.stopUsingBow, modName, "SliverAvaritiaClientSystem", "stopUsingBow")
        self.addListenEvent(self.DestroyBlockEventPickaxe,eventName='DestroyBlockEvent')
        self.addListenEvent(self.DestroyBlockEventShovel,eventName='DestroyBlockEvent')
        self.addListenEvent(self.DestroyBlockEventAxe,eventName='DestroyBlockEvent')
    
    def DestroyBlockEventAxe(self,args):
        pos = (args['x'],args['y'],args['z'])
        dimension_id = args['dimensionId']
        player_id = args['playerId']
        pos = (args['x'], args['y'], args['z'], dimension_id)
        ItemCreate = compFactory.CreateItem(player_id).GetPlayerItem(minecraftEnum.ItemPosType.CARRIED, 0)
        if ItemCreate and ItemCreate['newItemName'] == ItemType.INFINITY_AXE and compFactory.CreatePlayer(player_id).isSneaking():
            if any([s in args['fullName'] for s in ['log']]):
                self.destroyBlockQueue.insert(0, pos)
            if compFactory.CreateBlockInfo(levelId).GetBlockNew((pos[0],pos[1]-1,pos[2]), pos[-1])['name'] in ["minecraft:grass","minecraft:drit"]:
                self.replaceBlockQueue[player_id] = [{
                    "replace" : ["minecraft:grass","minecraft:drit"],
                    "count" : 0,
                    "pos" : [pos]
                }]

    def LIFO(self):
        if not self.destroyBlockQueue: return
        pos = self.destroyBlockQueue.pop()
        compFactory.CreateBlockInfo(levelId).SetBlockNew(pos[:3], {
            'name': 'minecraft:air',
            'aux': 0
        }, 1, pos[-1], True)
        for offset in [(0, 0, 1, 0),(0, 0, -1, 0),(0, 1, 0, 0),(0, -1, 0, 0),(1, 0, 0, 0),(-1, 0, 0, 0),]:
            nextPos = tuple((p + offset[i] for i, p in enumerate(pos)))
            nextBlock = compFactory.CreateBlockInfo(levelId).GetBlockNew(nextPos[:3], nextPos[-1])
            if any([s in nextBlock['name'] for s in ['log']]):
                self.destroyBlockQueue.insert(0, nextPos) 
        for playerId,data in self.replaceBlockQueue.items():
            data['count'] += 1
            if data['count'] >= 100:
                del self.replaceBlockQueue[playerId]
                return
            for offset in [(0, 0, 1, 0),(0, 0, -1, 0),(0, 1, 0, 0),(0, -1, 0, 0),(1, 0, 0, 0),(-1, 0, 0, 0),]:
                nextPos = tuple((p + offset[i] for i, p in enumerate(pos)))
                nextBlock = compFactory.CreateBlockInfo(levelId).GetBlockNew(nextPos[:3], nextPos[-1])
                if any([s in nextBlock['name'] for s in [data['replace'][0]]]):
                    data['pos'].insert(0, nextPos) 
            compFactory.CreateBlockInfo(levelId).SetBlockNew(pos[:3], {
                'name': data['replace'][1],
                'aux': 0
            }, 1, pos[-1], True)

    def DestroyBlockEventPickaxe(self,args):
        pos = (args['x'],args['y'],args['z'])
        dimension_id = args['dimensionId']
        player_id = args['playerId']
        ItemCreate = compFactory.CreateItem(player_id).GetPlayerItem(minecraftEnum.ItemPosType.CARRIED, 0)
        if ItemCreate and ItemCreate['newItemName'] == ItemType.INFINITY_PICKAXE_HAMMER:
            def destory_and_get_items():
                start_x = pos[0] - 8
                end_x = pos[0] + 8
                start_y = pos[1] - 4
                end_y = pos[1] + 4
                start_z = pos[2] - 8
                end_z = pos[2] + 8
                items = {}
                items[args['fullName']] = 1
                for block_pos in [(x, y, z) for x in range(start_x, end_x + 1)for y in range(start_y, end_y + 1)for z in range(start_z, end_z + 1)]:
                    block_id = compFactory.CreateBlockInfo(levelId).GetBlockNew(block_pos, dimension_id)['name']
                    if block_id != 'minecraft:air':
                        if block_id in items:
                            items[block_id] += 1
                        else:
                            items[block_id] = 1
                        compFactory.CreateBlockInfo(levelId).SetBlockNew(block_pos, {'name': 'minecraft:air','aux': 0}, 0, dimension_id, True)
                item_list = []
                for item_id,count in items.items():
                    item_list.append(compFactory.CreateItem(levelId).GetItemBasicInfo(item_id)['itemName'] + ' x' + str(count))
                item_dict = {'itemName': ItemType.MATTER_CLUSTER_FULL,'count': 1,'auxValue': 0,'customTips':'§c装有物品的物质团\n§o§7用于毁灭一切...§r\n'+'\n'.join(item_list),'extraId': json.dumps(items)}
                compFactory.CreateItem(levelId).SpawnItemToLevel(item_dict, dimension_id,pos)
                self.stop_coroutine(player_id)
                return
            def callback():
                pass
            for content in self.search:
                if player_id == content.get('player'):
                    coroutine = content.get('coroutine')
                    serverApi.StopCoroutine(coroutine)
            coroutine = serverApi.StartCoroutine(destory_and_get_items, callback)
            self.search.append({'player': player_id,'coroutine': coroutine})
            return
        
    def DestroyBlockEventShovel(self,args):
        pos = (args['x'],args['y'],args['z'])
        dimension_id = args['dimensionId']
        player_id = args['playerId']
        ItemCreate = compFactory.CreateItem(player_id).GetPlayerItem(minecraftEnum.ItemPosType.CARRIED, 0)
        if ItemCreate and ItemCreate['newItemName'] == ItemType.INFINITY_SHOVEL_DESTROYER:
            def destory_and_get_items():
                start_x = pos[0] - 8
                end_x = pos[0] + 8
                start_y = pos[1] - 4
                end_y = pos[1] + 4
                start_z = pos[2] - 8
                end_z = pos[2] + 8
                items = {}
                items[args['fullName']] = 1
                for block_pos in [(x, y, z) for x in range(start_x, end_x + 1)for y in range(start_y, end_y + 1)for z in range(start_z, end_z + 1)]:
                    block_id = compFactory.CreateBlockInfo(levelId).GetBlockNew(block_pos, dimension_id)['name']
                    if block_id in ('minecraft:clay','minecraft:sand','minecraft:red_sand','minecraft:farmland','minecraft:grass','minecraft:dirt'):
                        if block_id in items:
                            items[block_id] += 1
                        else:
                            items[block_id] = 1
                        compFactory.CreateBlockInfo(levelId).SetBlockNew(block_pos, {'name': 'minecraft:air','aux': 0}, 0, dimension_id, True)
                item_list = []
                for item_id,count in items.items():
                    item_list.append(compFactory.CreateItem(levelId).GetItemBasicInfo(item_id)['itemName'] + ' x' + str(count))
                item_dict = {'itemName': ItemType.MATTER_CLUSTER_FULL,'count': 1,'auxValue': 0,'customTips':'§c装有物品的物质团\n§o§7用于毁灭一切...§r\n'+'\n'.join(item_list),'extraId': json.dumps(items)}
                compFactory.CreateItem(levelId).SpawnItemToLevel(item_dict, dimension_id,pos)
                self.stop_coroutine(player_id)
                return
            def callback():
                pass
            for content in self.search:
                if player_id == content.get('player'):
                    coroutine = content.get('coroutine')
                    serverApi.StopCoroutine(coroutine)
            coroutine = serverApi.StartCoroutine(destory_and_get_items, callback)
            self.search.append({'player': player_id,'coroutine': coroutine})
            return
        
    def stop_coroutine(self, player_id):
        for content in self.search:
            if player_id == content.get('player'):self.search.remove(content)

    def ServerItemTryUseEvent(self,args):
        player_id = args['playerId']
        itemDict = args['itemDict']
        if itemDict:
            userData = itemDict.get('userData',None)
            extraId = itemDict.get('extraId',None)
            newItemName = itemDict['newItemName']
            enchantData = itemDict['enchantData']
            modEnchantData = itemDict['modEnchantData']
            if newItemName == ItemType.INFINITY_PICKAXE and compFactory.CreatePlayer(player_id).isSneaking():
                itemDict = {'itemName': ItemType.INFINITY_PICKAXE_HAMMER,'count': 1,'modEnchantData' : modEnchantData,'enchantData': enchantData,'auxValue': 0,}
                compFactory.CreateItem(player_id).SpawnItemToPlayerCarried(itemDict, player_id)
            elif newItemName == ItemType.INFINITY_PICKAXE_HAMMER and compFactory.CreatePlayer(player_id).isSneaking():
                itemDict = {'itemName': ItemType.INFINITY_PICKAXE,'count': 1,'modEnchantData' : modEnchantData,'enchantData': enchantData,'auxValue': 0,}
                compFactory.CreateItem(player_id).SpawnItemToPlayerCarried(itemDict, player_id)
            elif newItemName == ItemType.INFINITY_SHOVEL and compFactory.CreatePlayer(player_id).isSneaking():
                itemDict = {'itemName': ItemType.INFINITY_SHOVEL_DESTROYER,'count': 1,'modEnchantData' : modEnchantData,'enchantData': enchantData,'auxValue': 0,}
                compFactory.CreateItem(player_id).SpawnItemToPlayerCarried(itemDict, player_id)
            elif newItemName == ItemType.INFINITY_SHOVEL_DESTROYER and compFactory.CreatePlayer(player_id).isSneaking():
                itemDict = {'itemName': ItemType.INFINITY_SHOVEL,'count': 1,'modEnchantData' : modEnchantData,'enchantData': enchantData,'auxValue': 0,}
                compFactory.CreateItem(player_id).SpawnItemToPlayerCarried(itemDict, player_id)
            elif newItemName == ItemType.MATTER_CLUSTER_FULL:
                for item,count in json.loads(extraId).items():
                    item_dict = {'itemName': item,'count': count,}
                    compFactory.CreateItem(levelId).SpawnItemToLevel(item_dict, compFactory.CreateDimension(player_id).GetEntityDimensionId(),compFactory.CreatePos(player_id).GetPos())
                itemDict = {'itemName': 'minecraft:air','count': 1,}
                compFactory.CreateItem(player_id).SpawnItemToPlayerCarried(itemDict, player_id)

    def EntityTickServerEvent(self, args):
        entityId = args['entityId']
        engineType = args['identifier']
        if engineType != EntityType.GAPING_VOID:
            return
        attrComp = compFactory.CreateAttr(entityId)
        max_health = attrComp.GetAttrMaxValue(minecraftEnum.AttrType.HEALTH)
        attrComp.SetAttrMaxValue(minecraftEnum.AttrType.HEALTH, max_health + 2)
        age = max_health - 12.5
        pos = compFactory.CreatePos(entityId).GetPos()
        dimension_id = compFactory.CreateDimension(entityId).GetEntityDimensionId()
        radius = self.CalculateVoidScale(age) * 0.5
        hurtRange = radius * 1.1
        self.apply_drag_and_hurt(entityId, pos, radius, hurtRange)

    def CalculateVoidScale(self, age):
        life = age / 186.0
        if life < 1:
            a = 1.0 - (1.0 - life) / 1.0
            if a < 0:a = 0.0
            curve = 0.007 + self.EaseFunction(a) * 0.995
        else:
            a = 1.0 - (life - 1.0)
            if a < 0:a = 0.0
            curve = self.EaseFunction(a)
        return 10.0*curve

    def EaseFunction(self, value):
        t = value - 1
        return math.sqrt(1 - t * t)

    def apply_drag_and_hurt(self, entity_id, position, radius, hurt_range):
        entities = compFactory.CreateGame(levelId).GetEntitiesAround(
            entity_id, 20, {'test': 'is_family', 'subject': 'other', 'operator': 'not', 'value': 'void'}
        )
        for entity in entities:
            e_position = compFactory.CreatePos(entity).GetPos()
            def CalculateDistance(pos1, pos2):
                dx = pos1[0] - pos2[0]
                dy = pos1[1] - pos2[1]
                dz = pos1[2] - pos2[2]
                return math.sqrt(dx * dx + dy * dy + dz * dz)
            distance = CalculateDistance(position, e_position)
            if 0 < distance <= 20.0:
                strength = (1 - distance / 20.0) ** 2
                power = 0.075 * radius
                self.DragEntity(entity, e_position, position, distance, strength, power)
            if distance <= hurt_range:
                compFactory.CreateHurt(entity).Hurt(3, minecraftEnum.ActorDamageCause.Void, entity_id)

    def DragEntity(self, entity_id, e_position, to_position, distance, strength, power):
        motion_comp = compFactory.CreateActorMotion(entity_id)
        motion = motion_comp.GetMotion()
        new_motion = (
            motion[0] + (to_position[0] - e_position[0]) / distance * strength * power,
            motion[1] + (to_position[1] - e_position[1]) / distance * strength * power,
            motion[2] + (to_position[2] - e_position[2]) / distance * strength * power,
        )
        motion_comp.SetMotion(new_motion) if not entity_id in serverApi.GetPlayerList() else motion_comp.SetPlayerMotion(new_motion)

    def coolDownUpdate(self):
        for playerId, tick in self.cooldown.items():
            if tick <= 0:
                self.shootBow(playerId)
                self.cooldown[playerId] = 12
            else:
                self.cooldown[playerId] -= 1

    def shootBow(self, playerId):
        projectileComp = compFactory.CreateProjectile(levelId)
        itemComp = compFactory.CreateItem(playerId)
        projectileComp.CreateProjectileEntity(playerId, EntityType.HEAVEN_ARROW)
        self.CallAllclient("shootSound", {"playerId": playerId})
        itemDict = itemComp.GetEntityItem(minecraftEnum.ItemPosType.CARRIED, 0, True)
        itemStack = ItemStack(**itemDict)
        itemStack.data = 1 if itemStack.data == 0 else 0
        itemComp.SetEntityItem(minecraftEnum.ItemPosType.CARRIED, itemStack.toItemDict())

    def startUsingBow(self, args):
        playerId = args["__id__"]
        self.cooldown[playerId] = 12

    def stopUsingBow(self, args):
        playerId = args["__id__"]
        self.cooldown.pop(playerId)

    def ProjectileDoHitEffectEvent(self, args):
        projectile = args['id']
        identifier = compFactory.CreateEngineType(projectile).GetEngineTypeStr()
        if identifier == EntityType.ENDEST_PEARL:
            world = compFactory.CreateDimension(projectile).GetEntityDimensionId()
            pos = compFactory.CreatePos(projectile).GetPos()
            self.CreateEngineEntityByTypeStr(EntityType.GAPING_VOID, pos, (0, 0), world, True)
        if identifier == EntityType.HEAVEN_ARROW:
            self.spaw_barrage(args['srcId'],projectile)
            if args['hitTargetType'] == 'ENTITY':
                compFactory.CreateGame(levelId).KillEntity(args['targetId'])
    
    def spaw_barrage(self, srcId, projectileId):
        projectileComp = compFactory.CreateProjectile(levelId)
        posX, posY, posZ = compFactory.CreatePos(projectileId).GetPos()
        for i in range(12):
            angle = random.random() * 2 * math.pi
            dist = (1 - random.random()) * 0.5
            x = math.sin(angle) * dist + posX
            z = math.cos(angle) * dist + posZ
            y = posY + 25.0
            dAngle = random.random() * 2 * math.pi
            dDist = random.random() * 0.35
            dx = math.sin(dAngle) * dDist
            dz = math.cos(dAngle) * dDist
            entityId = projectileComp.CreateProjectileEntity(srcId, EntityType.SUB_HEAVEN_ARROW, {'position': (x, y, z), 'direction': (dx, -(random.random() * 1.85 + 0.15), dz)})
            compFactory.CreateActorMotion(entityId).SetMotion((dx, -(random.random() * 1.85 + 0.15), dz))

    def EntityDieLootTableServer(self, args):
        attacker = args['attacker']
        die_entity_id = args['dieEntityId']
        item_comp = compFactory.CreateItem(attacker)
        carried_item = item_comp.GetEntityItem(minecraftEnum.ItemPosType.CARRIED)
        if carried_item and carried_item["newItemName"] == ItemType.SKULLFIRE_SWORD:
            attr_comp = compFactory.CreateAttr(die_entity_id)
            if "skeleton" in attr_comp.GetTypeFamily():
                self.process_loot_list(args, ItemStack(newItemName="minecraft:skull", newAuxValue=1, count=1))

    def process_loot_list(self, args, skull_item):
        item_list = args.get('itemList', [])
        if not item_list:
            args['itemList'] = [skull_item.toItemDict()]
        else:
            new_item_list = self.update_loot_list(item_list, skull_item)
            args['itemList'] = [item.toItemDict() for item in new_item_list]
        args['dirty'] = True

    def update_loot_list(self, item_list, skull_item):
        new_item_list = [ItemStack(**item) for item in item_list]
        has_skull = False
        for item_stack in new_item_list:
            if item_stack.identifier == "minecraft:skull":
                if item_stack.data != 1:
                    item_stack.data = 1
                has_skull = True
        if not has_skull:
            new_item_list.append(skull_item)
        return new_item_list

    def playerAttackEntity(self, args):
        playerId = args["playerId"]
        victimId = args["victimId"]
        itemCarried = compFactory.CreateItem(playerId).GetEntityItem(minecraftEnum.ItemPosType.CARRIED, 0)
        if itemCarried and itemCarried["newItemName"] == ItemType.INFINITY_SWORD:
            compFactory.CreateAttr(victimId).SetAttrValue(minecraftEnum.AttrType.HEALTH, 0)
    
    def inventoryItemChangedServer(self, args):
        playerId = args['playerId']
        slotId = args['slot']
        newItemDict = args['newItemDict']
        if newItemDict and newItemDict["newItemName"] == ItemType.INFINITY_SWORD:
            itemStack = ItemStack(**newItemDict)
            itemStack.setItemCustomTips("%name%%category%%enchanting%\n\n§r§9+§cI§6n§ef§ai§bn§9i§dt§cy §r§9攻击伤害§r")
            self.gameComp.AddTimer(0.05, compFactory.CreateItem(playerId).SetPlayerAllItems, {(minecraftEnum.ItemPosType.INVENTORY, slotId): itemStack.toItemDict()})
        if newItemDict and newItemDict["newItemName"] in [ItemType.INFINITY_PICKAXE,ItemType.INFINITY_PICKAXE_HAMMER]:
            itemStack = ItemStack(**newItemDict)
            if not itemStack.hasEnchant(18):
                itemStack.addEnchant(18, 10)
                itemComp = compFactory.CreateItem(playerId)
                gameComp = compFactory.CreateGame(levelId)
                gameComp.AddTimer(0.05, itemComp.SetPlayerAllItems, {(minecraftEnum.ItemPosType.INVENTORY, slotId): itemStack.toItemDict()})

    def DamageEvent(self, args):
        entityId = args['entityId']
        cause = args['cause']
        if self.isAlArmor(entityId):
            args['knock'] = False
            args['ignite'] = False
            args['damage'] = 0
            args['damage_f'] = 0.0
    
    def HealthChangeBeforeServerEvent(self, args):
        entityId = args['entityId']
        if self.isAlArmor(entityId):
            if args['from'] - args['to'] > 0:
                args["cancel"] = True
        engine_type = compFactory.CreateEngineType(entityId).GetEngineTypeStr()
        if engine_type != EntityType.GAPING_VOID:
            return
        
    def isAlArmor(self, entityId):
        return self.armor.helmetEquipped(entityId) and self.armor.chestplateEquipped(entityId) and self.armor.leggingsEquipped(entityId) and self.armor.bootsEquipped(entityId)
    
    def OnNewArmorExchangeServerEvent(self, args):
        playerId = args["playerId"]
        slot = args["slot"]
        oldArmorDict = args["oldArmorDict"]
        newArmorDict = args["newArmorDict"]
        if slot == minecraftEnum.ArmorSlotType.HEAD:
            if oldArmorDict and oldArmorDict["newItemName"] == ItemType.INFINITY_HELMET:self.armor.setUnequipItem(playerId, ItemType.INFINITY_HELMET)
            if newArmorDict and newArmorDict["newItemName"] == ItemType.INFINITY_HELMET:self.armor.setEquipItem(playerId, ItemType.INFINITY_HELMET)
        elif slot == minecraftEnum.ArmorSlotType.BODY:
            if oldArmorDict and oldArmorDict["newItemName"] == ItemType.INFINITY_CHESTPLATE:
                self.armor.setUnequipItem(playerId, ItemType.INFINITY_CHESTPLATE)
                flyComp = compFactory.CreateFly(playerId)
                gameComp = compFactory.CreateGame(levelId)
                if flyComp.IsPlayerCanFly() and gameComp.GetPlayerGameType(playerId) != minecraftEnum.GameType.Creative:
                    flyComp.ChangePlayerFlyState(False, False)
            if newArmorDict and newArmorDict["newItemName"] == ItemType.INFINITY_CHESTPLATE:self.armor.setEquipItem(playerId, ItemType.INFINITY_CHESTPLATE)
        elif slot == minecraftEnum.ArmorSlotType.LEG:
            if oldArmorDict and oldArmorDict["newItemName"] == ItemType.INFINITY_LEGGINGS:self.armor.setUnequipItem(playerId, ItemType.INFINITY_LEGGINGS)
            if newArmorDict and newArmorDict["newItemName"] == ItemType.INFINITY_LEGGINGS:self.armor.setEquipItem(playerId, ItemType.INFINITY_LEGGINGS)
        elif slot == minecraftEnum.ArmorSlotType.FOOT:
            if oldArmorDict and oldArmorDict["newItemName"] == ItemType.INFINITY_BOOTS:
                self.armor.setUnequipItem(playerId, ItemType.INFINITY_BOOTS)
                attrComp = compFactory.CreateAttr(playerId)
                gravityComp = compFactory.CreateGravity(playerId)
                attrComp.SetStepHeight(0.5625)
                gravityComp.SetJumpPower(0.42)
                attrComp.SetAttrValue(minecraftEnum.AttrType.SPEED, 0.1)
            if newArmorDict and newArmorDict["newItemName"] == ItemType.INFINITY_BOOTS:self.armor.setEquipItem(playerId, ItemType.INFINITY_BOOTS)

    def requestFlyState(self, args):
        playerId = args["__id__"]
        self.clientCaller(playerId, "syncFlyState", {"state": self.armor.PlayerflyState})
    
    def OnScriptTickServer(self):
        for playerId in serverApi.GetPlayerList():
            flyComp = compFactory.CreateFly(playerId)
            isFlying = flyComp.IsPlayerFlying()
            self.armor.PlayerflyState[playerId] = isFlying
        self.CallAllclient("syncFlyState", {"state": self.armor.PlayerflyState})
        for entityId in self.armor.equipedArmors:
            armors = self.armor.equipedArmors[entityId]
            if ItemType.INFINITY_HELMET in armors:
                attrComp = compFactory.CreateAttr(entityId)
                compFactory.CreateBreath(entityId).SetCurrentAirSupply(300)
                attrComp.SetAttrValue(minecraftEnum.AttrType.HUNGER, 20)
                attrComp.SetAttrValue(minecraftEnum.AttrType.SATURATION, 20)
                compFactory.CreateEffect(entityId).AddEffectToEntity(minecraftEnum.EffectType.NIGHT_VISION, 15, 0, False)
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
                attrComp.SetStepHeight(1.0625)
                attrComp.SetAttrValue(minecraftEnum.AttrType.SPEED, 0.2)
                compFactory.CreateGravity(entityId).SetJumpPower(0.82)