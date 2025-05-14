from SliverAvaritiaScript.api.lib.itemStack import ItemStack
from SliverAvaritiaScript.api.lib.unicodeUtils import UnicodeConvert
import math
import mod.client.extraClientApi as clientApi
levelId = clientApi.GetLevelId()
class ItemSlot(object):
    def __init__(self, screenNode, path, index = 0):
        self.screenNode = screenNode
        self.path = path
        self.index = index if isinstance(index, int) else screenNode.PATH_TO_CONTAINER.get(path)
        self.itemButton = self.screenNode.GetBaseUIControl("{}/item_button".format(path)).asButton()
        self.itemRendererPath = self.screenNode.GetBaseUIControl("{}/item_renderer_panel/item_renderer".format(path))
        self.HightImage = self.screenNode.GetBaseUIControl("{}/hight_light_image".format(path))
        self.HoverText = self.screenNode.GetBaseUIControl("{}/item_button/newHover".format(path))
        self.itemRenderer = self.screenNode.GetBaseUIControl("{}/item_renderer_panel/item_renderer".format(path)).asItemRenderer()
        self.itemCountLabel = self.screenNode.GetBaseUIControl("{}/item_renderer_panel/count_label".format(path)).asLabel()
        self.itemCountLabelPath = self.screenNode.GetBaseUIControl("{}/item_renderer_panel/count_label".format(path))
        self.selectedCellImage = self.screenNode.GetBaseUIControl("{}/selected_cell_image".format(path))
        self.selectImage = self.screenNode.GetBaseUIControl("{}/select_image".format(path) )
        self.lockCellImage = self.screenNode.GetBaseUIControl("{}/lock_cell_image".format(path))
        self.lockTypePanel = self.screenNode.GetBaseUIControl("{}/lock_type_panel".format(path))
        self.lockInInventoryImage = self.screenNode.GetBaseUIControl("{}/lock_type_panel/lock_in_inventory_image".format(path))
        self.lockInSlotImage = self.screenNode.GetBaseUIControl("{}/lock_type_panel/lock_in_slot_image".format(path))
        self.progressBar = self.screenNode.GetBaseUIControl("{}/progress_bar".format(path))
        self.filledProgressBar = self.screenNode.GetBaseUIControl("{}/progress_bar/filled_progress_bar".format(path)).asImage()
        self.durabilltyBar = self.screenNode.GetBaseUIControl("{}/item_renderer_panel/durability_bar".format(path))
        self.durabillty_progressBar = self.screenNode.GetBaseUIControl("{}/item_renderer_panel/durability_bar/progress_bar".format(path)).asProgressBar()
        self.Vaule = self.screenNode.GetBaseUIControl("{}/item_renderer_panel/durability_bar/progress_bar/filled_progress_bar".format(path)).asImage()
        self.itemStack = ItemStack()
        self.itemButton.AddHoverEventParams()
        self.itemButton.SetButtonHoverInCallback(self.onButtonHoveInCallback)
        self.itemButton.SetButtonHoverOutCallback(self.OnButtonHoverOutCallback)

    def onButtonHoveInCallback(self,args):
        self.SetItemHoverText()
        self.setHightCell(True)

    def SetItemHoverText(self):
        self.screenNode.hoverButton = self
        self.screenNode.showItemhoverText(self)
        if self.itemStack.isEmpty():
            self.screenNode.hoverText = ''

    def OnButtonHoverOutCallback(self,args):
        if self.screenNode.slotHight == self:
            self.HightImage.SetVisible(False,False)
            return
        self.setHightCell(False)

    def setHightCell(self, isHide):
        self.HoverText.SetVisible(isHide,False)
        self.HightImage.SetVisible(isHide,False)
    
    def setSlotItem(self, itemDict = None):
        if not itemDict:
            itemDict = {}
        if self.screenNode.hoverButton == self:
            self.SetItemHoverText()
        itemDict = UnicodeConvert(itemDict)
        self.itemStack = ItemStack(**itemDict)
        itemName = self.itemStack.identifier
        count = self.itemStack.count
        auxValue = self.itemStack.data
        isEnchanted = len(self.itemStack.getEnchantData()) > 0
        userData = self.itemStack.tag
        maxDurability = self.itemStack.getMaxDamage(clientApi.GetEngineCompFactory().CreateItem(levelId))
        minDurability = itemDict.get('durability',0)
        if self.itemStack.isEmpty():
            self.setHide(True)
            self.setShowItemLock(userData)
            self.durabilltyBar.SetVisible(False, False)
        else:
            self.setHide(False)
            self.setShowItem(itemName, auxValue, isEnchanted, userData)
            self.setShowCount(count)
            self.setShowItemLock(userData)
            self.setDurability(float(maxDurability),float(minDurability))
        self.setProgressBar(False, 0.0)

    def setSlotItem2(self, itemDict = None):
        if self.screenNode.hoverButton == self:
            self.SetItemHoverText()
        if not itemDict:
            itemDict = {}
        itemDict = UnicodeConvert(itemDict)
        self.itemStack = ItemStack(**itemDict)
        itemName = self.itemStack.identifier
        count = self.itemStack.count
        auxValue = self.itemStack.data
        isEnchanted = len(self.itemStack.getEnchantData()) > 0
        userData = self.itemStack.tag
        maxDurability = self.itemStack.getMaxDamage(clientApi.GetEngineCompFactory().CreateItem(levelId))
        minDurability = itemDict.get('durability',0)
        if self.itemStack.isEmpty():
            self.setHide2(True)
            self.setShowItemLock2(userData)
            self.durabilltyBar.SetVisible(False)
        else:
            self.setHide2(False)
            self.setShowItem2(itemName, auxValue, isEnchanted, userData)
            self.setShowCount2(count)
            self.setShowItemLock2(userData)
            self.setDurability2(float(maxDurability),float(minDurability))
        self.setProgressBar(False, 0.0)

    def setDurability(self,maxDurability,minDurability):
        if minDurability <= 0.0 or maxDurability <= 0.0 or maxDurability == minDurability:
            self.durabilltyBar.SetVisible(False,False)
            return
        self.durabilltyBar.SetVisible(True,False)
        durabilityRatio = minDurability/maxDurability
        self.durabillty_progressBar.SetValue(max(0,durabilityRatio-0.08))
        self.Vaule.SetSpriteColor((1 - durabilityRatio, durabilityRatio, 0))

    def setDurability2(self,maxDurability,minDurability):
        if minDurability <= 0.0 or maxDurability <= 0.0 or maxDurability == minDurability:
            self.durabilltyBar.SetVisible(False)
            return
        self.durabilltyBar.SetVisible(True)
        durabilityRatio = minDurability/maxDurability
        self.durabillty_progressBar.SetValue(max(0,durabilityRatio-0.08))
        self.Vaule.SetSpriteColor((1 - durabilityRatio, durabilityRatio, 0))
    
    def setProgressBar(self, visible, progress):
        self.progressBar.SetVisible(visible)
        self.filledProgressBar.SetSpriteClipRatio(progress)
    
    def setShowItem(self, itemName, auxValue, isEnchanted, userData):
        self.setHide(False)
        self.itemRenderer.SetUiItem(itemName, auxValue, isEnchanted, userData)

    def setShowItem2(self, itemName, auxValue, isEnchanted, userData):
        self.setHide2(False)
        self.itemRenderer.SetUiItem(itemName, auxValue, isEnchanted, userData)

    def setShowCount2(self, count):
        self.setHide2(False)
        self.itemCountLabel.SetText(str(count) if count > 1 else "")
    
    def setShowCount(self, count):
        self.setHide(False)
        self.itemCountLabel.SetText(str(count) if count > 1 else "")
    
    def setShowItemLock(self, userData):
        lockType = userData.get("minecraft:item_lock", {}).get("__value__", 0.0)
        if lockType == 1:
            self.lockTypePanel.SetVisible(True,False)
            self.lockCellImage.SetVisible(True,False)
            self.lockInInventoryImage.SetVisible(False)
            self.lockInSlotImage.SetVisible(True,False)
        elif lockType == 2:
            self.lockTypePanel.SetVisible(True,False)
            self.lockCellImage.SetVisible(True,False)
            self.lockInSlotImage.SetVisible(False,False)
            self.lockInInventoryImage.SetVisible(True,False)
        else:
            self.lockTypePanel.SetVisible(False,False)
            self.lockCellImage.SetVisible(False,False)

    def setShowItemLock2(self, userData):
        lockType = userData.get("minecraft:item_lock", {}).get("__value__", 0.0)
        if lockType == 1:
            self.lockTypePanel.SetVisible(True)
            self.lockCellImage.SetVisible(True)
            self.lockInInventoryImage.SetVisible(False)
            self.lockInSlotImage.SetVisible(True)
        elif lockType == 2:
            self.lockTypePanel.SetVisible(True)
            self.lockCellImage.SetVisible(True)
            self.lockInSlotImage.SetVisible(False)
            self.lockInInventoryImage.SetVisible(True)
        else:
            self.lockTypePanel.SetVisible(False)
            self.lockCellImage.SetVisible(False)
    
    def setHide(self, isHide):
        self.itemRendererPath.SetVisible(not isHide, False)
        if isHide:
            self.HoverText.SetVisible(not isHide,False)
            self.HightImage.SetVisible(not isHide,False)
        self.itemCountLabelPath.SetVisible(not isHide, False)

    def setHide2(self, isHide):
        self.itemRendererPath.SetVisible(not isHide)
        if isHide:
            self.HoverText.SetVisible(not isHide)
            self.HightImage.SetVisible(not isHide)
        self.itemCountLabelPath.SetVisible(not isHide)
    
    def setSelected(self, isSelected):
        self.selectImage.SetVisible(isSelected, False)
        self.selectedCellImage.SetVisible(isSelected, False)