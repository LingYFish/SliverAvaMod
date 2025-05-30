from ..sliver_x_lib.server.core import api as sApi
from ..sliver_x_lib.client.core import api as cApi
from ..sliver_x_lib.server.level import level
from ..sliver_x_lib.util import minecraftEnum
from ..sliver_x_lib.util.itemStack import ItemStack
from ..sliver_x_lib.ui.backpack.InventoryServerSystem import InventoryBlockServerSystem
from SliverAvaritiaScript import modConfig
import copy
import json

class extremeCraftingTable(object):
    index = 0
    posToSlot = {(x, y): index for y in range(9) for x in range(9) for index in [y * 9 + x]}

    recipeItems = [
        {"newItemName": modConfig.ItemType.INFINITY_CATALYST,"newAuxValue": 0,"count": 1},
        {"newItemName": modConfig.ItemType.INFINITY_INGOT,"newAuxValue": 0,"count": 1},
        {"newItemName": modConfig.ItemType.INFINITY_SWORD,"newAuxValue": 0,"count": 1,'userData': {'ItemCustomTips': {'__type__': 8, '__value__': '%name%%category%%enchanting%%\n\n§r§9+§cI§6n§ef§ai§bn§9i§dt§cy §r§9攻击伤害§r'}}},
        {"newItemName": modConfig.ItemType.INFINITY_BOW,"newAuxValue": 0,"count": 1},
        {"newItemName": modConfig.ItemType.INFINITY_PICKAXE,"newAuxValue": 0,"count": 1,'userData': {'ench': [{'lvl': {'__type__': 2, '__value__': 10}, 'id': {'__type__': 2, '__value__': 18}}]}},
        {"newItemName": modConfig.ItemType.INFINITY_SHOVEL,"newAuxValue": 0,"count": 1},
        {"newItemName": modConfig.ItemType.INFINITY_HOE,"newAuxValue": 0,"count": 1},
        {"newItemName": modConfig.ItemType.INFINITY_AXE,"newAuxValue": 0,"count": 1},
        {"newItemName": modConfig.ItemType.INFINITY_HELMET,"newAuxValue": 0,"count": 1},
        {"newItemName": modConfig.ItemType.INFINITY_CHESTPLATE,"newAuxValue": 0,"count": 1},
        {"newItemName": modConfig.ItemType.INFINITY_LEGGINGS,"newAuxValue": 0,"count": 1},
        {"newItemName": modConfig.ItemType.INFINITY_BOOTS,"newAuxValue": 0,"count": 1},
        {"newItemName": modConfig.ItemType.SKULLFIRE_SWORD,"newAuxValue": 0,"count": 1},
        {"newItemName": modConfig.ItemType.ENDEST_PEARL,"newAuxValue": 0,"count": 1},
        {"newItemName": modConfig.ItemType.ULTIMATE_STEW,"newAuxValue": 0,"count": 1},
        {"newItemName": modConfig.ItemType.COSMIC_MEATBALLS,"newAuxValue": 0,"count": 1},
        {"newItemName": modConfig.BlockType.collect,"newAuxValue": 0,"count": 1},
        {"newItemName": modConfig.BlockType.compress,"newAuxValue": 0,"count": 1}]
    extremeRecipe = [
        {"identifier": "sliver_x:infinity_catalyst", "type": "shapeless", "ingredients": [{"newItemName": "sliver_x:diamond_lattice", "newAuxValue": 0, "count": 1}, {"newItemName": "sliver_x:crystal_matrix_ingot", "newAuxValue": 0, "count": 1}, {"newItemName": "sliver_x:neutron_pile", "newAuxValue": 0, "count": 1}, {"newItemName": "sliver_x:neutron_nugget", "newAuxValue": 0, "count": 1}, {"newItemName": "sliver_x:neutronium_ingot", "newAuxValue": 0, "count": 1}, {"newItemName": "sliver_x:ultimate_stew", "newAuxValue": 0, "count": 1}, {"newItemName": "sliver_x:cosmic_meatballs", "newAuxValue": 0, "count": 1}, {"newItemName": "sliver_x:endest_pearl", "newAuxValue": 0, "count": 1}, {"newItemName": "sliver_x:record_fragment", "newAuxValue": 0, "count": 1}, {"newItemName": "sliver_x:iron_singularity", "newAuxValue": 0, "count": 1}, {"newItemName": "sliver_x:gold_singularity", "newAuxValue": 0, "count": 1}, {"newItemName": "sliver_x:lapis_singularity", "newAuxValue": 0, "count": 1}, {"newItemName": "sliver_x:redstone_singularity", "newAuxValue": 0, "count": 1}, {"newItemName": "sliver_x:quartz_singularity", "newAuxValue": 0, "count": 1}, {"newItemName": "sliver_x:diamond_singularity", "newAuxValue": 0, "count": 1}, {"newItemName": "sliver_x:emerald_singularity", "newAuxValue": 0, "count": 1}], "result": {"newItemName": "sliver_x:infinity_catalyst", "newAuxValue": 0, "count": 1}},
        {"identifier": "sliver_x:cosmic_meatballs", "type": "shapeless", "ingredients": [{"newItemName": "sliver_x:neutron_pile", "newAuxValue": 0, "count": 1}, {"newItemName": "minecraft:beef", "newAuxValue": 0, "count": 1}, {"newItemName": "minecraft:beef", "newAuxValue": 0, "count": 1}, {"newItemName": "minecraft:chicken", "newAuxValue": 0, "count": 1}, {"newItemName": "minecraft:chicken", "newAuxValue": 0, "count": 1}, {"newItemName": "minecraft:porkchop", "newAuxValue": 0, "count": 1}, {"newItemName": "minecraft:porkchop", "newAuxValue": 0, "count": 1}, {"newItemName": "minecraft:rabbit", "newAuxValue": 0, "count": 1}, {"newItemName": "minecraft:rabbit", "newAuxValue": 0, "count": 1}, {"newItemName": "minecraft:cod", "newAuxValue": 0, "count": 1}, {"newItemName": "minecraft:cod", "newAuxValue": 0, "count": 1}], "result": {"newItemName": "sliver_x:cosmic_meatballs", "newAuxValue": 0, "count": 1}},
        {"identifier": "sliver_x:ultimate_stew", "type": "shapeless", "ingredients": [{"newItemName": "sliver_x:neutron_pile", "newAuxValue": 0, "count": 1}, {"newItemName": "minecraft:wheat", "newAuxValue": 0, "count": 1}, {"newItemName": "minecraft:wheat", "newAuxValue": 0, "count": 1}, {"newItemName": "minecraft:carrot", "newAuxValue": 0, "count": 1}, {"newItemName": "minecraft:carrot", "newAuxValue": 0, "count": 1}, {"newItemName": "minecraft:potato", "newAuxValue": 0, "count": 1}, {"newItemName": "minecraft:potato", "newAuxValue": 0, "count": 1}, {"newItemName": "minecraft:cactus", "newAuxValue": 0, "count": 1}, {"newItemName": "minecraft:cactus", "newAuxValue": 0, "count": 1}, {"newItemName": "minecraft:red_mushroom", "newAuxValue": 0, "count": 1}, {"newItemName": "minecraft:red_mushroom", "newAuxValue": 0, "count": 1}, {"newItemName": "minecraft:brown_mushroom", "newAuxValue": 0, "count": 1}, {"newItemName": "minecraft:brown_mushroom", "newAuxValue": 0, "count": 1}], "result": {"newItemName": "sliver_x:ultimate_stew", "newAuxValue": 0, "count": 1}},
        {"identifier": "sliver_x:endest_pearl", "type": "shaped", "pattern": ["   EEE   ", " EEPPPEE ", " EPPPPPE ", "EPPPNPPPE", "EPPNSNPPE", "EPPPNPPPE", " EPPPPPE ", " EEPPPEE ", "   EEE   "], "key": {"E": {"newItemName": "minecraft:end_stone", "newAuxValue": 0, "count": 1}, "P": {"newItemName": "minecraft:ender_pearl", "newAuxValue": 0, "count": 1}, "S": {"newItemName": "minecraft:nether_star", "newAuxValue": 0, "count": 1}, "N": {"newItemName": "sliver_x:neutronium_ingot", "newAuxValue": 0, "count": 1}}, "result": {"newItemName": "sliver_x:endest_pearl", "newAuxValue": 0, "count": 1}},
        {"identifier": "sliver_x:infinity_ingot", "type": "shaped", "pattern": ["NNNNNNNNN", "NCXXCXXCN", "NXCCXCCXN", "NCXXCXXCN", "NNNNNNNNN"], "key": {"C": {"newItemName": "sliver_x:crystal_matrix_ingot", "newAuxValue": 0, "count": 1}, "N": {"newItemName": "sliver_x:neutronium_ingot", "newAuxValue": 0, "count": 1}, "X": {"newItemName": "sliver_x:infinity_catalyst", "newAuxValue": 0, "count": 1}}, "result": {"newItemName": "sliver_x:infinity_ingot", "newAuxValue": 0, "count": 1}},
        {"identifier": "sliver_x:compress", "type": "shaped", "pattern": ["IIIHHHIII", "X N   N X", "I N   N I", "X N   N X", "RNN O NNR", "X N   N X", "I N   N I", "X N   N X", "IIIXIXIII"], "key": {"X": {"newItemName": "sliver_x:crystal_matrix_ingot", "newAuxValue": 0, "count": 1}, "N": {"newItemName": "sliver_x:neutronium_ingot", "newAuxValue": 0, "count": 1}, "I": {"newItemName": "minecraft:iron_block", "newAuxValue": 0, "count": 1}, "H": {"newItemName": "minecraft:hopper", "newAuxValue": 0, "count": 1}, "R": {"newItemName": "minecraft:redstone_block", "newAuxValue": 0, "count": 1}, "O": {"newItemName": "sliver_x:neutronium_block", "newAuxValue": 0, "count": 1}}, "result": {"newItemName": "sliver_x:compress", "newAuxValue": 0, "count": 1}},
        {"identifier": "sliver_x:collect", "type": "shaped", "pattern": ["IIQQQQQII", "I QQQQQ I", "I  RRR  I", "X RRRRR X", "I RRXRR I", "X RRRRR X", "I  RRR  I", "I       I", "IIIXIXIII"], "key": {"X": {"newItemName": "sliver_x:crystal_matrix_ingot", "newAuxValue": 0, "count": 1}, "I": {"newItemName": "minecraft:iron_block", "newAuxValue": 0, "count": 1}, "Q": {"newItemName": "minecraft:quartz_block", "newAuxValue": 0, "count": 1}, "R": {"newItemName": "minecraft:redstone_block", "newAuxValue": 0, "count": 1}}, "result": {"newItemName": "sliver_x:collect", "newAuxValue": 0, "count": 1}},
        {"identifier": "sliver_x:skullfire_sword", "type": "shaped", "pattern": ["       IX", "      IXI", "     IXI ", "    IXI  ", " B IXI   ", "  BXI    ", "  WB     ", " W  B    ", "D        "], "key": {"I": {"newItemName": "sliver_x:crystal_matrix_ingot", "newAuxValue": 0, "count": 1}, "X": {"newItemName": "minecraft:blaze_powder", "newAuxValue": 0, "count": 1}, "B": {"newItemName": "minecraft:bone", "newAuxValue": 0, "count": 1}, "D": {"newItemName": "minecraft:nether_star", "newAuxValue": 0, "count": 1}, "W": {"newItemName": "minecraft:log", "newAuxValue": 0, "count": 1}}, "result": {"newItemName": "sliver_x:skullfire_sword", "newAuxValue": 0, "count": 1}},
        {"identifier": "sliver_x:infinity_sword", "type": "shaped", "pattern": ["       II", "      III", "     III ", "    III  ", " C III   ", "  CII    ", "  NC     ", " N  C    ", "X        "], "key": {"I": {"newItemName": "sliver_x:infinity_ingot", "newAuxValue": 0, "count": 1}, "X": {"newItemName": "sliver_x:infinity_catalyst", "newAuxValue": 0, "count": 1}, "C": {"newItemName": "sliver_x:crystal_matrix_ingot", "newAuxValue": 0, "count": 1}, "N": {"newItemName": "sliver_x:neutronium_ingot", "newAuxValue": 0, "count": 1}}, "result": {"newItemName": "sliver_x:infinity_sword", "newAuxValue": 0, "count": 1, "userData": {"ItemCustomTips": {"__type__": 8, "__value__": "%name%%category%%enchanting%%\n§r§9+§cI§6n§ef§ai§bn§9i§dt§cy §r§9攻击伤害§r"}}}},
        {"identifier": "sliver_x:infinity_pickaxe", "type": "shaped", "pattern": [" IIIIIII ", "IIIICIIII", "II  N  II", "    N    ", "    N    ", "    N    ", "    N    ", "    N    ", "    N    "], "key": {"I": {"newItemName": "sliver_x:infinity_ingot", "newAuxValue": 0, "count": 1}, "C": {"newItemName": "sliver_x:crystal_matrix", "newAuxValue": 0, "count": 1}, "N": {"newItemName": "sliver_x:neutronium_ingot", "newAuxValue": 0, "count": 1}}, "result": {"newItemName": "sliver_x:infinity_pickaxe", "newAuxValue": 0, "count": 1, "userData": {"ench": [{"lvl": {"__type__": 2, "__value__": 10}, "id": {"__type__": 2, "__value__": 18}}]}}},
        {"identifier": "sliver_x:infinity_shovel", "type": "shaped", "pattern": ["      III", "     IIXI", "      III", "     N I ", "    N    ", "   N     ", "  N      ", " N       ", "N        "], "key": {"I": {"newItemName": "sliver_x:infinity_ingot", "newAuxValue": 0, "count": 1}, "X": {"newItemName": "sliver_x:infinity_block", "newAuxValue": 0, "count": 1}, "N": {"newItemName": "sliver_x:neutronium_ingot", "newAuxValue": 0, "count": 1}}, "result": {"newItemName": "sliver_x:infinity_shovel", "newAuxValue": 0, "count": 1}},
        {"identifier": "sliver_x:infinity_axe", "type": "shaped", "pattern": [" I   ", "IIIII", " IIII", "   IN", "    N", "    N", "    N", "    N", "    N"], "key": {"I": {"newItemName": "sliver_x:infinity_ingot", "newAuxValue": 0, "count": 1}, "N": {"newItemName": "sliver_x:neutronium_ingot", "newAuxValue": 0, "count": 1}}, "result": {"newItemName": "sliver_x:infinity_axe", "newAuxValue": 0, "count": 1}},
        {"identifier": "sliver_x:infinity_hoe", "type": "shaped", "pattern": ["     N ", " IIIIII", "IIIIIII", "I    II", "     N ", "     N ", "     N ", "     N ", "     N "], "key": {"I": {"newItemName": "sliver_x:infinity_ingot", "newAuxValue": 0, "count": 1}, "N": {"newItemName": "sliver_x:neutronium_ingot", "newAuxValue": 0, "count": 1}}, "result": {"newItemName": "sliver_x:infinity_hoe", "newAuxValue": 0, "count": 1}},
        {"identifier": "sliver_x:infinity_bow", "type": "shaped", "pattern": ["   II", "  I W", " I  W", "I   W", "X   W", "I   W", " I  W", "  I W", "   II"], "key": {"I": {"newItemName": "sliver_x:infinity_ingot", "newAuxValue": 0, "count": 1}, "X": {"newItemName": "sliver_x:crystal_matrix_ingot", "newAuxValue": 0, "count": 1}, "W": {"newItemName": "minecraft:wool", "newAuxValue": 0, "count": 1}}, "result": {"newItemName": "sliver_x:infinity_bow", "newAuxValue": 0, "count": 1}},
        {"identifier": "sliver_x:infinity_helmet", "type": "shaped", "pattern": [" NNNNN ", "NIIIIIN", "N XIX N", "NIIIIIN", "NIIIIIN", "NI I IN"], "key": {"N": {"newItemName": "sliver_x:neutronium_ingot", "newAuxValue": 0, "count": 1}, "X": {"newItemName": "sliver_x:infinity_catalyst", "newAuxValue": 0, "count": 1}, "I": {"newItemName": "sliver_x:infinity_ingot", "newAuxValue": 0, "count": 1}}, "result": {"newItemName": "sliver_x:infinity_helmet", "newAuxValue": 0, "count": 1}},
        {"identifier": "sliver_x:infinity_chestplate", "type": "shaped", "pattern": [" NN   NN ", "NNN   NNN", "NNN   NNN", " NIIIIIN ", " NIIXIIN ", " NIIIIIN ", " NIIIIIN ", " NIIIIIN ", "  NNNNN  "], "key": {"N": {"newItemName": "sliver_x:neutronium_ingot", "newAuxValue": 0, "count": 1}, "X": {"newItemName": "sliver_x:crystal_matrix", "newAuxValue": 0, "count": 1}, "I": {"newItemName": "sliver_x:infinity_ingot", "newAuxValue": 0, "count": 1}}, "result": {"newItemName": "sliver_x:infinity_chestplate", "newAuxValue": 0, "count": 1}},
        {"identifier": "sliver_x:infinity_leggings", "type": "shaped", "pattern": ["NNNNNNNNN", "NIIIXIIIN", "NINNXNNIN", "NIN   NIN", "NCN   NCN", "NIN   NIN", "NIN   NIN", "NIN   NIN", "NNN   NNN"], "key": {"N": {"newItemName": "sliver_x:neutronium_ingot", "newAuxValue": 0, "count": 1}, "X": {"newItemName": "sliver_x:infinity_catalyst", "newAuxValue": 0, "count": 1}, "I": {"newItemName": "sliver_x:infinity_ingot", "newAuxValue": 0, "count": 1}, "C": {"newItemName": "sliver_x:crystal_matrix", "newAuxValue": 0, "count": 1}}, "result": {"newItemName": "sliver_x:infinity_leggings", "newAuxValue": 0, "count": 1}},        
        {"identifier": "sliver_x:infinity_boots", "type": "shaped", "pattern": [" NNN NNN ", " NIN NIN ", " NIN NIN ", "NNIN NINN", "NIIN NIIN", "NNNN NNNN"], "key": {"N": {"newItemName": "sliver_x:neutronium_ingot", "newAuxValue": 0, "count": 1}, "I": {"newItemName": "sliver_x:infinity_ingot", "newAuxValue": 0, "count": 1}}, "result": {"newItemName": "sliver_x:infinity_boots", "newAuxValue": 0, "count": 1}},
    ]

    @staticmethod
    def getRecipeAllItems(recipe):
        if recipe["type"] == "shapeless":
            return [ItemStack(**i) for i in recipe["ingredients"]]
        if recipe["type"] == "shaped":
            all_items = []
            shape = extremeCraftingTable.getShaped(recipe)[0]
            for line in shape:
                for item in line:
                    if item:
                        all_items.append(ItemStack(**item))
            return all_items

    @staticmethod
    def getExtremeRecipe(container):
        for recipe in extremeCraftingTable.extremeRecipe:
            if extremeCraftingTable.handleRecipe(recipe, container):
                return recipe
        return None

    @staticmethod
    def getExtremeRecipeByName(name):
        for recipe in extremeCraftingTable.extremeRecipe:
            if recipe["identifier"] == name:
                return recipe
        return None

    @staticmethod
    def handleRecipe(recipe, container):
        if recipe["type"] == "shapeless":
            return extremeCraftingTable.canShapelessRecipe(recipe, container)
        if recipe["type"] == "shaped":
            return extremeCraftingTable.canShapedRecipe(recipe, container)
        return False

    @staticmethod
    def getShaped(recipe):
        pattern = recipe["pattern"]
        key = recipe["key"]
        shape = []
        width = 0
        for i in pattern:
            line = [key.get(s) for s in i]
            width = max(len(line), width)
            shape.append(line)
        height = len(shape)
        return shape, width, height

    @staticmethod
    def canShapedRecipe(recipe, container):
        shape, width, height = extremeCraftingTable.getShaped(recipe)
        for x in range(9 - (width - 1)):
            for y in range(9 - (height - 1)):
                can_recipe = True
                pos = (x, y)
                all_pos = set()
                for i in range(width):
                    for j in range(height):
                        posX, posY = pos[0] + i, pos[1] + j
                        all_pos.add((posX, posY))
                        item = container[extremeCraftingTable.posToSlot[(posX, posY)]]
                        item2 = shape[j][i]
                        item2 = ItemStack(**item2) if item2 else ItemStack()
                        if not (item == item2 and item.count >= item2.count) and not (item.isEmpty() and item2.isEmpty()):
                            can_recipe = False
                left_pos = set(extremeCraftingTable.posToSlot.keys()) - all_pos
                if all(container[extremeCraftingTable.posToSlot[i]].isEmpty() for i in left_pos) and can_recipe:
                    return True
        return False

    @staticmethod
    def canShapelessRecipe(recipe, container):
        all_items = list(container.values())
        ingredients = [ItemStack(**i) for i in recipe["ingredients"]]
        ingredients_count = len(ingredients)
        for item in ingredients:
            for item2 in all_items:
                if item == item2 and item2.count >= item.count:
                    ingredients_count -= 1
                    break
        return ingredients_count == 0 and len([i for i in all_items if not i.isEmpty()]) == len(recipe["ingredients"])
    
"""工作台所有逻辑来自AlwnRrr苏奶白 特别鸣谢"""
compFactory = sApi.serverApi.GetEngineCompFactory()
levelId = sApi.serverApi.GetLevelId()

class extreme_crafting_tableServerSystem(InventoryBlockServerSystem):
    CLIENT_NAME = "extreme_crafting_tableClientSystem"
    OPEN_BLOCK_NAME = modConfig.BlockType.extreme_crafting_table

    def addRecipe(self,data,recipe):
        extremeCraftingTable.recipeItems.append(data)
        extremeCraftingTable.extremeRecipe.append(recipe)

    def _OpenContainer(self,args):
        """打开容器"""
        blockName = args["blockName"] #type: str
        aux = args["aux"] #type: int
        dimensionId = args["dimensionId"] #type: int
        pos = (args["x"], args["y"], args["z"]) #type: tuple
        playerId = args["playerId"] #type: str
        blockEntityDataComp = compFactory.CreateBlockEntityData(levelId)
        if blockName == self.OPEN_BLOCK_NAME and playerId not in self.CoolDown:
            args["cancel"] = True
            self.clientCaller(playerId, "openContainer", {"pos": pos,"recipeItems": extremeCraftingTable.recipeItems})#发送事件给客户端，在客户端打开ui界面
            self.PlayerContainer[playerId] = {"pos": pos, "dimensionId": dimensionId, "blockName": self.OPEN_BLOCK_NAME, "auxValue": aux,"recipeItems": extremeCraftingTable.recipeItems}
            self.CoolDown[playerId] = 10

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
        dir = sApi.serverApi.GetDirFromRot(rotComp.GetRot())
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