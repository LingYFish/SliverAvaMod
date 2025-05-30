# Embedded file name: mod/common/PlaceStructureModeType.py


class AnimationModeType:
    """
    @description 描述放置结构体时的动画模式
    @state 2.9.nodoc 新增 cxz nbt接口
    """
    NONE = 0
    LAYERS = 1
    BLOCKS = 2


class MirrorModeType:
    """
    @description 描述放置结构体时的镜像模式
    @state 2.9.nodoc 新增 cxz nbt接口
    """
    NONE = 0
    X = 1
    Y = 2
    XY = 3