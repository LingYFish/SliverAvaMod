from ..sliver_x_lib.client.core.api import extraClientApi as clientApi
from SliverAvaritiaScript.api.lib.color import ColorGradientText
ViewBinder = clientApi.GetViewBinderCls()
compFactory = clientApi.GetEngineCompFactory()
levelId = clientApi.GetLevelId()
minecraftEnum = clientApi.GetMinecraftEnum()

class colorUiProxy(clientApi.GetUIScreenProxyCls()):
    def __init__(self, namespace, systemname):
        super(colorUiProxy, self).__init__(namespace, systemname)
        self.screen = self.GetScreenNode()
        self.TipsPath = '/variables_button_mappings_and_controls/safezone_screen_matrix/inner_matrix/safezone_screen_panel/root_screen_panel/popup_tip_text/item_panel_image/item_text_label'
        colorTips =  {
            "Infinity":ColorGradientText("Infinity",['c', '6', 'e', 'a', 'b', '9', 'd']),
            "SANIC":ColorGradientText("SANIC",['7', '7', '7', '9', '7', 'c', '7']),
        }
        self.itemInfoTips = {
            "§c§c寰宇支配之剑§r" : {
                "customTips" : lambda: "\n§9+{} §r§9攻击伤害".format(str(colorTips["Infinity"])),
                "Cache" : ""
            },
            "§c§c无尽靴子§r" : {
                "customTips" : lambda: "\n§9+{} §r§9速度加成".format(str(colorTips["SANIC"])),
                "Cache" : ""
            }
        }
        clientApi.GetEngineCompFactory().CreateGame(levelId).AddRepeatedTimer(0.1,self.alterTips)

    def alterTips(self):
        tipsBaseUiControl = self.screen.GetBaseUIControl(self.TipsPath)
        if tipsBaseUiControl:
            tipsBaseUiControl = tipsBaseUiControl.asLabel()
        else:
            return
        tips = str(tipsBaseUiControl.GetText())
        if "§c§c寰宇支配之剑§r" in tips or self.itemInfoTips["§c§c寰宇支配之剑§r"]["Cache"]:
            text = "{}\n{}".format("§c§c寰宇支配之剑§r",self.itemInfoTips["§c§c寰宇支配之剑§r"]['customTips']())
            tipsBaseUiControl.SetText(text, False)
        elif "§c§c无尽靴子§r" in tips or self.itemInfoTips["§c§c无尽靴子§r"]["Cache"]:
            text = "{}\n{}".format("§c§c无尽靴子§r",self.itemInfoTips["§c§c无尽靴子§r"]['customTips']())
            tipsBaseUiControl.SetText(text, False)