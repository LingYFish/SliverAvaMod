# Embedded file name: mod/common/actorDamageCause.py


class ActorDamageCause(object):
    """
    @description 描述实体伤害来源枚举值，及实体被伤害的原因。
    @state 2.11 调整 cxz 新增Custom枚举，用于在Hurt接口标识为自定义伤害来源
    """
    NONE = 'none'
    Override = 'override'
    Contact = 'contact'
    EntityAttack = 'entity_attack'
    Projectile = 'projectile'
    Suffocation = 'suffocation'
    Fall = 'fall'
    Fire = 'fire'
    FireTick = 'fire_tick'
    Lava = 'lava'
    Drowning = 'drowning'
    BlockExplosion = 'block_explosion'
    EntityExplosion = 'entity_explosion'
    Void = 'void'
    Suicide = 'suicide'
    Magic = 'magic'
    Wither = 'wither'
    Starve = 'starve'
    Anvil = 'anvil'
    Thorns = 'thorns'
    FallingBlock = 'falling_block'
    Piston = 'piston'
    FlyIntoWall = 'fly_into_wall'
    Magma = 'magma'
    Fireworks = 'fireworks'
    Lightning = 'lightning'
    Freezing = 'freezing'
    Stalactite = 'stalactite'
    Stalagmite = 'stalagmite'
    RamAttack = 'ram_attack'
    Custom = 'custom'