from ..sliver_x_lib.client.core import api as cApi
from ..sliver_x_lib.server.core import api as sApi
from util.log import logger
from config import *

serverApi = sApi.extraServerApi
clientApi = cApi.extraClientApi

class Mod(object):

    @staticmethod
    def Binding(name, version = None):
        def _binding(cls):
            cls.MOD_NAME = name
            cls.VERSION = version
            return cls
        return _binding

    @staticmethod
    def InitClient():
        def _initClient(func):
            func.InitClient = 'initClient'
            return func
        return _initClient

    @staticmethod
    def DestroyClient():
        def _destroyClient(func):
            func.DestroyClient = 'destroyClient'
            return func
        return _destroyClient

    @staticmethod
    def InitServer():

        def _initServer(func):
            func.InitServer = 'initServer'
            return func
        return _initServer

    @staticmethod
    def DestroyServer():
        def _destroyServer(func):
            func.DestroyServer = 'destroyServer'
            return func
        return _destroyServer

    @staticmethod
    def InitMaster():
        def _initMaster(func):
            func.InitMaster = 'initMaster'
            return func
        return _initMaster

    @staticmethod
    def DestroyMaster():
        def _destroyMaster(func):
            func.DestroyMaster = 'destroyMaster'
            return func
        return _destroyMaster

    @staticmethod
    def InitService():
        def _initService(func):
            func.InitService = 'initService'
            return func
        return _initService

    @staticmethod
    def DestroyService():
        def _destroyService(func):
            func.DestroyService = 'destroyService'
            return func
        return _destroyService

dirName = cApi.SliverClientSystem.__module__.split(".")[0]

@Mod.Binding(modName,modVersion)
class ModLoader(object):
    ServerSystem = []
    ClientSystem = []
    def __init__(self):
        pass
    
    @Mod.InitServer()
    def initServer(self):
        logger.debug("====={} initServer=====".format(modName))
        for systemName, systemPath in ModLoader.ServerSystem:
            serverApi.RegisterSystem(modName, systemName, systemPath)
    
    @Mod.InitClient()
    def initClient(self):
        logger.debug("====={} initClient=====".format(modName))
        for systemName, systemPath in ModLoader.ClientSystem:
            clientApi.RegisterSystem(modName, systemName, systemPath)

def server(Name,path):
    ModLoader.ServerSystem.append(
        (
            Name,
            "{}.{}".format(dirName,path)
        )
    )

def client(Name,path):
    ModLoader.ClientSystem.append(
        (
            Name,
            "{}.{}".format(dirName,path)
        )
    )

def Init():
    loader = ModLoader()
    loader.initClient()
    loader.initServer()