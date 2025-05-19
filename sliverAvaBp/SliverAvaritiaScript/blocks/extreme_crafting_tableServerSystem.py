import mod.server.extraServerApi as serverApi
from SliverAvaritiaScript.container.InventoryServerSystem import InventoryBlockServerSystem
from SliverAvaritiaScript import modConfig
from SliverAvaritiaScript.api.lib.itemStack import ItemStack
from SliverAvaritiaScript.recipe.recipeHelper import extremeCraftingTable
import copy
import json
"""工作台所有逻辑来自AlwnRrr苏奶白 特别鸣谢"""
compFactory = serverApi.GetEngineCompFactory()
levelId = serverApi.GetLevelId()
minecraftEnum = serverApi.GetMinecraftEnum()

class extreme_crafting_tableServerSystem(InventoryBlockServerSystem):
    CLIENT_NAME = "extreme_crafting_tableClientSystem"
    OPEN_BLOCK_NAME = modConfig.BlockType.extreme_crafting_table

    def listenEvent(self):
        InventoryBlockServerSystem.listenEvent(self)
        self.addListenEvent(self.requestRecipe, modConfig.modName, self.CLIENT_NAME, "requestRecipe")
        self.addListenEvent(self.requestRecipeId,  modConfig.modName, self.CLIENT_NAME, "requestRecipeId")
        self.addListenEvent(self.clearTable,  modConfig.modName, self.CLIENT_NAME, "clearTable")

    def clearTable(self,args):
        playerId = args["__id__"]
        blockInfo = self.PlayerContainer.get(playerId)
        if not blockInfo:
            return
        dimensionId = blockInfo["dimensionId"]
        pos = blockInfo["pos"]
        for i in range(81):
            key = "crafting_slot%s" % str(i + 1)
            self.SetContainerItem(None,dimensionId, pos,'container_slot', key, {})

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

    def _OnBlockRemoveEvent(self, args):
        """删除数据"""
        pos =  (args["x"], args["y"], args["z"])
        fullName = args["fullName"]
        auxValue = args["auxValue"]
        dimensionId =  args["dimension"]
        for playerId, blockData in self.PlayerContainer.items():
            if fullName == blockData["blockName"] and pos == blockData["pos"] and auxValue == blockData["auxValue"] and dimensionId == blockData["dimensionId"]:
                self.clientCaller(playerId, "closeContainer", {})
        if fullName != self.OPEN_BLOCK_NAME:
            return
        for slot in self.BlockInfo[(dimensionId, pos)]['container_slot'].keys():
            if 'slot' in slot:
                slot = self.GetContainerItem(dimensionId,pos,'container_slot',slot)
                if not slot is None and not slot == {}:
                    if ItemStack(**slot).isEmpty():
                        continue
                    self.CreateEngineItemEntity(ItemStack(**slot).toItemDict(), dimensionId, pos)
        if (dimensionId, pos) in self.BlockInfo:
            del self.BlockInfo[(dimensionId, pos)]
        blockEntityDataComp = compFactory.CreateBlockEntityData(levelId)
        blockData = blockEntityDataComp.GetBlockEntityData(dimensionId, pos)
        blockEntityDataComp.CleanExtraData(dimensionId, pos)

    def requestRecipe(self, args):
        playerId = args["__id__"]
        blockInfo = self.PlayerContainer.get(playerId)
        if not blockInfo:
            return
        dimensionId = blockInfo["dimensionId"]
        pos = blockInfo["pos"]
        container = {}
        for i in range(81):
            key = "crafting_slot%s" % str(i + 1)
            item = self.GetContainerItem(dimensionId, pos,'container_slot', key)
            container[i] = ItemStack(**item) if item else ItemStack()
        recipe = extremeCraftingTable.getExtremeRecipe(container)
        if recipe:
            outputItem = recipe["result"]
            self.SetContainerItem(None,dimensionId, pos,'container_slot', "output", outputItem)
            return
        self.SetContainerItem(None,dimensionId, pos,'container_slot', "output", {})

    def DropItem(self, playerId, itemDict):
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
    
    def requestRecipeId(self, args):
        playerId = args["__id__"]
        itemName = args["itemName"]
        itemComp = compFactory.CreateItem(playerId)
        blockInfo = self.PlayerContainer.get(playerId)
        if not blockInfo:
            return
        dimensionId = blockInfo["dimensionId"]
        pos = blockInfo["pos"]
        self.ClearCraftingGrid(dimensionId, pos, playerId, itemComp)
        recipe = extremeCraftingTable.getExtremeRecipeByName(itemName)
        if not recipe:
            return
        inventoryItems = self.GetInventoryItems(itemComp)
        requiredItems = extremeCraftingTable.getRecipeAllItems(recipe)
        checkSuccess, materialSnapshot = self.CheckMaterials(inventoryItems, requiredItems)
        
        if checkSuccess:
            try:
                self.SetupRecipeGrid(recipe, dimensionId, pos)
                self.UpdateInventory(itemComp, inventoryItems)
            except Exception as e:
                self.RecoverMaterials(inventoryItems, materialSnapshot)
                self.UpdateInventory(itemComp, inventoryItems)
                self.ShowSystemError(playerId, str(e))
        else:
            missingItems = self.CalculateMissingItems(requiredItems)
            self.ShowWarning(playerId, missingItems, itemComp)

    def ClearCraftingGrid(self, dimensionId, pos, playerId, itemComp):
        for i in range(81):
            slotKey = "crafting_slot%s" % (i + 1)
            item = self.GetContainerItem(dimensionId, pos, 'container_slot', slotKey)
            if not item:
                continue
            if len([i for i in itemComp.GetPlayerAllItems(minecraftEnum.ItemPosType.INVENTORY) if i]) < 36:
                itemComp.SpawnItemToPlayerInv(item, playerId)
            else:
                self.DropItem(playerId, item)
            self.SetContainerItem(None, dimensionId, pos, 'container_slot', slotKey, {})

    def GetInventoryItems(self, itemComp):
        return [
            ItemStack(**item).clone() if item else ItemStack()
            for item in itemComp.GetPlayerAllItems(minecraftEnum.ItemPosType.INVENTORY)
        ]

    def CheckMaterials(self, inventoryItems, requiredItems):
        materialSnapshot = [item.clone() for item in inventoryItems]
        tempInventory = [item.clone() for item in inventoryItems]
        try:
            for required in requiredItems:
                if required.isEmpty():
                    continue
                remaining = required.count
                for invItem in tempInventory:
                    if invItem == required and invItem.count > 0:
                        deduct = min(invItem.count, remaining)
                        invItem.count -= deduct
                        remaining -= deduct
                        if remaining <= 0:
                            break
                if remaining > 0:
                    return False, materialSnapshot
            for i in range(len(inventoryItems)):
                inventoryItems[i].count = tempInventory[i].count
            return True, None
        except:
            return False, materialSnapshot

    def RecoverMaterials(self, inventoryItems, snapshot):
        for i in range(len(inventoryItems)):
            inventoryItems[i].count = snapshot[i].count

    def SetupRecipeGrid(self, recipe, dimensionId, pos):
        if recipe["type"] == "shaped":
            shape, width, height = extremeCraftingTable.getShaped(recipe)
            for x in range(width):
                for y in range(height):
                    slotNum = extremeCraftingTable.posToSlot.get((x, y)) + 1
                    slotKey = "crafting_slot%s" % slotNum
                    self.SetContainerItem(None, dimensionId, pos, 'container_slot', slotKey, shape[y][x])
        else:
            ingredients = copy.deepcopy(recipe["ingredients"])
            for idx in range(len(ingredients)):
                slotKey = "crafting_slot%s" % (idx + 1)
                self.SetContainerItem(None, dimensionId, pos, 'container_slot', slotKey, ingredients[idx])

    def CalculateMissingItems(self, requiredItems):
        missing = []
        for item in requiredItems:
            if item.isEmpty():
                continue
            found = False
            for m in missing:
                if m == item:
                    m.count += item.count
                    found = True
                    break
            if not found:
                missing.append(item.clone())
        return missing

    def ShowWarning(self, playerId, missingItems, itemComp):
        msg = ["§c材料不足！\n§r§7缺少以下物品：\n"]
        for item in missingItems:
            info = itemComp.GetItemBasicInfo(item.identifier, item.data)
            msg.append("§r§7%s §r§7x%d§r\n" % (info['itemName'], item.count))
        self.clientCaller(playerId, "showItemText", {"text": "".join(msg)})

    def UpdateInventory(self, itemComp, inventoryItems):
        updateDict = {
            (minecraftEnum.ItemPosType.INVENTORY, i): item.toItemDict()
            for i, item in enumerate(inventoryItems)
        }
        itemComp.SetPlayerAllItems(updateDict)

    def ShowSystemError(self, playerId, errorMsg):
        self.clientCaller(playerId, "showItemText", {
            "text": "§c合成过程发生错误！\n§r§7错误信息：%s\n§r§e材料已自动恢复" % errorMsg
        })