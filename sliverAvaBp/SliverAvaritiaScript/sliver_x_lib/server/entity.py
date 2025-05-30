_serverentitymodule = __builtins__['__import__']('_serverentitymodule')
_serverlevel = __builtins__['__import__']('_serverlevel')
_item = __builtins__['__import__']('_item')
class entity:
    def __init__(self,entityId):
        self.entityId = entityId
        self._tag = []

    @property
    def tag(self):
        """固定标签"""
        return self._tag

    @property
    def uid(self):
        """生物在指针里的id"""
        return self.entityId
    
    @property
    def type_id(self):
        """生物标识符"""
        return _serverentitymodule.get_entity_type_str(self.entityId)
    
    @property
    def alive(self):
        """实体是否存活"""
        return _serverlevel.is_entity_alive(self.entityId)
    
    @property
    def dimension_id(self):
        """实体所处维度"""
        return _serverentitymodule.get_entity_dimension_id(self.entityId)
    
    @property
    def health(self):
        """实体血量"""
        return _serverentitymodule.get_entity_health(self.entityId)
    
    @property
    def max_health(self):
        """实体最大血量"""
        return _serverentitymodule.get_entity_maxhealth(self.entityId)
    
    def set_max_health(self,setHealth=20):
        """设置实体最大血量"""
        return _serverentitymodule.set_entity_maxhealth(self.entityId,setHealth)
    
    def set_health(self,setHealth=20):
        """设置实体血量"""
        return _serverentitymodule.set_entity_health(self.entityId,setHealth)
    
    def run_command(self,command,show=True):
        """按照实体来运行指令"""
        return _serverentitymodule.minecraft_command(command,self.entityId,show)
    
    def set_name(self,name):
        """设置实体名称"""
        if self.type_id == 'minecraft:player':
            return False
        return _serverentitymodule.set_actor_name(self.entityId,name)
 
    def is_player(self):
        return self.type_id == 'minecraft:player'
    
    def add_tag(self,tag,locls=False):
        """给实体添加标签"""
        if locls and tag not in locls:
            self._tag.append(locls)
        _serverentitymodule.add_entity_tag(self.entityId,tag)

    def remove_entity_tag(self,tag,locls=False):
        """给实体添加标签"""
        if locls and tag in locls:
            self._tag.append(locls)
        _serverentitymodule.remove_entity_tag(self.entityId,tag)

    def tags(self,entityId,locls=False):
        """获取实体标签"""
        tags = _serverentitymodule.get_entity_tags(entityId)
        if locls:
            tags + self.tag
        return tags
    
    @property
    def get_name(self):
        """获取实体名称"""
        extract_value_type = lambda s: s.split(":", 1)[1] if len(s.split(":", 1)) == 2 and s.split(":", 1)[0] == "minecraft" else s
        lang = "entity.{}.name".format(extract_value_type(self.type_id))
        if self.type_id == 'minecraft:player':
            return _serverentitymodule.get_player_name(self.entityId)
        elif _serverentitymodule.get_actor_name(self.entityId) != None:
            return _serverentitymodule.get_actor_name(self.entityId)
        elif not self.type_id == 'minecraft:player' and not _serverlevel.get_language_value(lang) == lang:
            return _serverlevel.get_language_value(lang)
        return self.type_id
    
    @property
    def position(self):
        """实体位置"""
        return _serverentitymodule.get_entity_foot_pos(self.entityId)

    def set_position(self,pos):
        """设置实体位置"""
        return _serverentitymodule.set_entity_foot_position(self.entityId, pos)

    def set_dimension(self,dimension):
        """设置实体维度"""
        return _serverentitymodule.change_dimension(self.entityId, dimension)
    
    def set_carried_item(self,item_dict):
        """设置实体手持物品"""
        return _item.set_entity_carried_item(self.entityId, item_dict)

    @property
    def speed(self):
        """实体移动速度"""
        return _serverentitymodule.get_mob_speed(self.entityId)

    def set_speed(self,speed):
        """设置实体移动速度"""
        return _serverentitymodule.set_mob_speed(self.entityId)

    @property
    def target(self):
        """实体目标"""
        return _serverentitymodule.get_mob_target(self.entityId)

    def set_target(self,target):
        """设置实体目标"""
        return _serverentitymodule.set_mob_target(self.entityId, target)

    @property
    def loot(self):
        """实体掉落表"""
        return _serverentitymodule.get_actor_loot_table(self.entityId)

    def set_loot(self,loot):
        """设置实体掉落表"""
        return _serverentitymodule.set_actor_loot_table(self.entityId, loot)

    @property
    def motion(self):
        """实体运动向量"""
        return _serverentitymodule.get_actor_motion(self.entityId)

    def set_motion(self,motion):
        """设置实体运动向量"""
        return _serverentitymodule.set_actor_motion(self.entityId, motion)

    @property
    def ignore_hurt(self):
        """实体是否忽略伤害"""
        return _serverentitymodule.get_entity_ignore_hurt(self.entityId)

    def set_ignore_hurt(self,ignore):
        """设置实体是否忽略伤害"""
        return _serverentitymodule.set_entity_ignore_hurt(self.entityId, ignore)

    @property
    def last_hurt_by(self):
        """实体最后一次被谁伤害"""
        return _serverentitymodule.get_mob_last_hurt_by(self.entityId)

    def set_last_hurt_by(self,entity_id):
        """设置实体最后一次被谁伤害"""
        return _serverentitymodule.set_mob_last_hurt_by(self.entityId, entity_id)

    def hurt(self, attacker, damage, damage_cause='none', knockback=True, ignite=False, custom_data=None):
        """对实体造成伤害"""
        return _serverentitymodule.hurt(self.entityId, attacker, damage, damage_cause, knockback, ignite, custom_data)

    def hurt_to_death(self,attacker):
        """对实体造成致命伤害"""
        return lambda :_serverentitymodule.hurt_to_death(attacker, self.entityId)

    def spawn_loot(self,attacker, pos):
        """生成实体掉落"""
        return _serverentitymodule.spawn_entity_loot_table_with_actor(attacker, pos, self.entityId, attacker, attacker)
    
    @property
    def mark_remove(self):
        """移除实体"""
        _serverlevel.mark_remove_entity(self.entityId)

    @property
    def entity_die(self):
        """杀死实体"""
        return _serverentitymodule.entity_die(self.entityId)