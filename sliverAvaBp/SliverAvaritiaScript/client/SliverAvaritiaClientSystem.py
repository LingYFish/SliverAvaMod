from SliverAvaritiaScript.api.client.BaseClientSystem import BaseClientSystem
from SliverAvaritiaScript.modConfig import *
from SliverAvaritiaScript.api.lib.unicodeUtils import UnicodeConvert
import mod.client.extraClientApi as clientApi
import json
import uuid
compFactory = clientApi.GetEngineCompFactory()
levelId = clientApi.GetLevelId()
minecraftEnum = clientApi.GetMinecraftEnum()
localId = clientApi.GetLocalPlayerId()
class SliverAvaritiaClientSystem(BaseClientSystem):
    gameComp = compFactory.CreateGame(levelId)

    def __init__(self, namespace, systemName):
        BaseClientSystem.__init__(self, namespace, systemName)
        self.addListenEvent(self.UiInitFinished,eventName='UiInitFinished')

    def UiInitFinished(self,args):
        Data = {
			"name": "bloom_comsic",
			"enable": True,
            "paras": [
                # (threshold 门限 , strength 泛光强度, sigma 高斯模糊, bloom_size 泛光大小)
                { "name": "threshold", "value": 0.97, "range": [0.0, 1.0] }, 
                { "name": "strength", "value": 11.5, "range": [0.0, 10.0] },
                { "name": "sigma", "value": 10.0, "range": [0.0, 10.0] },
                { "name": "bloom_size", "value": 10.0, "range": [0.0, 10.0] }
            ],
            "pass_array":[
                {
                    "render_target":{"width":1.0,"height":1.0},
                    "material":"bloom_startMat",
                    "depth_enable": True
                },
                {
                    "render_target":{"width":1.0,"height":1.0},
                    "material":"bloom_processMat",
                    "depth_enable": True
                },
                {
                    "render_target":{"width":0.75,"height":0.75},
                    "material":"bloom_processMat",
                    "depth_enable": True
                },
                {
                    "render_target":{"width":0.5,"height":0.5},
                    "material":"bloom_processMat",
                    "depth_enable": True
                },
                {
                    "render_target":{"width":1.0,"height":1.0},
                    "material":"bloom_endMat",
                    "depth_enable": True
                }
            ]
        }
        PostProcessList = clientApi.GetEngineCompFactory().CreatePostProcess(levelId).GetPostProcessOrder()
        print ("开启后处理")
        if not PostProcessList:
            PostProcessList = []
        clientApi.GetEngineCompFactory().CreatePostProcess(levelId).AddPostProcess(Data, len(PostProcessList))
        print clientApi.GetEngineCompFactory().CreatePostProcess(levelId).SetEnableByName("bloom_comsic", True)