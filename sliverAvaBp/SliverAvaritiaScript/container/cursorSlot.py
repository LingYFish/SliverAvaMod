from ..api.lib.itemStack import ItemStack
from ..api.client.BaseClientSystem import clientApi
from ..api.lib.unicodeUtils import UnicodeConvert

compFactory = clientApi.GetEngineCompFactory()
levelId = clientApi.GetLevelId()
minecraftEnum = clientApi.GetMinecraftEnum()

class cursorSlot:

    def __init__(self, screenNode, path):
        self.screenNode = screenNode
        self.path = path
        self.index = None
        self.itemRendererPath = self.screenNode.GetBaseUIControl("{}/item_renderer_panel/item_renderer".format(path))
        self.HightImage = self.screenNode.GetBaseUIControl("{}/hight_light_image".format(path))
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

    def setSlotItem(self, itemDict = None):
        if not itemDict:
            itemDict = {}
        itemDict = UnicodeConvert(itemDict)
        self.itemStack = ItemStack(**itemDict)
        itemName = self.itemStack.identifier
        count = self.itemStack.count
        auxValue = self.itemStack.data
        isEnchanted = len(self.itemStack.getEnchantData()) > 0
        userData = self.itemStack.tag
        if self.itemStack.isEmpty():
            self.setHide(True)
            self.setShowItemLock(userData)
        else:
            self.setHide(False)
            self.setShowItem(itemName, auxValue, isEnchanted, userData)
            self.setShowCount(count)
            self.setShowItemLock(userData)
        self.setProgressBar(False, 0.0)

    def setHide(self, isHide):
        self.itemRendererPath.SetVisible(not isHide, False)
        if isHide:
            self.HightImage.SetVisible(not isHide,False)
        self.itemCountLabelPath.SetVisible(not isHide, False)

    def setProgressBar(self, visible, progress):
        self.progressBar.SetVisible(visible)
        self.filledProgressBar.SetSpriteClipRatio(progress)
    
    def setShowItem(self, itemName, auxValue, isEnchanted, userData):
        self.setHide(False)
        self.itemRenderer.SetUiItem(itemName, auxValue, isEnchanted, userData)
    
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