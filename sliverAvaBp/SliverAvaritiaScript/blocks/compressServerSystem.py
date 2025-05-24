import mod.server.extraServerApi as serverApi
from SliverAvaritiaScript.container.InventoryServerSystem import InventoryBlockServerSystem
from SliverAvaritiaScript import modConfig
from SliverAvaritiaScript.api.lib.itemStack import ItemStack
import copy
import json

compFactory = serverApi.GetEngineCompFactory()
levelId = serverApi.GetLevelId()
minecraftEnum = serverApi.GetMinecraftEnum()

class compressServerSystem(InventoryBlockServerSystem):
    CLIENT_NAME = "compressClientSystem"
    OPEN_BLOCK_NAME = modConfig.BlockType.compress
    compressRepic = {
        "sliver_x:diamond_singularity" : {"items" : ["minecraft:diamond_block"],"count" : 300},
        "sliver_x:iron_singularity" : {"items" : ["minecraft:iron_block"],"count" : 400},
        "sliver_x:emerald_singularity" : {"items" : ['minecraft:emerald_block'],"count" : 200},
        "sliver_x:copper_singularity" : {"items" : ['minecraft:copper_block','minecraft:exposed_copper','minecraft:weathered_copper','minecraft:oxidized_copper','minecraft:waxed_copper','minecraft:waxed_exposed_copper','minecraft:waxed_weathered_copper','minecraft:waxed_oxidized_copper'],"count" : 400},
        "sliver_x:gold_singularity" : {"items" : ['minecraft:gold_block'],"count" : 200},
        "sliver_x:lapis_singularity" : {"items" : ['minecraft:lapis_block'],"count" : 400},
        "sliver_x:redstone_singularity" : {"items" : ['minecraft:redstone_block'],"count" : 400},
        "sliver_x:quartz_singularity" : {"items" : ['minecraft:quartz_block'],"count" : 300},
    }
    ItemToCompressRepic = {}
    for key,vaule in compressRepic.items():
        for index in vaule['items']:
            ItemToCompressRepic[index] = key

    def listenEvent(self):
        InventoryBlockServerSystem.listenEvent(self)

    def addCompressRepic(self,itemName,data):
        self.compressRepic[itemName] = data

    def _OnBlockTickServer(self,args):
        if args["blockName"] != self.OPEN_BLOCK_NAME:
            return
        dimensionId = args["dimension"]
        pos = (args["posX"], args["posY"], args["posZ"])
        blockEntityDataComp = compFactory.CreateBlockEntityData(levelId)
        blockData = blockEntityDataComp.GetBlockEntityData(dimensionId,pos)
        if not blockData['_container_']:
            blockData['_container_'] = {}
            self.SetContainerItem(None,dimensionId,pos,'__Progress__','Progress',0)
            self.SetContainerItem(None,dimensionId,pos,'__Progress__','MaxProgress',0)
            self.SetContainerItem(None,dimensionId,pos,'output','item',None)
            self.SetContainerItem(None,dimensionId,pos,'input','item',None)
        if (dimensionId, pos) not in self.BlockInfo:
            print ("初始化容器信息成功 - {}".format(blockData['_container_']))
            self.BlockInfo[(dimensionId, pos)] = blockData['_container_']
        Progress = int(self.GetContainerItem(dimensionId,pos,'__Progress__','Progress'))
        MaxProgress = int(self.GetContainerItem(dimensionId,pos,'__Progress__','MaxProgress'))
        inputD = self.GetContainerItem(dimensionId,pos,'container_slot','input')
        if Progress <= 0:
            if inputD is None or inputD == {} or ItemStack(**inputD).isEmpty():
                self.SetContainerItem(None,dimensionId,pos,'__Progress__','Progress',0)
                self.SetContainerItem(None,dimensionId,pos,'__Progress__','MaxProgress',0)
                self.SetContainerItem(None,dimensionId,pos,'output','item',None)
                self.SetContainerItem(None,dimensionId,pos,'input','item',None)
        if MaxProgress > 0:
            if Progress >= MaxProgress and MaxProgress >= 0:
                output = self.GetContainerItem(dimensionId,pos,'container_slot','output')
                if not output is None and output != {} and not ItemStack(**output).isEmpty():
                    if ItemStack(**output).count < 64:
                        self.SetContainerItem(None,dimensionId,pos,'container_slot','output',ItemStack(newItemName=self.GetContainerItem(dimensionId,pos,'output','item')['itemName'],count=ItemStack(**output).count+1).toItemDict())
                else:
                    self.SetContainerItem(None,dimensionId,pos,'container_slot','output',ItemStack(newItemName=self.GetContainerItem(dimensionId,pos,'output','item')['itemName'],count=1).toItemDict())
                self.SetContainerItem(None,dimensionId,pos,'__Progress__','Progress',0)
        if self.GetContainerItem(dimensionId,pos,'output','item') is None and not inputD is None and inputD != {} and not ItemStack(**inputD).isEmpty():
            itemStack = ItemStack(**inputD)
            if itemStack.identifier in self.ItemToCompressRepic:
                self.SetContainerItem(None,dimensionId,pos,'__Progress__','Progress',0)
                self.SetContainerItem(None,dimensionId,pos,'__Progress__','MaxProgress',self.compressRepic[self.ItemToCompressRepic[itemStack.identifier]]['count'])
                self.SetContainerItem(None,dimensionId,pos,'output','item',{'itemName':self.ItemToCompressRepic[itemStack.identifier],'auxValue':0})
        elif not inputD is None and inputD != {} and not ItemStack(**inputD).isEmpty() and not self.GetContainerItem(dimensionId,pos,'output','item') is None:
            itemStack = ItemStack(**inputD)
            add = False
            output = self.GetContainerItem(dimensionId,pos,'container_slot','output')
            if output is None or output != {} or ItemStack(**output).isEmpty() or ItemStack(**output).count < 64:
                add = True
            if itemStack.identifier in self.ItemToCompressRepic:
                if self.ItemToCompressRepic[itemStack.identifier] == self.GetContainerItem(dimensionId,pos,'output','item')['itemName'] and add:
                    self.SetContainerItem(None,dimensionId,pos,'__Progress__','Progress',int(self.GetContainerItem(dimensionId,pos,'__Progress__','Progress'))+1)
                    self.SetContainerItem(None,dimensionId,pos,'input','item',{'itemName':itemStack.identifier,'auxValue':0})
                    itemStack.count -= 1
                    self.SetContainerItem(None,dimensionId,pos,'container_slot','input',itemStack.toItemDict())

    def _OnBlockRemoveEvent(self, args):
        """删除数据"""
        pos =  (args["x"], args["y"], args["z"])
        fullName = args["fullName"]
        auxValue = args["auxValue"]
        dimensionId =  args["dimension"]
        print (fullName)
        for playerId, blockData in self.PlayerContainer.items():
            if fullName == blockData["blockName"] and pos == blockData["pos"] and auxValue == blockData["auxValue"] and dimensionId == blockData["dimensionId"]:
                self.clientCaller(playerId, "closeContainer", {})
        if fullName != self.OPEN_BLOCK_NAME:
            return
        for slot in self.BlockInfo[(dimensionId, pos)]['container_slot'].keys():
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