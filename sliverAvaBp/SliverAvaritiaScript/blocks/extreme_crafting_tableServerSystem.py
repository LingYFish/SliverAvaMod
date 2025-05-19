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
        else:
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
        for i in range(81):
            key = "crafting_slot%s" % str(i + 1)
            item = self.GetContainerItem(dimensionId, pos,'container_slot', key)
            if item:
                if len([i for i in itemComp.GetPlayerAllItems(minecraftEnum.ItemPosType.INVENTORY) if i != None]) < 36:
                    itemComp.SpawnItemToPlayerInv(item, playerId)
                else:
                    self.DropItem(playerId, item)
                self.SetContainerItem(None,dimensionId, pos,'container_slot', key, {})
        recipe = extremeCraftingTable.getExtremeRecipeByName(itemName)
        if recipe:
            allItem = extremeCraftingTable.getRecipeAllItems(recipe)
            Invitem = []
            for i in range(36):
                item = itemComp.GetPlayerItem(minecraftEnum.ItemPosType.INVENTORY, i, True)
                if item:
                    Invitem.append(ItemStack(**item))
                else:
                    Invitem.append(ItemStack())
            for i in Invitem:
                for i2 in allItem:
                    if i2.isEmpty():
                        continue
                    if i == i2 and i.count >= i2.count:
                        i.count -= i2.count
                        i2.count = 0
            enough = all([i.isEmpty() for i in allItem])
            if enough:
                if recipe["type"] == "shaped":
                    shape, width, hight = extremeCraftingTable.getShaped(recipe)
                    for i in range(width):
                        for j in range(hight):
                            key = "crafting_slot%s" % str(extremeCraftingTable.posToSlot.get((i, j)) + 1)
                            self.SetContainerItem(None,dimensionId, pos,'container_slot', key, shape[j][i])
                if recipe["type"] == "shapeless":
                    ingredients = copy.deepcopy(recipe["ingredients"])
                    for i in range(len(ingredients)):
                        key = "crafting_slot%s" % str(i + 1)
                        item = ingredients[i]
                        self.SetContainerItem(None,dimensionId, pos,'container_slot', key, item)
                for i in range(36):
                    itemComp.SetPlayerAllItems({(minecraftEnum.ItemPosType.INVENTORY, i): Invitem[i].toItemDict()})
            else:
                leftItem = []
                for i in allItem:
                    if not i.isEmpty():
                        for i2 in leftItem:
                            if i2 == i:
                                i2.count += i.count
                                break
                        else:
                            leftItem.append(i)
                text = ["§c目前制作物品材料不够!\n§r§7还缺:\n"]
                for item in leftItem:
                    name = itemComp.GetItemBasicInfo(item.identifier, item.data)['itemName']
                    text.append('§r§7{} §r§7x{}§r\n'.format(name, item.count))
                self.clientCaller(playerId, "showItemText", {"text": "".join(text)})