import mod.client.extraClientApi as clientApi
ClientSystem = clientApi.GetClientSystemCls()
class BaseClientSystem(ClientSystem):
    ClientName = ''
    ModName = ''
    ModVersion = '0.0.1'
    ListenEventUi = []

    def __init__(self, namespace, systemName):
        ClientSystem.__init__(self, namespace, systemName)
    
    def addListenEvent(self, func, namespace = 'Minecraft', systemName = 'Engine', eventName = '', priority = 0):
        self.ListenForEvent(namespace, systemName, eventName, self, func, priority)

    def addListenEventUi(self, screen, func, namespace = 'Minecraft', systemName = 'Engine', eventName = '', priority = 0):
        self.ListenForEvent(namespace, systemName, eventName, screen, func, priority)
    
    def removeListenEvent(self, func, namespace = 'Minecraft', systemName = 'Engine', eventName = '', priority = 0):
        self.UnListenForEvent(namespace, systemName, eventName, self, func, priority)
    
    def serverCaller(self, funcName, args):
        self.NotifyToServer(funcName, args)

    def Version(self):
        return 
    
    def getConfigData(self,configName='__ClientConfigData__',isGlobal=False):
        """
        - 获取本地数据
        - configName : 配置名称，只能包含字母、数字和下划线字符，另外为了避免addon之间的冲突，建议加上addon的命名空间作为前缀
        - isGlobal : 	为True时是全局配置，否则为存档配置，默认为False
        """
        #type: (str,bool) -> dict
        return clientApi.GetEngineCompFactory().CreateConfigClient(clientApi.GetLevelId()).GetConfigData(configName, isGlobal)
    
    def setConfigData(self,configName,vaule,isGlobal):
        """
        - 获取本地数据
        - configName : 配置名称，只能包含字母、数字和下划线字符，另外为了避免addon之间的冲突，建议加上addon的命名空间作为前缀
        - vaule : 数据
        - isGlobal : 	为True时是全局配置，否则为存档配置，默认为False
        """
        #type: (str,str,bool) -> dict
        return clientApi.GetEngineCompFactory().CreateConfigClient(clientApi.GetLevelId()).SetConfigData(configName, vaule, isGlobal)