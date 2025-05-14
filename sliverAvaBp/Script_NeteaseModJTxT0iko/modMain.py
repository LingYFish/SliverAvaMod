# -*- coding: utf-8 -*-

from mod.common.mod import Mod


@Mod.Binding(name="Script_NeteaseModJTxT0iko", version="0.0.1")
class Script_NeteaseModJTxT0iko(object):

    def __init__(self):
        pass

    @Mod.InitServer()
    def Script_NeteaseModJTxT0ikoServerInit(self):
        pass

    @Mod.DestroyServer()
    def Script_NeteaseModJTxT0ikoServerDestroy(self):
        pass

    @Mod.InitClient()
    def Script_NeteaseModJTxT0ikoClientInit(self):
        pass

    @Mod.DestroyClient()
    def Script_NeteaseModJTxT0ikoClientDestroy(self):
        pass
