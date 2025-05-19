from SliverAvaritiaScript.modConfig import ItemType, BlockType
from SliverAvaritiaScript.api.lib.itemStack import ItemStack
class extremeCraftingTable(object):
    index = 0
    posToSlot = {}
    for y in xrange(9):
        for x in xrange(9):
            posToSlot[(x, y)] = index
            index += 1
    del x, y, index
    recipeItems = [
        {
            "newItemName": ItemType.INFINITY_CATALYST,
            "newAuxValue": 0,
            "count": 1
        },
        {
            "newItemName": ItemType.INFINITY_INGOT,
            "newAuxValue": 0,
            "count": 1
        },
        {
            "newItemName": ItemType.INFINITY_SWORD,
            "newAuxValue": 0,
            "count": 1,
            'userData': {
                'ItemCustomTips': {
                    '__type__': 8, 
                    '__value__': 
                    '%name%%category%%enchanting%\n\n§r§9+§cI§6n§ef§ai§bn§9i§dt§cy §r§9攻击伤害§r'
                }
            }
        },
        {
            "newItemName": ItemType.INFINITY_BOW,
            "newAuxValue": 0,
            "count": 1
        },
        {
            "newItemName": ItemType.INFINITY_PICKAXE,
            "newAuxValue": 0,
            "count": 1,
            'userData': {
                'ench': [
                    {
                        'lvl': {
                            '__type__': 2, 
                            '__value__': 10
                        }, 
                        'id': {
                            '__type__': 2, 
                            '__value__': 18
                        }
                    }
                ]
            }
        },
        {
            "newItemName": ItemType.INFINITY_SHOVEL,
            "newAuxValue": 0,
            "count": 1
        },
        {
            "newItemName": ItemType.INFINITY_HOE,
            "newAuxValue": 0,
            "count": 1
        },
        {
            "newItemName": ItemType.INFINITY_AXE,
            "newAuxValue": 0,
            "count": 1
        },
        {
            "newItemName": ItemType.INFINITY_HELMET,
            "newAuxValue": 0,
            "count": 1
        },
        {
            "newItemName": ItemType.INFINITY_CHESTPLATE,
            "newAuxValue": 0,
            "count": 1
        },
        {
            "newItemName": ItemType.INFINITY_LEGGINGS,
            "newAuxValue": 0,
            "count": 1
        },
        {
            "newItemName": ItemType.INFINITY_BOOTS,
            "newAuxValue": 0,
            "count": 1
        },
        {
            "newItemName": ItemType.SKULLFIRE_SWORD,
            "newAuxValue": 0,
            "count": 1
        },
        {
            "newItemName": ItemType.ENDEST_PEARL,
            "newAuxValue": 0,
            "count": 1
        },
        {
            "newItemName": ItemType.ULTIMATE_STEW,
            "newAuxValue": 0,
            "count": 1
        },
        {
            "newItemName": ItemType.COSMIC_MEATBALLS,
            "newAuxValue": 0,
            "count": 1
        },
        {
            "newItemName": BlockType.collect,
            "newAuxValue": 0,
            "count": 1
        },
        {
            "newItemName": BlockType.compress,
            "newAuxValue": 0,
            "count": 1
        }
    ]
    extremeRecipe = [
        {
            "identifier": "sliver_x:infinity_catalyst",
            "type": "shapeless",
            "ingredients": [
                {
                    "newItemName": ItemType.DIAMOND_LATTICE,
                    "newAuxValue": 0,
                    "count": 1
                },
                {
                    "newItemName": ItemType.CRYSTAL_MATRIX_INGOT,
                    "newAuxValue": 0,
                    "count": 1
                },
                {
                    "newItemName": ItemType.NEUTRON_PILE,
                    "newAuxValue": 0,
                    "count": 1
                },
                {
                    "newItemName": ItemType.NEUTRON_NUGGET,
                    "newAuxValue": 0,
                    "count": 1
                },
                {
                    "newItemName": ItemType.NEUTRONIUM_INGOT,
                    "newAuxValue": 0,
                    "count": 1
                },
                {
                    "newItemName": ItemType.ULTIMATE_STEW,
                    "newAuxValue": 0,
                    "count": 1
                },
                {
                    "newItemName": ItemType.COSMIC_MEATBALLS,
                    "newAuxValue": 0,
                    "count": 1
                },
                {
                    "newItemName": ItemType.ENDEST_PEARL,
                    "newAuxValue": 0,
                    "count": 1
                },
                {
                    "newItemName": ItemType.RECORD_FRAGMENT,
                    "newAuxValue": 0,
                    "count": 1
                },
                {
                    "newItemName": ItemType.IRON_SINGULARITY,
                    "newAuxValue": 0,
                    "count": 1
                },
                {
                    "newItemName": ItemType.GOLD_SINGULARITY,
                    "newAuxValue": 0,
                    "count": 1
                },
                {
                    "newItemName": ItemType.LAPIS_SINGULARITY,
                    "newAuxValue": 0,
                    "count": 1
                },
                {
                    "newItemName": ItemType.REDSTONE_SINGULARITY,
                    "newAuxValue": 0,
                    "count": 1
                },
                {
                    "newItemName": ItemType.QUARTZ_SINGULARITY,
                    "newAuxValue": 0,
                    "count": 1
                },
                {
                    "newItemName": ItemType.DIAMOND_SINGULARITY,
                    "newAuxValue": 0,
                    "count": 1
                },
                {
                    "newItemName": ItemType.EMERALD_SINGULARITY,
                    "newAuxValue": 0,
                    "count": 1
                }
            ],
            "result": {
                "newItemName": ItemType.INFINITY_CATALYST,
                "newAuxValue": 0,
                "count": 1
            }
        },
        {
            "identifier": "sliver_x:cosmic_meatballs",
            "type": "shapeless",
            "ingredients": [
                {
                    "newItemName": ItemType.NEUTRON_PILE,
                    "newAuxValue": 0,
                    "count": 1
                },
                {
                    "newItemName": 'minecraft:beef',
                    "newAuxValue": 0,
                    "count": 1
                },
                {
                    "newItemName": 'minecraft:beef',
                    "newAuxValue": 0,
                    "count": 1
                },
                {
                    "newItemName": 'minecraft:chicken',
                    "newAuxValue": 0,
                    "count": 1
                },
                {
                    "newItemName": 'minecraft:chicken',
                    "newAuxValue": 0,
                    "count": 1
                },
                {
                    "newItemName": 'minecraft:porkchop',
                    "newAuxValue": 0,
                    "count": 1
                },
                {
                    "newItemName": 'minecraft:porkchop',
                    "newAuxValue": 0,
                    "count": 1
                },
                {
                    "newItemName": 'minecraft:rabbit',
                    "newAuxValue": 0,
                    "count": 1
                },
                {
                    "newItemName": 'minecraft:rabbit',
                    "newAuxValue": 0,
                    "count": 1
                },
                {
                    "newItemName": 'minecraft:cod',
                    "newAuxValue": 0,
                    "count": 1
                },
                {
                    "newItemName": 'minecraft:cod',
                    "newAuxValue": 0,
                    "count": 1
                }
            ],
            "result": {
                "newItemName": ItemType.COSMIC_MEATBALLS,
                "newAuxValue": 0,
                "count": 1
            }
        },
        {
            "identifier": "sliver_x:ultimate_stew",
            "type": "shapeless",
            "ingredients": [
                {
                    "newItemName": ItemType.NEUTRON_PILE,
                    "newAuxValue": 0,
                    "count": 1
                },
                {
                    "newItemName": 'minecraft:wheat',
                    "newAuxValue": 0,
                    "count": 1
                },
                {
                    "newItemName": 'minecraft:wheat',
                    "newAuxValue": 0,
                    "count": 1
                },
                {
                    "newItemName": 'minecraft:carrot',
                    "newAuxValue": 0,
                    "count": 1
                },
                {
                    "newItemName": 'minecraft:carrot',
                    "newAuxValue": 0,
                    "count": 1
                },
                {
                    "newItemName": 'minecraft:potato',
                    "newAuxValue": 0,
                    "count": 1
                },
                {
                    "newItemName": 'minecraft:potato',
                    "newAuxValue": 0,
                    "count": 1
                },
                {
                    "newItemName": 'minecraft:cactus',
                    "newAuxValue": 0,
                    "count": 1
                },
                {
                    "newItemName": 'minecraft:cactus',
                    "newAuxValue": 0,
                    "count": 1
                },
                {
                    "newItemName": 'minecraft:red_mushroom',
                    "newAuxValue": 0,
                    "count": 1
                },
                {
                    "newItemName": 'minecraft:red_mushroom',
                    "newAuxValue": 0,
                    "count": 1
                },
                {
                    "newItemName": 'minecraft:brown_mushroom',
                    "newAuxValue": 0,
                    "count": 1
                },
                {
                    "newItemName": 'minecraft:brown_mushroom',
                    "newAuxValue": 0,
                    "count": 1
                }
            ],
            "result": {
                "newItemName": ItemType.ULTIMATE_STEW,
                "newAuxValue": 0,
                "count": 1
            }
        },
        {
            "identifier": "sliver_x:endest_pearl",
            "type": "shaped",
            'pattern': [
                '   EEE   ',
                ' EEPPPEE ',
                ' EPPPPPE ',
                'EPPPNPPPE',
                'EPPNSNPPE',
                'EPPPNPPPE',
                ' EPPPPPE ',
                ' EEPPPEE ',
                '   EEE   '
            ],
            'key': {
                'E': {
                    'newItemName': 'minecraft:end_stone',
                    "newAuxValue": 0,
                    "count": 1
                },
                'P': {
                    'newItemName': 'minecraft:ender_pearl',
                    "newAuxValue": 0,
                    "count": 1
                },
                'S': {
                    'newItemName': 'minecraft:nether_star',
                    "newAuxValue": 0,
                    "count": 1
                },
                'N': {
                    'newItemName': ItemType.NEUTRONIUM_INGOT,
                    "newAuxValue": 0,
                    "count": 1
                }
            },
            "result": {
                "newItemName": ItemType.ENDEST_PEARL,
                "newAuxValue": 0,
                "count": 1
            }
        },
        {
            "identifier": "sliver_x:infinity_ingot",
            "type": "shaped",
            'pattern': [
                'NNNNNNNNN',
                'NCXXCXXCN',
                'NXCCXCCXN',
                'NCXXCXXCN',
                'NNNNNNNNN'
            ],
            'key': {
                'C': {
                    'newItemName': ItemType.CRYSTAL_MATRIX_INGOT,
                    "newAuxValue": 0,
                    "count": 1
                },
                'N': {
                    'newItemName': ItemType.NEUTRONIUM_INGOT,
                    "newAuxValue": 0,
                    "count": 1
                },
                'X': {
                    'newItemName': ItemType.INFINITY_CATALYST,
                    "newAuxValue": 0,
                    "count": 1
                }
            },
            "result": {
                "newItemName": ItemType.INFINITY_INGOT,
                "newAuxValue": 0,
                "count": 1
            }
        },
        {
            "identifier": "sliver_x:compress",
            "type": "shaped",
            'pattern': [
                'IIIHHHIII',
                'X N   N X',
                'I N   N I',
                'X N   N X',
                'RNN O NNR',
                'X N   N X',
                'I N   N I',
                'X N   N X',
                'IIIXIXIII'
            ],
            'key': {
                'X': {
                    'newItemName': ItemType.CRYSTAL_MATRIX_INGOT,
                    "newAuxValue": 0,
                    "count": 1
                },
                'N': {
                    'newItemName': ItemType.NEUTRONIUM_INGOT,
                    "newAuxValue": 0,
                    "count": 1
                },
                'I': {
                    'newItemName':'minecraft:iron_block',
                    "newAuxValue": 0,
                    "count": 1
                },
                'H': {
                    'newItemName': 'minecraft:hopper',
                    "newAuxValue": 0,
                    "count": 1
                },
                'R': {
                    'newItemName': 'minecraft:redstone_block',
                    "newAuxValue": 0,
                    "count": 1
                },
                'O': {
                    'newItemName': BlockType.neutronium_block,
                    "newAuxValue": 0,
                    "count": 1
                }
            },
            "result": {
                "newItemName": BlockType.compress,
                "newAuxValue": 0,
                "count": 1
            }
        },
        {
            "identifier": "sliver_x:collect",
            "type": "shaped",
            'pattern': [
                'IIQQQQQII',
                'I QQQQQ I',
                'I  RRR  I',
                'X RRRRR X',
                'I RRXRR I',
                'X RRRRR X',
                'I  RRR  I',
                'I       I',
                'IIIXIXIII'
            ],
            'key': {
                'X': {
                    'newItemName': ItemType.CRYSTAL_MATRIX_INGOT,
                    "newAuxValue": 0,
                    "count": 1
                },
                'I': {
                    'newItemName': 'minecraft:iron_block',
                    "newAuxValue": 0,
                    "count": 1
                },
                'Q': {
                    'newItemName': 'minecraft:quartz_block',
                    "newAuxValue": 0,
                    "count": 1
                },
                'R': {
                    'newItemName': 'minecraft:redstone_block',
                    "newAuxValue": 0,
                    "count": 1
                }
            },
            "result": {
                "newItemName": BlockType.collect,
                "newAuxValue": 0,
                "count": 1
            }
        },
        {
            "identifier": "sliver_x:skullfire_sword",
            "type": "shaped",
            'pattern': [
                '       IX',
                '      IXI',
                '     IXI ',
                '    IXI  ',
                ' B IXI   ',
                '  BXI    ',
                '  WB     ',
                ' W  B    ',
                'D        '
            ],
            'key': {
                'I': {
                    'newItemName': ItemType.CRYSTAL_MATRIX_INGOT,
                    "newAuxValue": 0,
                    "count": 1
                },
                'X': {
                    'newItemName': 'minecraft:blaze_powder',
                    "newAuxValue": 0,
                    "count": 1
                },
                'B': {
                    'newItemName': 'minecraft:bone',
                    "newAuxValue": 0,
                    "count": 1
                },
                'D': {
                    'newItemName': 'minecraft:nether_star',
                    "newAuxValue": 0,
                    "count": 1
                },
                'W': {
                    'newItemName': 'minecraft:log',
                    "newAuxValue": 0,
                    "count": 1
                }
            },
            "result": {
                "newItemName": ItemType.SKULLFIRE_SWORD,
                "newAuxValue": 0,
                "count": 1
            }
        },
        {
            "identifier": "sliver_x:infinity_sword",
            "type": "shaped",
            'pattern': [
                '       II',
                '      III',
                '     III ',
                '    III  ',
                ' C III   ',
                '  CII    ',
                '  NC     ',
                ' N  C    ',
                'X        '
            ],
            'key': {
                'I': {
                    'newItemName': ItemType.INFINITY_INGOT,
                    "newAuxValue": 0,
                    "count": 1
                },
                'X': {
                    'newItemName': ItemType.INFINITY_CATALYST,
                    "newAuxValue": 0,
                    "count": 1
                },
                'C': {
                    'newItemName': ItemType.CRYSTAL_MATRIX_INGOT,
                    "newAuxValue": 0,
                    "count": 1
                },
                'N': {
                    'newItemName': ItemType.NEUTRONIUM_INGOT,
                    "newAuxValue": 0,
                    "count": 1
                },
            },
            "result": {
                "newItemName": ItemType.INFINITY_SWORD,
                "newAuxValue": 0,
                "count": 1,
                'userData': {
                    'ItemCustomTips': {
                        '__type__': 8, 
                        '__value__': 
                        '%name%%category%%enchanting%\n\n§r§9+§cI§6n§ef§ai§bn§9i§dt§cy §r§9攻击伤害§r'
                    }
                }
            }
        },
        {
            "identifier": "sliver_x:infinity_pickaxe",
            "type": "shaped",
            'pattern': [
                ' IIIIIII ',
                'IIIICIIII',
                'II  N  II',
                '    N    ',
                '    N    ',
                '    N    ',
                '    N    ',
                '    N    ',
                '    N    '
            ],
            'key': {
                'I': {
                    'newItemName': ItemType.INFINITY_INGOT,
                    "newAuxValue": 0,
                    "count": 1
                },
                'C': {
                    'newItemName': BlockType.crystal_matrix,
                    "newAuxValue": 0,
                    "count": 1
                },
                'N': {
                    'newItemName': ItemType.NEUTRONIUM_INGOT,
                    "newAuxValue": 0,
                    "count": 1
                }
            },
            "result": {
                "newItemName": ItemType.INFINITY_PICKAXE,
                "newAuxValue": 0,
                "count": 1,
                'userData': {
                    'ench': [
                        {
                            'lvl': {
                                '__type__': 2, 
                                '__value__': 10
                            }, 
                            'id': {
                                '__type__': 2, 
                                '__value__': 18
                            }
                        }
                    ]
                }
            }
        },
        {
            "identifier": "sliver_x:infinity_shovel",
            "type": "shaped",
            'pattern': [
                '      III',
                '     IIXI',
                '      III',
                '     N I ',
                '    N    ',
                '   N     ',
                '  N      ',
                ' N       ',
                'N        '
            ],
            'key': {
                'I': {
                    'newItemName': ItemType.INFINITY_INGOT,
                    "newAuxValue": 0,
                    "count": 1
                },
                'X': {
                    'newItemName': BlockType.infinity_block,
                    "newAuxValue": 0,
                    "count": 1
                },
                'N': {
                    'newItemName': ItemType.NEUTRONIUM_INGOT,
                    "newAuxValue": 0,
                    "count": 1
                }
            },
            "result": {
                "newItemName": ItemType.INFINITY_SHOVEL,
                "newAuxValue": 0,
                "count": 1
            }
        },
        {
            "identifier": "sliver_x:infinity_axe",
            "type": "shaped",
            'pattern': [
                ' I   ',
                'IIIII',
                ' IIII',
                '   IN',
                '    N',
                '    N',
                '    N',
                '    N',
                '    N'
            ],
            'key': {
                'I': {
                    'newItemName': ItemType.INFINITY_INGOT,
                    "newAuxValue": 0,
                    "count": 1
                },
                'N': {
                    'newItemName': ItemType.NEUTRONIUM_INGOT,
                    "newAuxValue": 0,
                    "count": 1
                }
            },
            "result": {
                "newItemName": ItemType.INFINITY_AXE,
                "newAuxValue": 0,
                "count": 1
            }
        },
        {
            "identifier": "sliver_x:infinity_hoe",
            "type": "shaped",
            'pattern': [
                '     N ',
                ' IIIIII',
                'IIIIIII',
                'I    II',
                '     N ',
                '     N ',
                '     N ',
                '     N ',
                '     N '
            ],
            'key': {
                'I': {
                    'newItemName': ItemType.INFINITY_INGOT,
                    "newAuxValue": 0,
                    "count": 1
                },
                'N': {
                    'newItemName': ItemType.NEUTRONIUM_INGOT,
                    "newAuxValue": 0,
                    "count": 1
                }
            },
            "result": {
                "newItemName": ItemType.INFINITY_HOE,
                "newAuxValue": 0,
                "count": 1
            }
        },
        {
            "identifier": "sliver_x:infinity_bow",
            "type": "shaped",
            'pattern': [
                '   II',
                '  I W',
                ' I  W',
                'I   W',
                'X   W',
                'I   W',
                ' I  W',
                '  I W',
                '   II'
            ],
            'key': {
                'I': {
                    'newItemName': ItemType.INFINITY_INGOT,
                    "newAuxValue": 0,
                    "count": 1
                },
                'X': {
                    'newItemName': ItemType.CRYSTAL_MATRIX_INGOT,
                    "newAuxValue": 0,
                    "count": 1
                },
                'W': {
                    'newItemName': 'minecraft:wool',
                    "newAuxValue": 0,
                    "count": 1
                }
            },
            "result": {
                "newItemName": ItemType.INFINITY_BOW,
                "newAuxValue": 0,
                "count": 1
            }
        },
        {
            "identifier": "sliver_x:infinity_helmet",
            "type": "shaped",
            'pattern': [
                ' NNNNN ',
                'NIIIIIN',
                'N XIX N',
                'NIIIIIN',
                'NIIIIIN',
                'NI I IN'
            ],
            'key': {
                'N': {
                    'newItemName': ItemType.NEUTRONIUM_INGOT,
                    "newAuxValue": 0,
                    "count": 1
                },
                'X': {
                    'newItemName': ItemType.INFINITY_CATALYST,
                    "newAuxValue": 0,
                    "count": 1
                },
                'I': {
                    'newItemName': ItemType.INFINITY_INGOT,
                    "newAuxValue": 0,
                    "count": 1
                }
            },
            "result": {
                "newItemName": ItemType.INFINITY_HELMET,
                "newAuxValue": 0,
                "count": 1
            }
        },
        {
            "identifier": "sliver_x:infinity_chestplate",
            "type": "shaped",
            'pattern': [
                ' NN   NN ',
                'NNN   NNN',
                'NNN   NNN',
                ' NIIIIIN ',
                ' NIIXIIN ',
                ' NIIIIIN ',
                ' NIIIIIN ',
                ' NIIIIIN ',
                '  NNNNN  '
            ],
            'key': {
                'N': {
                    'newItemName': ItemType.NEUTRONIUM_INGOT,
                    "newAuxValue": 0,
                    "count": 1
                },
                'X': {
                    'newItemName': BlockType.crystal_matrix,
                    "newAuxValue": 0,
                    "count": 1
                },
                'I': {
                    'newItemName': ItemType.INFINITY_INGOT,
                    "newAuxValue": 0,
                    "count": 1
                }
            },
            "result": {
                "newItemName": ItemType.INFINITY_CHESTPLATE,
                "newAuxValue": 0,
                "count": 1
            }
        },
        {
            "identifier": "sliver_x:infinity_leggings",
            "type": "shaped",
            'pattern': [
                'NNNNNNNNN',
                'NIIIXIIIN',
                'NINNXNNIN',
                'NIN   NIN',
                'NCN   NCN',
                'NIN   NIN',
                'NIN   NIN',
                'NIN   NIN',
                'NNN   NNN'
            ],
            'key': {
                'N': {
                    'newItemName': ItemType.NEUTRONIUM_INGOT,
                    "newAuxValue": 0,
                    "count": 1
                },
                'X': {
                    'newItemName': ItemType.INFINITY_CATALYST,
                    "newAuxValue": 0,
                    "count": 1
                },
                'I': {
                    'newItemName': ItemType.INFINITY_INGOT,
                    "newAuxValue": 0,
                    "count": 1
                },
                'C': {
                    'newItemName': BlockType.crystal_matrix,
                    "newAuxValue": 0,
                    "count": 1
                }
            },
            "result": {
                "newItemName": ItemType.INFINITY_LEGGINGS,
                "newAuxValue": 0,
                "count": 1
            }
        },
        {
            "identifier": "sliver_x:infinity_boots",
            "type": "shaped",
            'pattern': [
                ' NNN NNN ',
                ' NIN NIN ',
                ' NIN NIN ',
                'NNIN NINN',
                'NIIN NIIN',
                'NNNN NNNN'
            ],
            'key': {
                'N': {
                    'newItemName': ItemType.NEUTRONIUM_INGOT,
                    "newAuxValue": 0,
                    "count": 1
                },
                'I': {
                    'newItemName': ItemType.INFINITY_INGOT,
                    "newAuxValue": 0,
                    "count": 1
                }
            },
            "result": {
                "newItemName": ItemType.INFINITY_BOOTS,
                "newAuxValue": 0,
                "count": 1
            }
        }
    ]
    @staticmethod
    def getRecipeAllItems(recipe):
        if recipe["type"] == "shapeless":
            return map(lambda i: ItemStack(**i), recipe["ingredients"])
        if recipe["type"] == "shaped":
            allItem = []
            shape = extremeCraftingTable.getShaped(recipe)[0]
            for line in shape:
                for item in line:
                    if item:
                        allItem.append(ItemStack(**item))
            return allItem

    @staticmethod
    def getExtremeRecipe(container):
        for recipe in extremeCraftingTable.extremeRecipe:
            ret = extremeCraftingTable.handleRecipe(recipe, container)
            if ret:
                return recipe
    
    @staticmethod
    def getExtremeRecipeByName(name):
        for recipe in extremeCraftingTable.extremeRecipe:
            if recipe["identifier"] == name:
                return recipe
    
    @staticmethod
    def handleRecipe(recipe, container):
        if recipe["type"] == "shapeless":
            return extremeCraftingTable.canShapelessRecipe(recipe, container)
        if recipe["type"] == "shaped":
            return extremeCraftingTable.canShapedRecipe(recipe, container)
        return False
    
    @staticmethod
    def getShaped(recipe):
        pattern = recipe["pattern"]
        key = recipe["key"]
        shape = []
        width = 0
        for i in pattern:
            line = []
            for s in i:
                line.append(key.get(s))
            width = max(len(line), width)
            shape.append(line)
        hight = len(shape)
        return shape, width, hight
    
    @staticmethod
    def canShapedRecipe(recipe, container):
        shape, width, hight = extremeCraftingTable.getShaped(recipe)
        for x in xrange(9 - (width - 1)):
            for y in xrange(9 - (hight - 1)):
                canRecipe = True
                pos = (x, y)
                allPos = set()
                for i in xrange(width):
                    for j in xrange(hight):
                        posX, posY = pos[0] + i, pos[1] + j
                        allPos.add((posX, posY))
                        item = container[extremeCraftingTable.posToSlot.get((posX, posY))]
                        item2 = shape[j][i]
                        item2 = ItemStack(**item2) if item2 else ItemStack()
                        if (not (item == item2 and item.count >= item2.count)) and (not (item.isEmpty() and item2.isEmpty())):
                            canRecipe = False
                leftPos = set(extremeCraftingTable.posToSlot.keys()) - allPos
                if all([container[extremeCraftingTable.posToSlot.get(i)].isEmpty() for i in leftPos]) and canRecipe:
                    return True
        return False
    
    @staticmethod
    def canShapelessRecipe(recipe, container):
        allItems = container.values()
        ingredients = map(lambda i: ItemStack(**i), recipe["ingredients"])
        ingredients2 = len(ingredients)
        for i in xrange(len(ingredients)):
            item = ingredients[i]
            for i2 in xrange(len(allItems)):
                item2 = allItems[i2]
                if item == item2 and item2.count >= item.count:
                    ingredients2 -= 1
                    break
        return (ingredients2 == 0 and len([i for i in allItems if not i.isEmpty()]) == len(recipe["ingredients"]))