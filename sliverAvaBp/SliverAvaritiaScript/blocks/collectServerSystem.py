import mod.server.extraServerApi as serverApi
from SliverAvaritiaScript.container.InventoryServerSystem import InventoryBlockServerSystem
from SliverAvaritiaScript import modConfig
from SliverAvaritiaScript.api.lib.itemStack import ItemStack
import copy
import json

compFactory = serverApi.GetEngineCompFactory()
levelId = serverApi.GetLevelId()
minecraftEnum = serverApi.GetMinecraftEnum()

class collectServerSystem(InventoryBlockServerSystem):
    CLIENT_NAME = "collectClientSystem"
    OPEN_BLOCK_NAME = modConfig.BlockType.collect

    def listenEvent(self):
        InventoryBlockServerSystem.listenEvent(self)

    def _OnBlockTickServer(self,args):
        if args["blockName"] != self.OPEN_BLOCK_NAME:
            return
        dimensionId = args["dimension"]
        pos = (args["posX"], args["posY"], args["posZ"])
        blockEntityDataComp = compFactory.CreateBlockEntityData(levelId)
        blockData = blockEntityDataComp.GetBlockEntityData(dimensionId,pos)
        if not blockData['_container_']:
            blockData['_container_'] = {}
            self.SetContainerItem(None,dimensionId,pos,'__Progress__','Progress',0.00)
        if (dimensionId, pos) not in self.BlockInfo:
            print ("初始化容器信息成功 - {}".format(blockData['_container_']))
            self.BlockInfo[(dimensionId, pos)] = blockData['_container_']
        Progress = self.GetContainerItem(dimensionId,pos,'__Progress__','Progress')
        if Progress is None:
            Progress = 0.00
        self.SetContainerItem(None,dimensionId,pos,'__Progress__','Progress',Progress+0.01)
        Progress = self.GetContainerItem(dimensionId,pos,'__Progress__','Progress')
        if Progress > 100.0:
            output = self.GetContainerItem(dimensionId,pos,'container_slot','output')
            if not output is None and output != {} and not ItemStack(**output).isEmpty():
                if ItemStack(**output).count < 64:
                    self.SetContainerItem(None,dimensionId,pos,'container_slot','output',ItemStack(newItemName='sliver_x:neutron_pile',count=ItemStack(**output).count+1).toItemDict())
            else:
                self.SetContainerItem(None,dimensionId,pos,'container_slot','output',ItemStack(newItemName='sliver_x:neutron_pile',count=1,newAuxValue=0).toItemDict())
            self.SetContainerItem(None,dimensionId,pos,'__Progress__','Progress',0.00)

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