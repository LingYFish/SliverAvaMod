import mod.server.extraServerApi as serverApi
ServerSystem = serverApi.GetServerSystemCls()
class BaseServerSystem(ServerSystem):
    ServerName = ''
    ModName = ''
    ModVersion = '0.0.1'

    def __init__(self, namespace, systemName):
        ServerSystem.__init__(self, namespace, systemName)
    
    def addListenEvent(self, func, namespace = 'Minecraft', systemName = 'Engine', eventName = '', priority = 0):
        self.ListenForEvent(namespace, systemName, eventName, self, func, priority)

    def removeListenEvent(self, func, namespace = 'Minecraft', systemName = 'Engine', eventName = '', priority = 0):
        self.UnListenForEvent(namespace, systemName, eventName, self, func, priority)
    
    def clientCaller(self, clientId, funcName, args):
        self.NotifyToClient(clientId, funcName, args)
    
    def CallAllclient(self, funcName, args):
        self.BroadcastToAllClient(funcName, args)

    def Version(self):
        return 