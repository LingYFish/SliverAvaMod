if 1>2:
    from . import extraServerApi as _serverApi
    from ServerSystem import ServerSystem as serverSystem
import mod.server.extraServerApi as _sliver_x_serverApi
extraServerApi = _sliver_x_serverApi #type: _serverApi
from ... import config
from ...util.log import logger
lambda : "By:SliverX"
engineNameSpace = "Minecraft"
engineSystemName = "Engine"
serverSystem = extraServerApi.GetServerSystemCls()
compFactory = extraServerApi.GetEngineCompFactory()
levelId = extraServerApi.GetLevelId()
serverApi = extraServerApi

class SliverServerSystem(serverSystem):
    modName = config.modName
    modVersion = config.modVersion
    __attr = 'serverSystem'

    def __init__(self, namespace, systemName):
        serverSystem.__init__(self, namespace, systemName)
        logger.debug("开始查找自定义监听装饰器")
        for method in dir(self):
            if hasattr(getattr(self,method),'event_list'):
                event_list = getattr(getattr(self,method),'event_list')
                for event in event_list:
                    _namespace = event[0]
                    _systemName = event[1]
                    eventName = event[2]
                    priority = event[3]
                    self.addListenEvent(func=getattr(self,method),systemName=_systemName,namespace=_namespace,eventName=eventName,priority=priority)

    @staticmethod
    def ListenEvent(namespace = engineNameSpace, systemName = engineSystemName, eventName = '',priority=0):
        def warp(func):
            if hasattr(func,'event_list'):
                func.event_list.append((namespace,systemName,eventName if eventName != '' else func.__name__,priority))
            else:
                func.event_list = [(namespace,systemName,eventName if eventName != '' else func.__name__,priority),]
            return func
        return warp
    
    def addListenEvent(self, func, namespace = engineNameSpace, systemName = engineSystemName, eventName = '', priority = 0):
        #type: (function,str,str,str,int) -> None
        """
        | 事件监听功能

        ----------------

        - method func: 监听函数
        - str namespace: 命名空间
        - str systemName: 系统名称
        - str eventName: 函数名称
        - int priority: 优先级
        - None return: 无

        """
        self.ListenForEvent(namespace, systemName, eventName, self, func, priority)

    def removeListenEvent(self, func, namespace = engineNameSpace, systemName = engineSystemName, eventName = '', priority = 0):
        #type: (function,str,str,str,int) -> None
        """
        | 删除事件监听功能

        ----------------

        - method func: 监听函数
        - str namespace: 命名空间
        - str systemName: 系统名称
        - str eventName: 函数名称
        - int priority: 优先级
        - None return: 无

        """
        self.UnListenForEvent(namespace, systemName, eventName, self, func, priority)
    
    def clientCaller(self, clientId, funcName, args):
        #type: (str,str,dict) -> None
        """
        | 给单独客户端Id发送事件

        ----------------

        - str clientId: 玩家客户端Id
        - str funcName: 要发送的事件名称
        - dict args: 事件信息
        - None return: 无

        """
        self.NotifyToClient(clientId, funcName, args)
    
    def CallAllclient(self, funcName, args):
        """
        | 给所有客户端Id发送事件

        ----------------
        
        - str funcName: 要发送的事件名称
        - dict args: 事件信息
        - None return: 无

        """
        self.NotifyToMultiClients(extraServerApi.GetPlayerList(),funcName, args)