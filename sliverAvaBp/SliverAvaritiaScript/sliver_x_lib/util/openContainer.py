# Embedded file name: mod/common/openContainer.py


class OpenContainerId(object):
    """
    @description 开放容器Id
    """
    AnvilInputContainer = 0
    AnvilMaterialContainer = 1
    SmithingTableInputContainer = 3
    SmithingTableMaterialContainer = 4
    EnchantingInputContainer = 22
    EnchantingMaterialContainer = 23
    LoomInputContainer = 41
    LoomDyeContainer = 42
    LoomMaterialContainer = 43
    GrindstoneInputContainer = 50
    GrindstoneAdditionalContainer = 51
    StonecutterInputContainer = 53
    CartographyInputContainer = 55
    CartographyAdditionalContainer = 56
    CursorContainer = 59
    CreatedOutputContainer = 60


class PlayerUISlot(object):
    """
    @description 开放容器对应的slot偏移
    """
    CursorSelected = 0
    AnvilInput = 1
    AnvilMaterial = 2
    StoneCutterInput = 3
    Trade2Ingredient1 = 4
    Trade2Ingredient2 = 5
    LoomInput = 9
    LoomDye = 10
    LoomMaterial = 11
    CartographyInput = 12
    CartographyAdditional = 13
    EnchantingInput = 14
    EnchantingMaterial = 15
    GrindstoneInput = 16
    GrindstoneAdditional = 17
    BeaconPayment = 27
    Crafting2x2Input1 = 28
    Crafting2x2Input2 = 29
    Crafting2x2Input3 = 30
    Crafting2x2Input4 = 31
    Crafting3x3Input1 = 32
    Crafting3x3Input2 = 33
    Crafting3x3Input3 = 34
    Crafting3x3Input4 = 35
    Crafting3x3Input5 = 36
    Crafting3x3Input6 = 37
    Crafting3x3Input7 = 38
    Crafting3x3Input8 = 39
    Crafting3x3Input9 = 40
    CreatedItemOutput = 50
    SmithingTableInput = 51
    SmithingTableMaterial = 52


class ContainerType(object):
    """
    @description 容器类型
    """
    NONE = -9
    INVENTORY = -1
    CONTAINER = 0
    WORKBENCH = 1
    FURNACE = 2
    ENCHANTMENT = 3
    BREWING_STAND = 4
    ANVIL = 5
    DISPENSER = 6
    DROPPER = 7
    HOPPER = 8
    CAULDRON = 9
    TRADE = 15
    JUKEBOX = 17
    ARMOR = 18
    HAND = 19
    LOOM = 24
    GRINDSTONE = 26
    BLAST_FURNACE = 27
    SMOKER = 28
    STONECUTTER = 29
    CARTOGRAPHY = 30
    SMITHING_TABLE = 33


OPEN_CONTAINER_OFFSET = {OpenContainerId.AnvilInputContainer: PlayerUISlot.AnvilInput,
 OpenContainerId.AnvilMaterialContainer: PlayerUISlot.AnvilMaterial,
 OpenContainerId.EnchantingInputContainer: PlayerUISlot.EnchantingInput,
 OpenContainerId.SmithingTableInputContainer: PlayerUISlot.SmithingTableInput,
 OpenContainerId.SmithingTableMaterialContainer: PlayerUISlot.SmithingTableMaterial,
 OpenContainerId.EnchantingMaterialContainer: PlayerUISlot.EnchantingMaterial,
 OpenContainerId.LoomInputContainer: PlayerUISlot.LoomInput,
 OpenContainerId.LoomDyeContainer: PlayerUISlot.LoomDye,
 OpenContainerId.LoomMaterialContainer: PlayerUISlot.LoomMaterial,
 OpenContainerId.GrindstoneInputContainer: PlayerUISlot.GrindstoneInput,
 OpenContainerId.GrindstoneAdditionalContainer: PlayerUISlot.GrindstoneAdditional,
 OpenContainerId.StonecutterInputContainer: PlayerUISlot.StoneCutterInput,
 OpenContainerId.CartographyInputContainer: PlayerUISlot.CartographyInput,
 OpenContainerId.CartographyAdditionalContainer: PlayerUISlot.CartographyAdditional,
 OpenContainerId.CursorContainer: PlayerUISlot.CursorSelected,
 OpenContainerId.CreatedOutputContainer: PlayerUISlot.CreatedItemOutput}

def GetContainerOffset(containerId):
    if containerId in OPEN_CONTAINER_OFFSET:
        return OPEN_CONTAINER_OFFSET[containerId]
    return 0