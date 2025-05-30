# Embedded file name: mod/common/CommandBlockControlType.py


class CommandBlockType:
    """
    @description 命令方块类型
    @state 2.9 新增 cxz nbt接口
    """
    PULSE = 0
    CYCLE = 1
    CHAIN = 2


class ConditionType:
    """
    @description 命令方块条件类型
    @state 2.9 新增 cxz nbt接口
    """
    UNCONDITIONAL = 0
    CONDITIONAL = 1


class RedstoneModeType:
    """
    @description 命令方块红石类型
    @state 2.9 新增 cxz nbt接口
    """
    KEEP_ON = 0
    REDSTONE_CONTROL = 1