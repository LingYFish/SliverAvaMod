from ...util.itemStack import ItemStack
from ...client.core.api import extraClientApi as clientApi
import math
import time
compFactory = clientApi.GetEngineCompFactory()
levelId = clientApi.GetLevelId()
minecraftEnum = clientApi.GetMinecraftEnum()
class FlyingItem(object):
    def __init__(self, screenNode, path, uuid, fromSlot, toSlot, offset, itemDict={}, runLater=lambda *args: None, *args):
        self.screenNode = screenNode
        self.path = path
        self.uuid = uuid
        self.runLater = runLater
        self.args = args
        self.fromSlot = fromSlot
        self.toSlot = toSlot
        self.fromDict =  self.fromSlot.itemStack.toItemDict()
        self.toDict =  self.toSlot.itemStack.toItemDict()
        self.fromPos = self.fromSlot.itemRenderer.GetGlobalPosition()
        self.toPos = self.toSlot.itemRenderer.GetGlobalPosition()
        self.moveX = self.toPos[0] - self.fromPos[0] + offset[0]
        self.moveY = self.toPos[1] - self.fromPos[1] + offset[1]
        self.time = time.time()
        self.flyTime = self.time + (min(math.ceil(math.sqrt(self.moveX ** 2 + self.moveY ** 2) / 10.0), 13.0) / 100)
        self.Finished = False
        self.itemRenderer = self.screenNode.GetBaseUIControl(path).asItemRenderer()
        self.itemRenderer.SetGlobalPosition(self.fromPos)
        self.itemStack = ItemStack(**itemDict)
        self.setFlyingItem(itemDict)

    def Finish(self):
        self.runLater(*self.args)
        remove = self.screenNode.RemoveChildControl
        self.itemRenderer.SetVisible(False)
        self.toSlot.setSlotItem2(self.fromDict)
        self.fromSlot.setSlotItem2(self.toDict)
        compFactory.CreateGame(levelId).AddTimer(0.1, remove, self.itemRenderer)
        compFactory.CreateGame(levelId).AddTimer(0.1, self.screenNode.Update)

    def setFlyingItem(self, itemDict=None):
        if not itemDict:
            itemDict = {}
        self.itemStack = ItemStack(**itemDict)
        itemName = self.itemStack.identifier
        auxValue = self.itemStack.data
        isEnchanted = len(self.itemStack.getEnchantData()) > 0
        userData = self.itemStack.tag
        self.itemRenderer.SetVisible(True)
        self.itemRenderer.SetUiItem(itemName, auxValue, isEnchanted, userData)

    def update(self):
        if time.time() > self.flyTime:
            self.Finished = True
            return
        elapsed_time = time.time() - self.time
        total_time = self.flyTime - self.time
        t = elapsed_time / total_time
        t = max(0, min(1, t))
        changePercent = self.bezier(t)
        currentX = self.fromPos[0] + self.moveX * changePercent
        currentY = self.fromPos[1] + self.moveY * changePercent
        self.itemRenderer.SetGlobalPosition((currentX, currentY))

    def bezier(self, t):
        P0 = 0
        P1 = 0.33
        P2 = 0.66
        P3 = 1
        return (1 - t) ** 3 * P0 + 3 * (1 - t) ** 2 * t * P1 + 3 * (1 - t) * t ** 2 * P2 + t ** 3 * P3