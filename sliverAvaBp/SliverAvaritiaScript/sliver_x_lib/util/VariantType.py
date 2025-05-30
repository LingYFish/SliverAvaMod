# Embedded file name: mod/common/VariantType.py


class CatVariantType:
    """
    @description 描述猫的变体种类
    @state 2.9.nodoc 新增 cxz nbt接口
    """
    White = 0
    Tuxedo = 1
    Red = 2
    Siamese = 3
    British = 4
    Calico = 5
    Persian = 6
    Ragdoll = 7
    Tabby = 8
    Black = 9
    Jellie = 10


class HorseType:
    """
    @description 描述马的变体颜色
    @state 2.9.nodoc 新增 cxz nbt接口
    """
    White = 0
    Creamy = 1
    Chestnut = 2
    Brown = 3
    Black = 4
    Gray = 5
    Darkbrown = 6


class HorseSpotType:
    """
    @description 描述马的斑点种类
    @state 2.9.nodoc 新增 cxz nbt接口
    """
    NoneSpot = 0
    WhiteStockings = 1
    WhiteField = 2
    WhiteDots = 3
    BlackDots = 4


class FoxType:
    """
    @description 描述狐狸的种类
    @state 2.9.nodoc 新增 cxz nbt接口
    """
    Red = 0
    Arctic = 1


class VillagerClothingType:
    """
    @description 描述v2版村民的衣服类型
    @state 2.9.nodoc 新增 cxz nbt接口
    """
    Normal = 0
    Desert = 1
    Jungle = 2
    Savanna = 3
    Snow = 4
    Swamp = 5
    Taiga = 6