import mod.client.extraClientApi as clientApi
from SliverAvaritiaScript.api.lib.color import ColorGradientText
ViewBinder = clientApi.GetViewBinderCls()
compFactory = clientApi.GetEngineCompFactory()
levelId = clientApi.GetLevelId()
minecraftEnum = clientApi.GetMinecraftEnum()

class ColorUiProxy(clientApi.GetUIScreenProxyCls()):
    def __init__(self, namespace, systemname):
        super(ColorUiProxy, self).__init__(namespace, systemname)
        super(self.GetScreenNode(), self).__init__(namespace, systemname)