class ClientSystem:

    def __init__(self, namespace, systemName):
        self.namespace = namespace
        self.systemName = systemName
        self.registerEvents = []
        self.notifyEvents = {}
        self.nameToListenEvents = {}

    def DefineEvent(self, eventName):
        """
        define event
        """
        pass

    def UnDefineEvent(self, eventName):
        """
        undefine event
        """
        eventID = self.namespace + ':' + self.systemName + ':' + eventName
        if eventID not in self.registerEvents:
            return
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
        broadcast own event with event_name
        """
        pass

    def BroadcastToAllClient(self, eventName, eventData):
        pass

    def NotifyToServer(self, eventName, eventData):
        """
        @description 客户端发送事件到服务器
        @classify_path 通用/事件
        @param eventName str 事件名
        @param eventData dict 事件参数，一般用CreateEventData的返回值
        @example
        import mod.client.extraClientApi as clientApi
        ClientSystem = clientApi.GetClientSystemCls()
        class FpsClientSystem(ClientSystem):
                def NotifyToServerTest(self, args):
                        self.NotifyToServer("bulletShootEvent", args)
        /example
        """
        pass

    def CreateEngineSfx(self, path, pos = None, rot = None, scale = None):
        """
        @description 创建序列帧特效
        @classify_path 特效/序列帧
        @param path str 特效资源路径，不用后缀名
        @param pos tuple(float,float,float) 创建位置，可选，没传则可以创建完用frameAniTrans组件设置
        @param rot tuple(float,float,float) 角度，可选，没传则可以创建完用frameAniTrans组件设置
        @param scale tuple(float,float,float) 缩放系数，可选，没传则可以创建完用frameAniTrans组件设置
        @return int或None frameEntityId或者None
        @comment 创建序列帧后，可以用返回的frameEntityId创建序列帧分类中的相关组件，设置所需属性，以实现各种表现效果
        /comment
        @comment 切换维度后会自动隐藏非本维度创建的而且没有绑定实体的序列帧, 回到该维度后会自动重新显示
        /comment
        @comment 需要注意，序列帧创建之后需要调用frameAniControl组件的play函数才会播放,如果播放非本维度创建的序列帧,会同时修改该序列帧的创建维度为当前维度
        /comment
        @example
        import mod.client.extraClientApi as clientApi
        class MyClientSystem(ClientSystem):
                # 创建
                def createSfx(self):
                        frameEntityId = self.CreateEngineSfx("textures/sfxs/snow_3")
                        frameAniTransComp = clientApi.GetEngineCompFactory().CreateFrameAniTrans(frameEntityId)
                        frameAniTransComp.SetPos((10,10,10))
                        frameAniTransComp.SetRot((0,0,0))
                        frameAniTransComp.SetScale((1,1,1))
                        frameAniControlComp = clientApi.GetEngineCompFactory().CreateFrameAniControl(frameEntityId)
                        frameAniControlComp.Play()
        
                # 删除
                def removeSfx(self, frameEntityId):
                        self.DestroyEntity(frameEntityId)
        /example
        """
        pass

    def CreateEngineSfxFromEditor(self, path, pos = None, rot = None, scale = None):
        """
        @description 指使用资源包中effects/xxx.json，按照编辑器中编辑好的参数创建序列帧。支持环状序列帧
        @classify_path 特效/序列帧
        @param path str 特效配置路径，需要为"effects/xxx.json"，"xxx"为编辑器创建序列帧时填写的名称
        @param pos tuple(float,float,float) 创建位置，可选，没传则可以创建完用frameAniTrans组件设置，一般需要设置播放的位置
        @param rot tuple(float,float,float) 角度，可选，没传则可以创建完用frameAniTrans组件设置
        @param scale tuple(float,float,float) 缩放系数，可选，没传则可以创建完用frameAniTrans组件设置
        @return int或None frameEntityId或者None
        @comment 创建序列帧后，可以用返回的frameEntityId创建序列帧分类中的相关组件，设置所需属性，以实现各种表现效果
        /comment
        @comment 需要注意，序列帧创建之后需要调用frameAniControl组件的play函数才会播放
        /comment
        @comment 根据editor配置生成序列帧后还需要设置位置或绑定，以及进行播放。
        /comment
        @example
        import mod.client.extraClientApi as clientApi
        class MyClientSystem(ClientSystem):
                # 创建
                def createSfxFromEditor(self):
                        frameEntityId = self.CreateEngineSfxFromEditor("effects/mySfx.json")
                        frameAniTransComp = clientApi.GetEngineCompFactory().CreateFrameAniTrans(frameEntityId)
                        frameAniTransComp.SetPos((10,10,10))
                        frameAniTransComp.SetRot((0,0,0))
                        frameAniTransComp.SetScale((1,1,1))
                        frameAniControlComp = clientApi.GetEngineCompFactory().CreateFrameAniControl(frameEntityId)
                        frameAniControlComp.Play()
        
                # 删除
                def removeSfx(self, frameEntityId):
                        self.DestroyEntity(frameEntityId)
        /example
        """
        pass

    def CreateEngineParticle(self, path, pos):
        """
        @description 用于创建粒子特效
        @classify_path 特效/粒子
        @param path str 特效资源路径，需要加上后缀名（一般是json）
        @param pos tuple(float,float,float) 创建位置坐标
        @return int或None particleEntityId或者None
        @comment 创建粒子后，可以用返回的particleEntityId创建客户端粒子分类中的相关组件，设置所需属性，以实现各种表现效果。
        /comment
        @comment 切换维度后会自动隐藏非本维度创建的而且没有绑定实体的粒子, 回到该维度后会自动重新显示
        /comment
        @comment 粒子创建之后需要调用particleControl组件的Play函数才会播放，如果播放非本维度创建的粒子,会同时修改该粒子的创建维度为当前维度
        /comment
        @example
        import mod.client.extraClientApi as clientApi
        class MyClientSystem(ClientSystem):
                # 创建
                def createParticle(self):
                        particleEntityId = self.CreateEngineParticle("effects/fire.json", (0,5,0))
                        particleControlComp = clientApi.GetEngineCompFactory().CreateParticleControl(particleEntityId)
                        particleControlComp.Play()
        
                # 删除
                def removeParticle(self, particleEntityId):
                        self.DestroyEntity(particleEntityId)
        /example
        """
        pass

    def CreateEngineEffect(self, path, bindEntity, aniName):
        """
        @description 指用编辑器保存资源包中models/effect/xxx_effect.json生成编辑好的所有挂点的所有特效。生成的特效会自动进行挂接及播放，编辑器中设为不可见的特效也会进行播放。并且使用这种方式创建的特效，开发者不用维护entity进出视野导致的挂接特效被移除，引擎会在entity每次进入视野时自动创建所有特效。
        @classify_path 特效/模型特效
        @deprecated 1.25 请使用CreateEngineEffectBind
        @param path str 特效配置路径，需要包含json后缀名
        @param bindEntity str 绑定实体的Id
        @param aniName str 选择使用哪个模型动作的特效
        @return int或None effectEntityId或者None
        @comment 创建特效前需要将entity的骨骼模型替换为编辑器中的一致（或者其他骨骼相同的模型），否则将挂接失败，替换模型见服务端和客户端的model组件。
        /comment
        @comment 暂不支持挂接原版史蒂夫的特效。
        /comment
        @example
        import mod.client.extraClientApi as clientApi
        class MyClientSystem(ClientSystem):
                # 创建
                def createEffect(self):
                        # 绑定在本地玩家身上的模型特效
                        effectEntityId = self.CreateEngineEffect("models/effect/xuenv_effect.json", extraClientApi.GetLocalPlayerId(), 'idle')
        
                # 删除
                def removeEffect(self, effectEntityId):
                        self.DestroyEntity(effectEntityId)
        /example
        """
        pass

    def CreateEngineEffectBind(self, path, bindEntity, aniName):
        """
        @description 指用编辑器保存资源包中models/bind/xxx_bind.json生成编辑好的所有挂点的所有特效。生成的特效会自动进行挂接及播放，编辑器中设为不可见的特效也会进行播放。并且使用这种方式创建的特效，开发者不用维护entity进出视野导致的挂接特效被移除，引擎会在entity每次进入视野时自动创建所有特效。
        @classify_path 特效/模型特效
        @state 1.25 新增 cyk 指用编辑器保存资源包中models/bind/xxx_bind.json生成编辑好的所有挂点的所有特效
        @param path str 特效配置路径，需要包含json后缀名
        @param bindEntity str 绑定实体的Id
        @param aniName str 选择使用哪个模型动作的特效
        @return int或None effectEntityId或者None
        @comment 创建特效前需要将entity的骨骼模型替换为编辑器中的一致（或者其他骨骼相同的模型），否则将挂接失败，替换模型见服务端和客户端的model组件的SetModel接口。
        /comment
        @example
        import mod.client.extraClientApi as clientApi
        class MyClientSystem(ClientSystem):
                # 创建
                def createEffect(self):
                        # 绑定在本地玩家身上的模型特效
                        effectEntityId = self.CreateEngineEffectBind("models/bind/xuenv_bind.json", clientApi.GetLocalPlayerId(), 'idle')
        
                # 删除
                def removeEffect(self, effectEntityId):
                        self.DestroyEntity(effectEntityId)
        /example
        """
        pass

    def DestroyEntity(self, entityId):
        """
        @description 销毁特效
        @classify_path 特效/通用
        @state 1.19 调整 gzhuabo 增加销毁实体返回值
        @param entityId int 销毁的特效ID
        @return bool 是否销毁成功
        @comment 支持销毁粒子，序列帧及模型特效，示例见对应的创建接口
        /comment
        """
        pass

    def NotifyToServerNode(self, targetId, eventName, eventData):
        pass

    def NotifyToMaster(self, eventName, eventData):
        pass

    def NotifyToClient(self, targetId, eventName, eventData):
        pass

    def GetLocalPlayer(self):
        pass

    def _GetApp(self):
        pass

    def AddListenUpdateComponent(self, listenEntityId, comp):
        pass

    def DestroyEvents(self):
        pass

    def Destroy(self):
        pass

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

    def NotifyToClient(self, targetId, eventName, eventData):
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