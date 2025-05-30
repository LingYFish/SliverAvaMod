from ...util.itemStack import ItemStack
from ...client.core.api import extraClientApi as clientApi
from ...util.unicodeUtils import UnicodeConvert
compFactory = clientApi.GetEngineCompFactory()
levelId = clientApi.GetLevelId()
minecraftEnum = clientApi.GetMinecraftEnum()
class hoverButton(object):
    def __init__(self, screenNode, path,setFunc=lambda a,b,c:a,Callck=None):
        self.screenNode = screenNode
        self.path = path
        self.playerId = clientApi.GetLocalPlayerId()
        self.itemRenderer = self.screenNode.GetBaseUIControl("{}/item_renderer".format(path)).asItemRenderer()
        self.HoverText = self.screenNode.GetBaseUIControl("{}/newHover".format(path))
        self.itemButton = self.screenNode.GetBaseUIControl(path).asButton()
        self.itemStack = ItemStack()
        self.itemButton.AddHoverEventParams()
        self.text = ""
        self.itemDict = {}
        self.setFunc = setFunc
        if Callck:
            self.itemButton.GetBaseUIControl("/panel/test_btn").asButton()
            self.itemButton.AddTouchEventParams({"isSwallow":True})
            self.itemButton.SetButtonTouchUpCallback(lambda button: Callck(self,button))
        self.itemButton.SetButtonHoverInCallback(self.onButtonHoveInCallback)
        self.itemButton.SetButtonHoverOutCallback(self.OnButtonHoverOutCallback)

    def replaceSpecialCharacters(self, text):
        """
        替换特殊字符。
        :param text: 文本
        :return: 替换后的文本
        """
        text = text.replace(':hollow_star:', '')
        text = text.replace(':solid_star:', '')
        return text
    
    def showText(self):
        text = ''
        if self.text != "":
            text = self.setFunc(self.replaceSpecialCharacters(text),None,None)
        if self.itemDict:
            text = compFactory.CreateItem(levelId).GetItemFormattedHoverText(str(self.itemDict['itemName']), 15, False)
            text = self.setFunc(self.replaceSpecialCharacters(text),self.itemDict['itemName'],self.itemDict['auxValue'])
        self.screenNode.hoverText = text

    def setUiItem(self):
        if self.itemDict:
            self.screenNode.GetBaseUIControl("{}/item_renderer".format(self.path)).SetVisible(True)
            self.itemRenderer.SetUiItem(self.itemDict['itemName'], int(self.itemDict['auxValue']))
        else:
            self.screenNode.GetBaseUIControl("{}/item_renderer".format(self.path)).SetVisible(False)

    def onButtonHoveInCallback(self,args):
        self.showText()
        self.setHightCell(True)

    def OnButtonHoverOutCallback(self,args):
        self.setHightCell(False)

    def setHightCell(self, isHide):
        self.HoverText.SetVisible(isHide,False)