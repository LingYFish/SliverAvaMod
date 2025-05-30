import BlockType as modBlockType
import PlaceStructureModeType as modPlaceStructureModeType
import EntityType as modEntityType
import CommandBlockControlType as modCommandBlockControlType
import BrewingStandSlotType as modBrewingStandSlotType
import TradeLevelType as modTradeLevelType
import VariantType as modVariantType
import GamepadKeyType as modGamepadKeyType
import EntityColorType as modEntityColorType
import inventoryType as inventoryType
import openContainer as openContainer
import itemUseMethodEnum as itemUseMethodEnum
import EnchantType as modEnchantType
import renderControllerArrayType as renderControllerArrayType
import featureOptionID as featureOptionID
import EffectType as modEffectType
import itemAcquisitionMethod as itemAcquisitionMethod
import actorDamageCause as actorDamageCause
import KeyBoardType as modKeyBoardaType
import ItemType as modItemType
import StructureFeatureType as structureFeatureType
import SysSoundType as modSysSoundType
import BiomeType as modBiomeType
import EnchantSlotType as modEnchantSlotType
from hopperType import Hopper as hopperType
from blockPosType import BlockPos as BlockPos

class EntityConst:
    TYPE_LVOBJ = 'lvobj'
    TYPE_ENTITY = 'entity'
    TYPE_MONSTER = 'monster'
    TYPE_PLAYER = 'player'
    TYPE_BULLET = 'bullet'
    TYPE_SFX = 'sfx'
    TYPE_BUFF = 'buff'
    TYPE_PARTICLE = 'particle'
    TYPE_EFFECT = 'effect'
    TYPE_EFFECT_BIND = 'effect_bind'
    TYPE_FONT = 'font'
    TYPE_TEAM = 'team'
    TYPE_ITEM_ENTITY = 'item_entity'
    TYPE_NPC = 'npc'
    TYPE_MOD_ENTITY = 'mod_entity'

class Change:
    """
    @description 刷怪设置参数枚举，用于[SpawnCustomModule](../接口/世界/生物生成.md#spawncustommodule)
    """
    Add = 0
    Remove = 1

class ButtonState(object):
    """
    @description 按钮状态枚举值
    """
    Up = 0
    Down = 1

class ButtonEventType(object):
    """
    @description 按钮事件枚举值
    """
    Clicked = 0
    Pressed = 1
    Released = 2

class TouchEvent:
    """
    @description 触摸回调事件枚举值
    """
    TouchUp = 0
    TouchDown = 1
    TouchCancel = 3
    TouchMove = 4
    TouchMoveIn = 5
    TouchMoveOut = 6
    TouchScreenExit = 7

class HoverEvent:
    HoverMoveIn = 1
    HoverMoveOut = 0

class AttrType(object):
    """
    @description 描述属性枚举值，用于设置与获取实体的引擎属性的当前值与最大值
    @state 2.10 新增 xsf 新增对AttrType.FOLLOW_RANGE,AttrType.KNOCKBACK_RESISTANCE,AttrType.JUMP_STRENGTH,AttrType.ARMOR的支持
    @comment ABSORPTION: 伤害吸收效果的量化值，详见wiki文档：[伤害吸收](https://minecraft-zh.gamepedia.com/index.php?title=%E4%BC%A4%E5%AE%B3%E5%90%B8%E6%94%B6&variant=zh)
    /comment
    @comment 各类属性值一般通过entity的json配置，如minecraft:knockback_resistance : { "value" : 100, "max" : 100}
    /comment
    @comment 当json文件中未配置时，引擎会针对不同属性进行不同初始值、不同最大值的设置
    /comment
    """
    HEALTH = 0
    SPEED = 1
    DAMAGE = 2
    UNDERWATER_SPEED = 3
    HUNGER = 4
    SATURATION = 5
    ABSORPTION = 6
    LAVA_SPEED = 7
    LUCK = 8
    FOLLOW_RANGE = 9
    KNOCKBACK_RESISTANCE = 10
    JUMP_STRENGTH = 11
    ARMOR = 12

class ItemPosType(object):
    """
    @description 描述玩家物品位置
    """
    INVENTORY = 0
    OFFHAND = 1
    CARRIED = 2
    ARMOR = 3
    POS_SIZE = (36, 1, 1, 4)

class ArmorSlotType(object):
    """
    @description 描述盔甲槽位枚举值
    """
    DEFAULT = -1
    HEAD = 0
    BODY = 1
    LEG = 2
    FOOT = 3

class GameType(object):
    """
    @description 描述游戏类型的枚举值
    """
    Undefined = -1
    Survival = 0
    Creative = 1
    Adventure = 2
    Default = Survival

class WalkState(object):
    """
    @description 玩家行走模式
    @state 2.10 新增 xsf 玩家行走模式
    """
    Walk = 1
    Sneak = 2
    Sprint = 3

class GameDiffculty(object):
    """
    @description 描述游戏难度的枚举值
    """
    Peaceful = 0
    Easy = 1
    Normal = 2
    Hard = 3
    Count = 4
    Unknown = 5

class EntityTeleportCause(object):
    """
    @description 传送理由枚举
    """
    Unkown = '0'
    Projectile = '1'
    Command = '3'
    ChorusFruit = '2'
    Behavior = '4'
    Agent = 'agent'
    Client = 'client'
    GateWay = 'gateway'
    Script = 'script'

class PistonFacing(object):
    """
    @description 活塞朝向枚举
    @deprecated 1.21 请使用Facing枚举
    """
    Down = 0
    Up = 1
    North = 2
    South = 3
    West = 4
    East = 5

class Facing(object):
    """
    @description 朝向枚举值
    """
    Down = 0
    Up = 1
    North = 2
    South = 3
    West = 4
    East = 5

class UseAnimation(object):
    """
    @description 使用物品时动画枚举值
    @author gzhuabo
    @version 1.18
    """
    Undefined = 'none'
    Eat = 'eat'
    Drink = 'drink'
    Block = 'block'
    Bow = 'bow'
    Camera = 'camera'
    Spear = 'spear'
    Crossbow = 'crossbow'
    Spyglass = 'spyglass'

class ItemColor(object):
    """
    @description 物品的颜色枚举值
    @author xltang
    @version 1.19
    @state 1.19 新增 xltang 物品的颜色枚举值
    """
    Black = 0
    Red = 1
    Green = 2
    Brown = 3
    Blue = 4
    Purple = 5
    Cyan = 6
    Silver = 7
    Gray = 8
    Pink = 9
    Lime = 10
    Yellow = 11
    LightBlue = 12
    Magenta = 13
    Orange = 14
    White = 15

class UiBaseLayer(object):
    """
    @description 自定义UI界面的层次宏定义，用于在多个插件之间协调UI界面的遮挡关系
    @author xltang
    @version 1.21
    @state 1.21 新增 xltang 自定义UI界面的层次宏定义
    """
    Desk = 0
    DeskFloat = 15000
    PopUpLv1 = 25000
    PopUpLv2 = 45000
    PopUpModal = 60000
    PopUpFloat = 75000

class OptionId(object):
    """
    @description 可设置的枚举值
    @author sutao
    @version 1.21
    @state 2.9 调整 xsf 新增十字键操作、隐藏HUD、摄像机摇晃等8个OptionId
    """
    Undefined = ''
    AUTO_JUMP = 'AUTO_JUMP'
    HIDE_PAPERDOLL = 'HIDE_PAPERDOLL'
    HIDE_HAND = 'HIDE_HAND'
    SPLIT_CONTROLS = 'SPLIT_CONTROLS'
    VIEW_BOBBING = 'VIEW_BOBBING'
    INPUT_MODE = 'INPUT_MODE'
    TRADITION_CONTROLS = 'TRADITION_CONTROLS'
    HIDE_HUD = 'HIDE_HUD'
    CAMERA_SHAKE = 'CAMERA_SHAKE'
    TRANSPARENTLEAVES = 'TRANSPARENTLEAVES'
    FANCY_SKIES = 'FANCY_SKIES'
    SMOOTH_LIGHTING = 'SMOOTH_LIGHTING'
    GRAPHICS = 'GRAPHICS'
    RENDER_CLOUDS = 'RENDER_CLOUDS'

class SliderOptionId(object):
    """
    @description 滑动条设置选项枚举值
    @author ljj
    @version 2.11
    @state 2.11 新增 ljj 滑动条设置选项枚举值
    """
    Undefined = ''
    MOUSE_SENSITIVITY = 'MOUSE_SENSITIVITY'
    MOUSE_SPYGLASS_DAMPING = 'MOUSE_SPYGLASS_DAMPING'
    GAMEPAD_SENSITIVITY = 'GAMEPAD_SENSITIVITY'
    GAMEPAD_SPYGLASS_DAMPING = 'GAMEPAD_SPYGLASS_DAMPING'
    GAMEPAD_CURSOR_SENSITIVITY = 'GAMEPAD_CURSOR_SENSITIVITY'
    TOUCH_SENSITIVITY = 'TOUCH_SENSITIVITY'
    TOUCH_SPYGLASS_DAMPING = 'TOUCH_SPYGLASS_DAMPING'
    DPAD_SCALE = 'DPAD_SCALE'
    GAMMA = 'GAMMA'
    INTERFACE_OPACITY = 'INTERFACE_OPACITY'
    FIELD_OF_VIEW = 'FIELD_OF_VIEW'

class AttributeBuffType(object):
    """
    @description Buff状态类型枚举值
    """
    Hunger = 0
    Saturation = 1
    Regeneration = 2
    Heal = 3
    Harm = 4
    Magic = 5
    Wither = 6
    Poison = 7
    FatalPoison = 8
    SelfHeal = 9

class ColorCode(object):
    """
    @description [样式代码](https://minecraft-zh.gamepedia.com/%E6%A0%B7%E5%BC%8F%E4%BB%A3%E7%A0%81)
    @state 1.21 新增 czh 代替GenerateColor接口
    """
    BLACK = '§0'
    DARK_BLUE = '§1'
    DARK_GREEN = '§2'
    DARK_AQUA = '§3'
    DARK_RED = '§4'
    DARK_PURPLE = '§5'
    GOLD = '§6'
    GRAY = '§7'
    DARK_GRAY = '§8'
    BLUE = '§9'
    GREEN = '§a'
    AQUA = '§b'
    RED = '§c'
    LIGHT_PURPLE = '§d'
    YELLOW = '§e'
    WHITE = '§f'
    MINECOIN_GOLD = '§g'
    RAND = '§k'
    BOLD = '§l'
    ITALIC = '§o'
    RESET = '§r'

class VirtualWorldObjectType(object):
    """
    @description 虚拟世界对象类型
    @state 1.22 新增 sutao 虚拟世界对象类型
    """
    Model = 1
    Sfx = 2
    Textboard = 3
    Particle = 4

class TimeEaseType(object):
    """
    @description 时间变化类型
    @state 1.22 新增 sutao 时间变化类型
    """
    linear = 'linear'
    spring = 'spring'
    in_quad = 'in_quad'
    out_quad = 'out_quad'
    in_out_quad = 'in_out_quad'
    in_cubic = 'in_cubic'
    out_cubic = 'out_cubic'
    in_out_cubic = 'in_out_cubic'
    in_quart = 'in_quart'
    out_quart = 'out_quart'
    in_out_quart = 'in_out_quart'
    in_quint = 'in_quint'
    out_quint = 'out_quint'
    in_out_quint = 'in_out_quint'
    in_sine = 'in_sine'
    out_sine = 'out_sine'
    in_out_sine = 'in_out_sine'
    in_expo = 'in_expo'
    out_expo = 'out_expo'
    in_out_expo = 'in_out_expo'
    in_circ = 'in_circ'
    out_circ = 'out_circ'
    in_out_circ = 'in_out_circ'
    in_bounce = 'in_bounce'
    out_bounce = 'out_bounce'
    in_out_bounce = 'in_out_bounce'
    in_back = 'in_back'
    out_back = 'out_back'
    in_out_back = 'in_out_back'
    in_elastic = 'in_elastic'
    out_elastic = 'out_elastic'
    in_out_elastic = 'in_out_elastic'

class PlayerExhauseRatioType(object):
    """
    @description 饥饿度消耗倍率类型
    @state 1.24 新增 hdy 饥饿度消耗倍率类型
    """
    HEAL = 0
    JUMP = 1
    SPRINT_JUMP = 2
    MINE = 3
    ATTACK = 4
    GLOBAL = 9

class EntityComponentType(object):
    """
    @description 原版实体组件类型,具体描述可参考[微软原版实体组件描述](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/componentlist)
    @state 2.7 新增 cxz 原版实体组件类型
    """
    addrider = 0
    admire_item = 1
    ageable = 2
    anger_level = 3
    angry = 4
    annotation_break_door = 5
    annotation_open_door = 6
    area_attack = 7
    attack = 8
    attack_cooldown = 9
    attack_damage = 10
    balloonable = 11
    barter = 12
    block_climber = 13
    block_sensor = 14
    boostable = 15
    boss = 16
    break_blocks = 17
    breathable = 18
    breedable = 19
    bribeable = 20
    buoyant = 21
    burns_in_daylight = 22
    celebrate_hunt = 23
    combat_regeneration = 24
    conditional_bandwidth_optimization = 25
    custom_hit_test = 26
    damage_over_time = 27
    damage_sensor = 28
    despawn = 29
    drying_out_timer = 30
    dweller = 31
    economy_trade_table = 32
    entity_sensor = 33
    environment_sensor = 34
    equip_item = 35
    equippable = 36
    exhaustion_values = 37
    experience_reward = 38
    explode = 39
    flocking = 40
    follow_range = 41
    genetics = 42
    giveable = 43
    group_size = 44
    grows_crop = 45
    healable = 46
    health = 47
    heartbeat = 48
    hide = 49
    home = 50
    horse_jump_strength = 51
    hurt_on_condition = 52
    inside_block_notifier = 53
    insomnia = 54
    instant_despawn = 55
    interact = 56
    inventory = 57
    item_hopper = 58
    jump_dynamic = 59
    jump_static = 60
    knockback_resistance = 61
    lava_movement = 62
    leashable = 63
    lookat = 64
    managed_wandering_trader = 65
    mob_effect = 66
    movement_amphibious = 67
    movement_basic = 68
    movement_dolphin = 69
    movement_fly = 70
    movement_generic = 71
    movement_glide = 72
    movement_hover = 73
    movement_jump = 74
    movement_skip = 75
    movement_sway = 76
    nameable = 77
    navigation_climb = 78
    navigation_float = 79
    navigation_fly = 80
    navigation_generic = 81
    navigation_hover = 82
    navigation_swim = 83
    navigation_walk = 84
    out_of_control = 85
    peek = 86
    persistent = 87
    physics = 88
    player_exhaustion = 89
    player_experience = 90
    player_level = 91
    player_saturation = 92
    preferred_path = 93
    projectile = 94
    pushable = 95
    raid_trigger = 96
    rail_movement = 97
    rail_sensor = 98
    ravager_blocked = 99
    rideable = 100
    scaffolding_climber = 101
    scale_by_age = 102
    scheduler = 103
    shareables = 104
    shooter = 105
    sittable = 106
    spawn_entity = 107
    strength = 108
    tameable = 109
    tamemount = 110
    target_nearby_sensor = 111
    teleport = 112
    tick_world = 113
    timer = 114
    trade_table = 115
    trail = 116
    transformation = 117
    trust = 118
    trusting = 119
    underwater_movement = 120
    water_movement = 121

class SetBlockType(object):
    """
    @description 方块设置的类型
    @state 2.0 新增 guanmingyu 方块设置的类型
    """
    MAN_MADE = 0
    NATURE = 1
    API = 2

class AniCheatConsts(object):
    """
    @description 反作弊配置开关宏定义
    @state 1.25.0.release20211223 新增 xltang 反作弊配置开关宏定义
    """
    Open = 'on'
    Close = 'off'
    MoveOff = 'client-auth'
    MoveOn = 'server-auth'
    MoveRewind = 'server-auth-with-rewind'

class AniCheatBlockBreak(object):
    """
    @description 反作弊配置枚举值，破坏方块相关
    @state 1.25.0.release20211223 新增 xltang 反作弊配置枚举值，破坏方块相关
    """
    OpenSwitch = 'server-authoritative-block-breaking'
    PickRangeScalar = 'server-authoritative-block-breaking-pick-range-scalar'

class AniCheatMove(object):
    """
    @description 反作弊配置枚举值，移动检查开关
    @state 1.25.0.release20211223 新增 xltang 反作弊配置枚举值，移动检查开关
    """
    CheckStyle = 'server-authoritative-movement'
    CorrectSwitch = 'correct-player-movement'
    MinCorrectDelayTick = 'player-rewind-min-correction-delay-ticks'
    TickHistorySize = 'player-rewind-history-size-ticks'

class AniCheatMoveRewind(object):
    """
    @description 反作弊配置枚举值，位移倒带模拟相关参数
    @state 1.25.0.release20211223 新增 xltang 反作弊配置枚举值，位移倒带模拟相关参数
    """
    PositionThreshold = 'player-rewind-position-threshold'
    VelocityThreshold = 'player-rewind-velocity-threshold'
    PositionAcceptance = 'player-rewind-position-acceptance'
    PositionPersuasion = 'player-rewind-position-persuasion'

class AniCheatMoveUnSupportRewind(object):
    """
    @description 反作弊配置枚举值，不支持倒带模拟的特殊场景相关参数
    @state 1.25.0.release20211223 新增 xltang 反作弊配置枚举值，不支持倒带模拟的特殊场景相关参数
    """
    PositionThreshold = 'player-rewind-unsupported-position-threshold'
    VelocityThreshold = 'player-rewind-unsupported-velocity-threshold'
    PositionAcceptance = 'player-rewind-unsupported-position-acceptance'
    PositionPersuasion = 'player-rewind-unsupported-position-persuasion'

ExistAniCheatSettingTypes = {AniCheatBlockBreak.OpenSwitch: bool,
 AniCheatBlockBreak.PickRangeScalar: float,
 AniCheatMove.CheckStyle: str,
 AniCheatMove.CorrectSwitch: bool,
 AniCheatMove.MinCorrectDelayTick: int,
 AniCheatMove.TickHistorySize: int,
 AniCheatMoveRewind.PositionThreshold: float,
 AniCheatMoveRewind.VelocityThreshold: float,
 AniCheatMoveRewind.PositionAcceptance: float,
 AniCheatMoveRewind.PositionPersuasion: float,
 AniCheatMoveUnSupportRewind.PositionThreshold: float,
 AniCheatMoveUnSupportRewind.VelocityThreshold: float,
 AniCheatMoveUnSupportRewind.PositionAcceptance: float,
 AniCheatMoveUnSupportRewind.PositionPersuasion: float}

class TransferServerFailReason(object):
    """
    @apollo
    @description 转服判定失败的错误码
    @state 2.0.0.release20220315 新增 xltang 转服判定失败的错误码
    """
    TypeNotExist = 10
    VersionNotExist = 11
    ServerIsFull = 12
    VersionNotFix = 13
    TargetIsFull = 14
    TargetNotVaild = 15
    ApiInputFail = 16

ReasonCodeToChinese = {TransferServerFailReason.TypeNotExist: '目标类型的服务器不存在',
 TransferServerFailReason.VersionNotExist: '目标类型的服务器的版本与玩家客户端的版本不符',
 TransferServerFailReason.ServerIsFull: '目标类型的服务器均已经满员了',
 TransferServerFailReason.VersionNotFix: '目标ID的服务器的版本与玩家客户端版本不符',
 TransferServerFailReason.TargetIsFull: '目标ID的服务器已经满员了',
 TransferServerFailReason.TargetNotVaild: '目标ID的服务器不存在或者已经与控制服断开连接',
 TransferServerFailReason.ApiInputFail: '目标玩家不在线'}

class RenderLayer(object):
    """
    @description 方块渲染时的材质类型
    @state 2.1 新增 xusifan 方块渲染时的材质类型
    @comment 目前自定义方块只支持使用部分材质，具体见[自定义方块json组件][/mc-dev/mcguide/20-玩法开发/15-自定义游戏内容/2-自定义方块/1-JSON组件.md]
    由于联机大厅和apollo存在部分材质缺少定义，所以枚举值在联机大厅和apollo环境下，整体-2
    如：Blend = 4 变成 Blend = 2 ; Opaque = 5 变成 Opaque = 3，依此类推
    /comment
    """
    Blend = 4
    Opaque = 5
    Alpha = 7
    SeasonOpaque = 9
    SeasonAlpha = 10

class ItemCategory(object):
    """
    @description 物品所属创造栏类型
    @state 2.1 新增 xusifan 物品所属创造栏类型
    """
    Construction = 1
    Nature = 2
    Equipment = 3
    Items = 4
    Custom = 8

class BlockBreathability(object):
    """
    @description 方块的可呼吸性
    @state 2.1 新增 xusifan 方块的可呼吸性
    """
    Solid = 0
    Air = 1

class InputMode(object):
    """
    @description 控制器输入模式
    @state 2.4 新增 cxz 控制器输入模式
    """
    Undefined = -1
    Mouse = 0
    Touch = 1
    GamePad = 2

class RayFilterType(object):
    """
    @description 射线检测类型
    @state 2.8 新增 hdy 射线检测类型
    """
    OnlyEntities = 1
    OnlyBlocks = 2
    BothEntitiesAndBlock = OnlyEntities | OnlyBlocks

class OriginGUIName(object):
    """
    @description 获取原生UI名字
    @state 2.11 新增 xsf 获取原生UI名字
    """
    MoveUpBtn = 'binding.area.move_up'
    MoveDownBtn = 'binding.area.move_down'
    MoveLeftBtn = 'binding.area.move_left'
    MoveRightBtn = 'binding.area.move_right'
    SneakBtn = 'binding.area.sneak'
    JumpBtn = 'binding.area.jump'
    AscendBtn = 'binding.area.ascend'
    DescendBtn = 'binding.area.descend'
    WalkStateBtn = 'binding.area.walkstate'
    PauseBtn = 'binding.area.pause'
    ChatBtn = 'binding.area.chat'
    MenuBtn = 'binding.area.fold_menu'
    ReportBtn = 'binding.area.report_cheat'

class UICategory(object):
    """
    @description 原生UI类型名
    @state 2.4 新增 cxz 原生UI类型名
    """
    netease_chat_screen = 'netease_chat_screen'
    inventory_screen = 'inventory_screen'
    anvil_screen = 'anvil_screen'
    crafting_screen = 'crafting_screen'
    trade_screen = 'trade_screen'
    enchanting_screen = 'enchanting_screen'
    pause_screen = 'pause_screen'
    cartography_screen = 'cartography_screen'
    smithing_table_screen = 'smithing_table_screen'
    brewing_stand_screen = 'brewing_stand_screen'
    furnace_screen = 'furnace_screen'
    blast_furnace_screen = 'blast_furnace_screen'
    smoker_screen = 'smoker_screen'
    grindstone_screen = 'grindstone_screen'
    small_chest_screen = 'small_chest_screen'
    large_chest_screen = 'large_chest_screen'
    barrel_screen = 'barrel_screen'
    sign_screen = 'sign_screen'
    dropper_screen = 'dropper_screen'
    hopper_screen = 'hopper_screen'
    dispenser_screen = 'dispenser_screen'
    stonecutter_screen = 'stonecutter_screen'

class NativeScreenDataType:
    INVENTORY_CONTENT_PANEL = ['crafting.inventory_screen', '/variables_button_mappings_and_controls/safezone_screen_matrix/inner_matrix/safezone_screen_panel/root_screen_panel/content_stack_panel/player_inventory']
    POCKET_INVENTORY_CONTENT_PANEL = ['crafting_pocket.inventory_screen_pocket', '/variables_button_mappings_and_controls/safezone_screen_matrix/inner_matrix/safezone_screen_panel/root_screen_panel/root_panel/hotbar_and_panels/gamepad_helper_border/both_panels/right_panel/armor_tab_content']
    CRAFTING_CONTENT_PANEL = ['crafting.crafting_screen', '/variables_button_mappings_and_controls/safezone_screen_matrix/inner_matrix/safezone_screen_panel/root_screen_panel/content_stack_panel/player_inventory']
    POCKET_CRAFTING_CONTENT_PANEL = ['crafting_pocket.crafting_screen_pocket', '/variables_button_mappings_and_controls/safezone_screen_matrix/inner_matrix/safezone_screen_panel/root_screen_panel/root_panel/hotbar_and_panels/gamepad_helper_border/both_panels/right_panel/crafting_tab_content']
    SMALL_CHEST_PANEL = ['chest.small_chest_screen', '/variables_button_mappings_and_controls/safezone_screen_matrix/inner_matrix/safezone_screen_panel/root_screen_panel/root_panel']
    POCKET_SMALL_CHEST_PANEL = ['chest.small_chest_screen', '/variables_button_mappings_and_controls/safezone_screen_matrix/inner_matrix/safezone_screen_panel/root_screen_panel/bg']
    LARGE_CHEST_PANEL = ['chest.large_chest_screen', '/variables_button_mappings_and_controls/safezone_screen_matrix/inner_matrix/safezone_screen_panel/root_screen_panel/root_panel']
    POCKET_LARGE_CHEST_PANEL = ['chest.large_chest_screen', '/variables_button_mappings_and_controls/safezone_screen_matrix/inner_matrix/safezone_screen_panel/root_screen_panel/bg']
    ENDER_CHEST_PANEL = ['chest.ender_chest_screen', '/variables_button_mappings_and_controls/safezone_screen_matrix/inner_matrix/safezone_screen_panel/root_screen_panel/root_panel']
    POCKET_ENDER_CHEST_PANEL = ['chest.ender_chest_screen', '/variables_button_mappings_and_controls/safezone_screen_matrix/inner_matrix/safezone_screen_panel/root_screen_panel/bg']
    FURNACE_PANEL = ['furnace.furnace_screen', '/variables_button_mappings_and_controls/safezone_screen_matrix/inner_matrix/safezone_screen_panel/root_screen_panel/root_panel/common_panel']
    POCKET_FURNACE_PANEL = ['furnace.furnace_screen', '/variables_button_mappings_and_controls/safezone_screen_matrix/inner_matrix/safezone_screen_panel/root_screen_panel/bg']

enchantType2String = ['ArmorAll','ArmorFire','ArmorFall','ArmorExplosive','ArmorProjectile','ArmorThorns','WaterBreath','WaterSpeed','WaterAffinity','WeaponDamage','WeaponUndead','WeaponArthropod','WeaponKnockback','WeaponFire','WeaponLoot','MiningEfficiency','MiningSilkTouch','MiningDurability','MiningLoot','BowDamage','BowKnockback','BowFire','BowInfinity','FishingLoot','FishingLure','FrostWalker','Mending','CurseBinding','CurseVanishing','TridentImpaling','TridentRiptide','TridentLoyalty','TridentChanneling','CrossbowMultishot','CrossbowPiercing','CrossbowQuickCharge','NumEnchantments','InvalidEnchantment']

BlockType = modBlockType.BlockType
EntityType = modEntityType.EntityType
SysSoundType = modSysSoundType.SysSoundType
EffectType = modEffectType.EffectType
EnchantType = modEnchantType.EnchantType
BiomeType = modBiomeType.BiomeType
ActorDamageCause = actorDamageCause.ActorDamageCause
ItemType = modItemType.ItemType
KeyBoardType = modKeyBoardaType.KeyBoardType
ItemAcquisitionMethod = itemAcquisitionMethod.ItemAcquisitionMethod
ItemUseMethodEnum = itemUseMethodEnum.ItemUseMethodEnum
StructureFeatureType = structureFeatureType.StructureFeatureType
OpenContainerId = openContainer.OpenContainerId
PlayerUISlot = openContainer.PlayerUISlot
ContainerType = openContainer.ContainerType
EnchantSlotType = modEnchantSlotType.EnchantSlotType
InventoryType = inventoryType.InventoryType
RenderControllerArrayType = renderControllerArrayType.RenderControllerArrayType
FeatureOptionID = featureOptionID.FeatureOptionID
GamepadKeyType = modGamepadKeyType.GamepadKeyType
EntityColorType = modEntityColorType.EntityColorType
CatVariantType = modVariantType.CatVariantType
HorseType = modVariantType.HorseType
HorseSpotType = modVariantType.HorseSpotType
FoxType = modVariantType.FoxType
VillagerClothingType = modVariantType.VillagerClothingType
TradeLevelType = modTradeLevelType.TradeLevelType
BrewingStandSlotType = modBrewingStandSlotType.BrewingStandSlotType
CommandBlockType = modCommandBlockControlType.CommandBlockType
ConditionType = modCommandBlockControlType.ConditionType
RedstoneModeType = modCommandBlockControlType.RedstoneModeType
AnimationModeType = modPlaceStructureModeType.AnimationModeType
MirrorModeType = modPlaceStructureModeType.MirrorModeType