import math
import mod.server.extraServerApi as serverApi
compFactory = serverApi.GetEngineCompFactory()
levelId = serverApi.GetLevelId()
minecraftEnum = serverApi.GetMinecraftEnum()

class Rot(object):
    def __init__(self,entityId):
        self.entityId = entityId

    def getEntityRotationTowardsTarget(self, target):
        """获取主实体对于其他实体的rot"""
        pos1 = compFactory.CreatePos(self.entityId).GetPos()
        targetPos = compFactory.CreatePos(target).GetPos()
        dx = targetPos[0] - pos1[0]
        dy = targetPos[1] - pos1[1]
        dz = targetPos[2] - pos1[2]
        horizontal_distance = math.sqrt(dx ** 2 + dz ** 2)
        pitch = math.atan2(dy, horizontal_distance)
        yaw = math.atan2(dz, dx)
        pitch = math.degrees(pitch)
        yaw = math.degrees(yaw)
        if yaw < 0:yaw += 360
        return (yaw, pitch)