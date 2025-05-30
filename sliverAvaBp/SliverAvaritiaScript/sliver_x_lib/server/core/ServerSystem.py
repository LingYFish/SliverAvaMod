class ServerSystem:

    def __init__(self, namespace, systemName):
        self.eventIDHead = namespace + ':' + systemName + ':'
        self.namespace = namespace
        self.systemName = systemName
        self.registerEvents = []
        self.notifyEvents = {}
        self.nameToListenEvents = {}

    def NotifyToClient(self, targetId, eventName, eventData):
        """
        @description 服务器发送事件到指定客户端
        @classify_path 通用/事件
        @param targetId str 客户端对应的Id，一般就是玩家Id
        @param eventName str 事件名
        @param eventData dict 事件参数，一般用CreateEventData的返回值
        """
        self.CreateEventData

    def DefineEvent(self, eventName):
        """
        @deprecated 1.21 监听自定义事件前不再需要DefineEvent
        @description 定义自定义事件
        @param eventName str 事件名
        @example
        import mod.server.extraServerApi as serverApi
        ServerSystem = serverApi.GetServerSystemCls()
        class FpsServerSystem(ServerSystem):
                def DefineEventTest(self):
                        self.DefineEvent('BulletHit')
        /example
        """
        pass

    def UnDefineEvent(self, eventName):
        """
        @deprecated 2.3 监听自定义事件前不再需要DefineEvent，所以也不再需要使用UnDefineEvent
        @description 取消自定义事件
        @classify_path 通用/事件
        @param eventName str 事件名
        @example
        import mod.server.extraServerApi as serverApi
        ServerSystem = serverApi.GetServerSystemCls()
        class FpsServerSystem(ServerSystem):
                def UnDefineEventTest(self):
                        self.UnDefineEvent('BulletHit')
        /example
        """
        pass

    def CreateEventData(self):
        """
        @description 创建自定义事件的数据，eventData用于发送事件。创建的eventData可以理解为一个dict，可以嵌套赋值dict,list和基本数据类型，但不支持tuple
        @classify_path 通用/事件
        @return dict 事件数据
        @example
        import mod.server.extraServerApi as serverApi
        ServerSystem = serverApi.GetServerSystemCls()
        class FpsServerSystem(ServerSystem):
                def shoot(self):
                        shootData = self.CreateEventData()
                        shootData["id"] = self.mPlayerId
                        # 向客户端发送事件，传递了一个playerId
                        self.NotifyToClient('-12345678910','BulletHit', shootData)
        /example
        """
        return {}

    def ListenForEvent(self, namespace, systemName, eventName, instance, func, priority = 0):
        """
        @description 注册监听某个系统抛出的事件。若监听引擎事件时，namespace和systemName分别为GetEngineNamespace()和GetEngineSystemName()。具体每个事件的详细事件data可以参考"事件"分类下的内容
        @classify_path 通用/事件
        @state 2.2 调整 czh 客户端系统事件的参数会自带客户端玩家id
        @param namespace str 所监听事件的来源系统的namespace
        @param systemName str 所监听事件的来源系统的systemName
        @param eventName str 事件名
        @param instance any 回调函数所属的类的实例
        @param func function 回调函数
        @param priority int 这个回调函数的优先级。默认值为0，这个数值越大表示被执行的优先级越高，最高为10。
        @comment 服务端system监听的客户端系统事件的回调参数中会自带一个叫"\\_\\_id\\_\\_"的key，值为对应客户端的玩家id
        /comment
        @example
        import mod.server.extraServerApi as serverApi
        ServerSystem = serverApi.GetServerSystemCls()
        class FpsServerSystem(ServerSystem):
                def ListenEvent(self):
                        # 监听了引擎事件'ServerChatEvent'
                        self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), 'ServerChatEvent', self, self.OnServerChat)
                        # 监听客户端系统事件
                        self.ListenForEvent("MyFpsMod", "FpsClientSystem", "MyEvent", self, self.OnMyEvent)
        
                def OnServerChat(self, args):
                        print 'OnServerChat', args
        
                def OnMyEvent(self, args):
                        print 'OnMyEvent', args['__id__'], args
        /example
        """
        pass

    def UnListenForEvent(self, namespace, systemName, eventName, instance, func, priority = 0):
        """
        @description 反注册监听某个系统抛出的事件，即不再监听。若是引擎事件，则namespace和systemName分别为[GetEngineNamespace](#getenginenamespace)和[GetEngineSystemName](#getenginesystemname)。与ListenForEvent对应。
        @classify_path 通用/事件
        @param namespace str 所监听事件的来源系统的namespace
        @param systemName str 所监听事件的来源系统的systemName
        @param eventName str 事件名
        @param instance any 回调函数所属的类的实例
        @param func function 回调函数
        @param priority int 这个回调函数的优先级。默认值为0，这个数值越大表示被执行的优先级越高。
        @example
        import mod.server.extraServerApi as serverApi
        ServerSystem = serverApi.GetServerSystemCls()
        class FpsServerSystem(ServerSystem):
                def ListenEvent(self):
                        # 服务端脚本自定义了1个事件
                        self.DefineEvent('BulletHit')
                        # 服务器端脚本监听了引擎的1个事件'ServerChatEvent'
                        self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), 'ServerChatEvent', self, self.OnServerChat)
                def UnListenEvent(self):
                        # 取消自定义的事件
                        self.UnDefineEvent('BulletHit')
                        # 取消监听的系统事件
                        self.UnListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), 'ServerChatEvent', self, self.OnServerChat)
        /example
        """
        pass

    def UnListenAllEvents(self):
        """
        @description 反注册监听某个系统抛出的所有事件，即不再监听。
        @state 1.18 新增 gzhuabo 反注册监听某个系统抛出的所有事件，即不再监听。
        @classify_path 通用/事件
        @example
        import mod.server.extraServerApi as serverApi
        ServerSystem = serverApi.GetServerSystemCls()
        class FpsServerSystem(ServerSystem):
                def ListenEvent(self):
                        # 服务端脚本自定义了1个事件
                        self.DefineEvent('BulletHit')
                        # 服务器端脚本监听了引擎的1个事件'ServerChatEvent'
                        # 具体每个事件的详细事件data可以参考《MODSDK文档》
                        self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), 'ServerChatEvent', self, self.OnServerChat)
                def UnListenEvent(self):
                        # 取消自定义的事件
                        self.UnDefineEvent('BulletHit')
                        # 取消监听的系统事件
                        self.UnListenAllEvents()
        /example
        """
        pass

    def ListenForEngine(self, namespace, systemName, eventName, instance, func, priority):
        """
        listen for system event at engine
        """
        pass

    def SetEngineEventCanceled(self, namespace, systemName, eventName, cancel):
        """
        cancel engine event, c++ don't post this event
        """
        pass

    def BroadcastEvent(self, eventName, eventData):
        """
        @description 本地广播事件，客户端system广播的事件仅客户端system能监听，服务器system广播的事件仅服务端system能监听。
        @classify_path 通用/事件
        @param eventName str 事件名
        @param eventData dict 事件参数，一般用CreateEventData的返回值
        @example
        import mod.server.extraServerApi as serverApi
        ServerSystem = serverApi.GetServerSystemCls()
        class FpsServerSystem(ServerSystem):
                def BroadCastEventTest(self, args):
                        self.BroadcastEvent("bulletShootEvent", args)
        /example
        """
        pass

    def BroadcastToAllClient(self, eventName, eventData):
        pass

    def NotifyToServer(self, eventName, eventData):
        pass

    def NotifyToServerNode(self, targetId, eventName, eventData):
        pass

    def NotifyToMaster(self, eventName, eventData):
        pass

    def Update(self):
        """
        do update for every event in this method
        """
        pass

    def Destroy(self):
        """
        do remove for every event in this method
        """
        pass

    def _GetApp(self):
        pass

    def GetNeedUpdate(self):
        pass

    def GetComponent(self, entityId, nameSpace, name):
        """
        @deprecated 1.21.nodoc 请使用extraApi
        @description 获取实体的组件。一般用来判断某个组件是否创建过，其他情况请使用CreateComponent
        @param entityId str 该组件属主的实体id
        @param nameSpace str 组件的命名空间，registerComponent的namespace
        @param name str 组件的名字
        @return BaseComponent 组件实例或者None
        @example
        import mod.server.extraServerApi as serverApi
        # entityId 根据游戏实际Id获取，这里'-12345678910'只是随便写的
        comp = serverApi.GetComponent(‘-12345678910’, "Minecraft", "item")
        # 拿到comp后就可以做一些逻辑内容，如果没有创建过会返回None
        /example
        """
        pass

    def GetCompData(self, comp, moduleName, funcName, *args):
        pass

    def RegisterComponent(self, nameSpace, name, clsPath):
        pass

    def NeedsUpdate(self, comp):
        pass

    def CreateComponent(self, entityId, nameSpace, name):
        """
        @deprecated 1.21.nodoc 请使用extraApi
        @description 给实体创建组件
        @param entityId str或int 该组件属主的实体id
        @param nameSpace str 组件的命名空间，registerComponent的namespace
        @param name str 组件的名字
        @return BaseComponent 组件实例
        @example
        import mod.server.extraServerApi as serverApi
        # entityId 根据游戏实际Id获取，这里'-12345678910'只是随便写的
        comp = serverApi.CreateComponent('-12345678910', "Minecraft", "item")
        # 拿到comp后就可以做一些逻辑内容，与GetComponent类似，如果已经创建会自动直接Get
        /example
        """
        pass

    def DestroyComponent(self, entityId, nameSpace, name):
        """
        @deprecated 1.21.nodoc 请使用extraApi
        @description 删除实体的组件
        @param entityId str 该组件属主的实体id
        @param nameSpace str 组件的命名空间，registerComponent的namespace
        @param name str 组件的名字
        @example
        import mod.server.extraServerApi as serverApi
        # entityId 根据游戏实际Id获取，这里'-12345678910'只是随便写的
        comp = serverApi.DestroyComponent('-12345678910', "Minecraft", "item")
        /example
        """
        pass

    def HasComponent(self, entityId, nameSpace, name):
        pass

    def RegisterView(self):
        pass

    def AddFilterToView(self, view, nameSpace, name):
        pass

    def GetEntitiesFromView(self, view):
        pass

    def CreateTempEntity(self):
        pass

    def CreateEngineEntity(self, engineType, pos, rot, dimensionId = None, isNpc = False, playerId = None):
        """
        @deprecated 1.19 请使用CreateEngineEntityByTypeStr
        @description **服务端系统接口**，用于创建生物类型的实体，具体参见创建实体部分内容
        @param engineType MinecraftEnum.EntityType 生物类型
        @param pos tuple(float,float,float) 生成坐标
        @param rot tuple(float,float) 生物面向
        @param dimensionId int 生成的维度，默认值为0（0为主世界，1为地狱，2为末地）
        @param isNpc bool 是否为npc，默认值为False。npc不会移动、转向、存盘。
        @return str或None 实体Id或者None
        @comment 生成村民请使用EntityType.VillagerV2
        /comment
        """
        pass

    def CreateEngineEntityByTypeStr(self, engineTypeStr, pos, rot, dimensionId = 0, isNpc = False):
        pass

    def CreateEngineBullet(self, shooterId, engineType, pos, direction, power, gravity = None, damage = None, targetId = '-1', isDamageOwner = None):
        """
        @deprecated 1.18 请使用新接口CreateProjectileEntity
        @description **服务端系统接口**，用于创建抛射物类型的实体，具体参见创建实体部分内容
        @param shooterId str 发射者entityId
        @param engineType MinecraftEnum.EntityType 弹射物类型
        @param pos tuple(float,float,float) 生成坐标
        @param direction tuple(float,float,float) 弹射物飞行方向
        @param power float 弹射物飞行速度
        @param gravity float 弹射物所受重力
        @param damage float 弹射物造成的伤害值
        @return str或None 实体Id或者None
        """
        pass

    def CreateEngineItem(self, pos, itemId, count = 1, auxVal = 0, modExtVal = '', showInHand = True, extraId = None, playerId = None, modVal = -1):
        pass

    def CreateEngineItemEntity(self, itemDict, dimensionId = 0, pos = (0, 0, 0)):
        pass

    def CreateEngineSfx(self, path, pos = None, rot = None, scale = None):
        pass

    def CreateEngineSfxFromEditor(self, path, pos = None, rot = None, scale = None):
        pass

    def CreateEngineParticle(self, path, pos):
        pass

    def CreateEngineEffect(self, path, bindEntity, aniName):
        pass

    def CreateEngineEffectBind(self, path, bindEntity, aniName):
        pass

    def CreateEngineEffectForHumanoid(self, path, bindEntity, aniName):
        pass

    def RemoveEngineEffectForHumanoid(self, bindEntity):
        pass

    def CreateEngineTextboard(self, text, ownerId, pos, textColor, tagColor, size = 1.0, depthTest = True):
        pass

    def RegisterExpressionNode(self, expressionStr, func):
        pass

    def UnRegisterExpressionNode(self, expressionStr):
        pass

    def CreateEntity(self, entity):
        pass

    def DestroyEntity(self, entityId):
        pass

    def GetLevelId(self):
        pass

    def AddListenEvent(self, namespace, systemName, eventName, instance, func, priority):
        pass

    def RemoveListenEvent(self, namespace, systemName, eventName, instance, func, priority):
        pass

    def GetPlatform(self):
        """
        @deprecated 1.21.nodoc 请使用extraApi
        @description 获取脚本运行的平台
        @state 1.18 新增 gzhuabo 获取脚本运行的平台
        @return int 0：Windows平台；1：IOS；2：Android
        @classify_path 通用/本地设备
        """
        pass

    def DefineEvent(self, eventName):
        """
        define event
        """
        pass

    def UnDefineEvent(self, eventName):
        """
        undefine event
        """
        pass

    def ListenForEventEngine(self, eventName, instance, func, priority = 0):
        """
        listen a certain event with func of instance
        """
        pass

    def ListenForEvent(self, namespace, systemName, eventName, instance, func, priority = 0):
        """
        listen a certain event with func of instance
        """
        pass

    def UnListenForEvent(self, namespace, systemName, eventName, instance, func, priority = 0):
        """
        unlisten a certain event with func of instance
        """
        pass

    def UnListenAllEvents(self):
        """
        unlisten all events
        """
        pass

    def ListenForEngine(self, namespace, systemName, eventName, instance, func, priority = 0):
        pass

    def SetEngineEventCanceled(self, namespace, systemName, eventName, cancel):
        """
        cancel engine event, c++ don't post this event
        """
        pass

    def BroadcastEvent(self, eventName, eventData):
        """
        broadcast own event with event name
        """
        pass

    def BroadcastEventWithID(self, eventID, eventData):
        pass

    def BroadcastToAllClient(self, eventName, eventData):
        """
        @description 服务器广播事件到所有客户端
        @classify_path 通用/事件
        @param eventName str 事件名
        @param eventData dict 事件参数，一般用CreateEventData的返回值
        @example
        import mod.server.extraServerApi as serverApi
        ServerSystem = serverApi.GetServerSystemCls()
        class FpsServerSystem(ServerSystem):
                def BroadCastEventTest(self, args):
                        self.BroadcastToAllClient("bulletShootEvent", args)
        
        /example
        """
        pass

    def NotifyToServer(self, eventName, eventData):
        pass

    def NotifyToServerNode(self, targetId, eventName, eventData):
        pass

    def NotifyToServiceNode(self, targetId, eventName, eventData):
        pass

    def BroadcastToService(self, eventName, eventData):
        pass

    def NotifyToMaster(self, eventName, eventData):
        pass

    def RequestToServiceMod(self, modname, method, args, callback = None, timeout = 2.0):
        """
        向使用指定modname的Mod发送一条请求型事件
        :param modname:
        :param method:
        :param args:
        :param callback:  (serverSystem, success, args) -> None
        :param timeout:
        :return:
        """
        pass

    def RequestToService(self, name, method, args, callback = None, timeout = 2.0):
        """
        :param name:
        :param method:
        :param args:
        :param callback:  (serverSystem, success, args) -> None
        :param timeout:
        :return:
        """
        pass

    def RequestToHashService(self, name, hashkey, method, args, callback = None, timeout = 2.0):
        pass

    def RequestSalogOutput(self, uid, keyname, log_dict):
        pass
    
    def RequestSalogUpdate(self, uid, playerId, sa_data):
        pass

    def RequestSalogLogout(self, uid, playerId):
        self.RequestToHashService('netease_salog', uid, 'salog_logout', {'uid': uid,
         'playerId': playerId})

    def NotifyToMultiClients(self, targetIdList, eventName, eventData):
        """
        @description 服务器发送事件到指定一批客户端，相比于在for循环内使用NotifyToClient性能更好
        @classify_path 通用/事件
        @state 2.0 新增 xltang  服务器发送事件到指定一批客户端
        @param targetIdList list(str) 客户端对应的playerId列表，playerId为玩家的entityId
        @param eventName str 事件名
        @param eventData dict 事件参数，一般用CreateEventData的返回值
        @example
        import mod.server.extraServerApi as serverApi
        ServerSystem = serverApi.GetServerSystemCls()
        class FpsServerSystem(ServerSystem):
                def NotifyToClientTest(self, args):
                        self.NotifyToMultiClients(['-1234567890', '-321654987'],"bulletShootEvent", args)
        /example
        """
        pass

    def CreateEngineEntityByTypeStr(self, engineTypeStr, pos, rot, dimensionId = 0, isNpc = False):
        """
        @description 创建指定identifier的实体
        @classify_path 世界/实体管理
        @param engineTypeStr str 实体identifier，例如'minecraft:husk'
        @param pos tuple(float,float,float) 生成坐标
        @param rot tuple(float,float) 生物面向
        @param dimensionId int 生成的维度，默认值为0（0为主世界，1为地狱，2为末地）
        @param isNpc bool 是否为npc，默认值为False。npc不会移动、转向、存盘。
        @return str或None 实体Id或者None
        @comment 在未加载的chunk无法创建
        生成村民请使用"minecraft:villager_v2"
        /comment
        @example
        import mod.server.extraServerApi as serverApi
        ServerSystem = serverApi.GetServerSystemCls()
        class MyServerSystem(ServerSystem):
                def createMob(self):
                        # 在主世界(0，5，0)的位置创建一个朝向为(0, 0)的尸壳
                        entityId = self.CreateEngineEntityByTypeStr('minecraft:husk', (0, 5, 0), (0, 0), 0)
        /example
        """
        pass

    def CreateEngineItemEntity(self, itemDict, dimensionId = 0, pos = (0, 0, 0)):
        """
        @description 用于创建物品实体（即掉落物），返回物品实体的entityId
        @classify_path 世界/实体管理
        @author hongshubin@corp
        @version 1.17
        @param itemDict dict <a href="../../../../mcguide/20-玩法开发/10-基本概念/1-我的世界基础概念.html#物品信息字典#物品信息字典">物品信息字典</a>
        @param dimensionId int 设置dimension，默认为主世界
        @param pos tuple(float,float,float) 生成坐标
        @return str或None 实体Id或者None
        @example
        import mod.server.extraServerApi as serverApi
        itemDict = {
                'itemName': 'minecraft:bow',
                'count': 1,
                'enchantData': [(serverApi.GetMinecraftEnum().EnchantType.BowDamage, 1),],
                'auxValue': 0,
                'customTips':'§c new item §r',
                'extraId': 'abc',
                'userData': { 'color': { '__type__':8, '__value__':'gray'} },
        }
        itemEntityId = self.CreateEngineItemEntity(itemDict, 0, (0, 5, 0))
        /example
        """
        pass

    def DestroyEntity(self, entityId):
        """
        @description 销毁实体
        @classify_path 世界/实体管理
        @state 1.19 调整 gzhuabo 增加销毁实体返回值
        @param entityId str 销毁的实体ID
        @return bool 是否销毁成功
        @example
        import mod.server.extraServerApi as serverApi
        ServerSystem = serverApi.GetServerSystemCls()
        class FpsServerSystem(ServerSystem):
                def testDestroyEntity(self, entityId):
                        self.DestroyEntity(entityId)
        /example
        """
        pass

    def RemoteNotifyToClient(self, neteaseId, proxyid, eventName, eventData):
        pass

    def RemoteBroadcastToClient(self, eventName, eventData):
        pass

    def _GetApp(self):
        pass

    def DestroyEvents(self):
        pass

    def Destroy(self):
        pass