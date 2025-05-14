import math
import mod.server.extraServerApi as serverApi
compFactory = serverApi.GetEngineCompFactory()
levelId = serverApi.GetLevelId()
minecraftEnum = serverApi.GetMinecraftEnum()
def entityNearByEntity(entityId, around=10, excludeTypes=[], includeTypes=[]):
    """
    查找指定实体附近最近的其他实体。
    
    参数:
    - entityId: 要查找的实体 ID。
    - around: 搜索范围的半径
    - excludeTypes: 排除的实体类型列表，如果为
    - includeTypes: 包含的实体类型列表，如果为
    
    返回:
    - (nearestEntityId, distance)
    """
    posComp = compFactory.CreatePos(entityId)
    arrowPos = posComp.GetPos()
    x, y, z = map(lambda x: int(x), arrowPos)
    dimensionComp = compFactory.CreateDimension(entityId)
    dimensionId = dimensionComp.GetEntityDimensionId()
    search_area_min = (x - around, y - around, z - around)
    search_area_max = (x + around, y + around, z + around)
    comp = compFactory.CreateGame(levelId)
    nearEntityList = comp.GetEntitiesInSquareArea(None, search_area_min, search_area_max, dimensionId)
    nearestEntityId = None
    minDistance = float('inf')
    if not nearEntityList:return nearestEntityId, minDistance
    for id in nearEntityList:
        typeComp = compFactory.CreateEngineType(id)
        entityType = typeComp.GetEngineTypeStr()
        if excludeTypes != [] and entityType in excludeTypes:continue
        if includeTypes != [] and entityType not in includeTypes:continue
        posComp = compFactory.CreatePos(id)
        pos = posComp.GetPos()
        distance = math.sqrt((x - pos[0]) ** 2 + (y - pos[1]) ** 2 + (z - pos[2]) ** 2)
        if distance < minDistance:
            nearestEntityId = id
            minDistance = distance
    return nearestEntityId, minDistance