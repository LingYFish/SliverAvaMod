from SliverAvaritiaScript.api.server.BaseServerSystem import BaseServerSystem
from SliverAvaritiaScript.modConfig import *
from SliverAvaritiaScript.api.lib.unicodeUtils import UnicodeConvert
import mod.client.extraClientApi as clientApi
import json
import uuid
compFactory = clientApi.GetEngineCompFactory()
levelId = clientApi.GetLevelId()
minecraftEnum = clientApi.GetMinecraftEnum()
localId = clientApi.GetLocalPlayerId()
class SliverAvaritiaServerSystem(BaseServerSystem):
    gameComp = compFactory.CreateGame(levelId)

    def __init__(self, namespace, systemName):
        BaseServerSystem.__init__(self, namespace, systemName)