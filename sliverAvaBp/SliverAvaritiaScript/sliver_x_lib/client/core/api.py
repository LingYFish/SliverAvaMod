if 1>2:
    from . import extraClientApi as _clientApi
    from ClientSystem import ClientSystem as clientSystem
    from ui.screenNode import ScreenNode as screenNode
import mod.client.extraClientApi as _sliver_x_clientApi
from mod.client.ui.screenNode import ScreenNode as _ScreenNode
ScreenNode = _ScreenNode #type:screenNode
extraClientApi = _sliver_x_clientApi #type: _clientApi
ViewBinder = extraClientApi.GetViewBinderCls()
from ... import config
from ...util.log import logger
lambda : "By:SliverX"
engineNameSpace = "Minecraft"
engineSystemName = "Engine"
clientSystem = extraClientApi.GetClientSystemCls()
compFactory = extraClientApi.GetEngineCompFactory()
levelId = extraClientApi.GetLevelId()
clientApi = extraClientApi

class SliverClientSystem(clientSystem):
    modName = config.modName
    modVersion = config.modVersion
    __attr = 'clientSystem'

    def __init__(self, namespace, systemName):
        clientSystem.__init__(self,namespace, systemName)
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

    def addListenEventUi(self, screen, func, namespace = engineNameSpace, systemName = engineSystemName, eventName = '', priority = 0):
        #type: (object,function,str,str,str,int) -> None
        """
        | 在UI中的事件监听功能

        ----------------

        - object screen: uiNode
        - method func: 监听函数
        - str namespace: 命名空间
        - str systemName: 系统名称
        - str eventName: 函数名称
        - int priority: 优先级
        - None return: 无

        """
        self.ListenForEvent(namespace, systemName, eventName, screen, func, priority)

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
    
    def removeListenEvent(self, func, namespace = 'Minecraft', systemName = 'Engine', eventName = '', priority = 0):
        self.UnListenForEvent(namespace, systemName, eventName, self, func, priority)
    
    def serverCaller(self, funcName, args):
        #type: (str,dict) -> None
        """
        | 给服务端发送事件

        ----------------

        - str clientId: 玩家客户端Id
        - str funcName: 要发送的事件名称
        - dict args: 事件信息
        - None return: 无

        """
        self.NotifyToServer(funcName, args)
    
    def getConfigData(self,configName='__ClientConfigData__',isGlobal=False):
        #type: (str,bool) -> dict
        """
        | 获取本地信息数据

        ----------------

        - str configName: 配置名称，只能包含字母、数字和下划线字符，另外为了避免addon之间的冲突，建议加上addon的命名空间作为前缀
        - bool isGlobal: 	为True时是全局配置，否则为存档配置，默认为False
        - dict|None return: 本地保存的数据

        """
        return compFactory.CreateConfigClient(levelId).GetConfigData(configName, isGlobal)
    
    def setConfigData(self,configName,vaule,isGlobal):
        #type: (str,dict,bool) -> dict
        """
        | 设置本地信息数据

        ----------------

        - str configName: 配置名称，只能包含字母、数字和下划线字符，另外为了避免addon之间的冲突，建议加上addon的命名空间作为前缀
        - dict vaule: 数据
        - bool isGlobal: 为True时是全局配置，否则为存档配置，默认为False
        - None return: 无

        """
        return compFactory.CreateConfigClient(levelId).SetConfigData(configName, vaule, isGlobal)