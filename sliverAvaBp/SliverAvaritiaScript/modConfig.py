modName = 'SliverAvaritiaScript'
modClientName = 'SliverAvaritiaClientSystem'
modServerName = 'SliverAvaritiaServerSystem'
modVersion = '1.0.0'
class SystemInit:
    ServerSystem = [
        (
            "SliverAvaritiaServerSystem",
            "SliverAvaritiaScript.server.SliverAvaritiaServerSystem.SliverAvaritiaServerSystem"
        ),
        (
            "collectServerSystem",
            "SliverAvaritiaScript.blocks.collectServerSystem.collectServerSystem"
        ),
        (
            "compressServerSystem",
            "SliverAvaritiaScript.blocks.compressServerSystem.compressServerSystem"
        ),
        (
            "extreme_crafting_tableServerSystem",
            "SliverAvaritiaScript.blocks.extreme_crafting_tableServerSystem.extreme_crafting_tableServerSystem"
        )
    ]
    ClientSystem = [
        (
            "SliverAvaritiaClientSystem",
            "SliverAvaritiaScript.client.SliverAvaritiaClientSystem.SliverAvaritiaClientSystem"   
        ),
        (
            "collectClientSystem",
            "SliverAvaritiaScript.blocks.collectClientSystem.collectClientSystem"
        ),
        (
            "compressClientSystem",
            "SliverAvaritiaScript.blocks.compressClientSystem.compressClientSystem"
        ),
        (
            "extreme_crafting_tableClientSystem",
            "SliverAvaritiaScript.blocks.extreme_crafting_tableClientSystem.extreme_crafting_tableClientSystem"
        )
    ]
    UiScreenNode = [
        (
            "collectUi",
            "SliverAvaritiaScript.ui.collect.collect",
            "AvaritiaUi.collectUi"
        ),
        (
            "compressUi",
            "SliverAvaritiaScript.ui.compress.compress",
            "AvaritiaUi.compressUi"
        ),
        (
            "extreme_crafting_tableUi",
            "SliverAvaritiaScript.ui.extreme_crafting_table.extreme_crafting_table",
            "AvaritiaUi.extreme_crafting_tableUi"
        )
    ]

class EntityType:
    GAPING_VOID = "sliver_x:gaping_void"
    HEAVEN_ARROW = "sliver_x:heaven_arrow"
    ENDEST_PEARL = "sliver_x:endest_pearl"
    SUB_HEAVEN_ARROW = "sliver_x:sub_heaven_arrow"

class ItemType:
    DIAMOND_SINGULARITY = "sliver_x:diamond_singularity"
    GOLD_SINGULARITY = "sliver_x:gold_singularity"
    NEUTRON_PILE = "sliver_x:neutron_pile"
    INFINITY_PICKAXE_HAMMER = "sliver_x:infinity_pickaxe.hammer"
    SILVER_SINGULARITY = "sliver_x:silver_singularity"
    INFINITY_SHOVEL_DESTROYER = "sliver_x:infinity_shovel.destroyer"
    INFINITY_INGOT = "sliver_x:infinity_ingot"
    DIAMOND_LATTICE = "sliver_x:diamond_lattice"
    INFINITY_BOW = "sliver_x:infinity_bow"
    INFINITY_LEGGINGS = "sliver_x:infinity_leggings"
    INFINITY_SHOVEL = "sliver_x:infinity_shovel"
    QUARTZ_SINGULARITY = "sliver_x:quartz_singularity"
    COSMIC_MEATBALLS = "sliver_x:cosmic_meatballs"
    PLATINUM_SINGULARITY = "sliver_x:platinum_singularity"
    REDSTONE_SINGULARITY = "sliver_x:redstone_singularity"
    INFINITY_BOOTS = "sliver_x:infinity_boots"
    INFINITY_CHESTPLATE = "sliver_x:infinity_chestplate"
    INFINITY_HELMET = "sliver_x:infinity_helmet"
    CRYSTAL_MATRIX_INGOT = "sliver_x:crystal_matrix_ingot"
    ENDEST_PEARL = "sliver_x:endest_pearl"
    INFINITY_CATALYST = "sliver_x:infinity_catalyst"
    MATTER_CLUSTER_FULL = "sliver_x:matter_cluster.full"
    MATTER_CLUSTER = "sliver_x:matter_cluster"
    NEUTRONIUM_INGOT = "sliver_x:neutronium_ingot"
    NEUTRON_NUGGET = "sliver_x:neutron_nugget"
    RECORD_FRAGMENT = "sliver_x:record_fragment"
    COPPER_SINGULARITY = "sliver_x:copper_singularity"
    EMERALD_SINGULARITY = "sliver_x:emerald_singularity"
    FLUXED_SINGULARITY = "sliver_x:fluxed_singularity"
    IRIDIUM_SINGULARITY = "sliver_x:iridium_singularity"
    IRON_SINGULARITY = "sliver_x:iron_singularity"
    LAPIS_SINGULARITY = "sliver_x:lapis_singularity"
    LEAD_SINGULARITY = "sliver_x:lead_singularity"
    NICKEL_SINGULARITY = "sliver_x:nickel_singularity"
    TIN_SINGULARITY = "sliver_x:tin_singularity"
    INFINITY_AXE = "sliver_x:infinity_axe"
    INFINITY_HOE = "sliver_x:infinity_hoe"
    INFINITY_PICKAXE = "sliver_x:infinity_pickaxe"
    INFINITY_SWORD = "sliver_x:infinity_sword"
    SKULLFIRE_SWORD = "sliver_x:skullfire_sword"
    ULTIMATE_STEW = "sliver_x:ultimate_stew"

class BlockType:
    collect = 'sliver_x:collect'
    compress = 'sliver_x:compress'
    extreme_crafting_table = 'sliver_x:extreme_crafting_table'
    neutronium_block = "sliver_x:neutronium_block"
    double_compressed_crafting_table = "sliver_x:double_compressed_crafting_table"
    crystal_matrix = "sliver_x:crystal_matrix"
    compressed_crafting_table = "sliver_x:compressed_crafting_table"
    infinity_block = "sliver_x:infinity_block"