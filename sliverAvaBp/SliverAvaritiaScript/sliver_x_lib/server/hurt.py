from core import api
from ..util.itemStack import ItemStack
from ..util import minecraftEnum

class Filter:
    """过滤器"""
    @staticmethod

    def mob(entityId):
        """
        | 过滤生物是否有血量组件

        ----------------

        - str entityId: 实体ID
        - bool return: 返回True时表示该实体为生物实体

        """
        return api.compFactory.CreateEntityComponent(entityId).HasComponent(minecraftEnum.EntityComponentType.health)


    @staticmethod
    def non_mob(entityId):
        """
        | 过滤非生物是否有血量组件

        ----------------

        - str entityId: 实体ID
        - bool return: 返回True时表示该实体为非生物实体

        """
        return not Filter.mob(entityId)

    @staticmethod
    def has_health(entityId):
        """
        | 过滤当前生命值大于0的实体。

        ----------------

        - str entityId: 实体ID
        - bool return: 生命值是否大于0

        """
        return api.compFactory.CreateAttr(entityId).GetAttrValue(minecraftEnum.AttrType.HEALTH) > 0