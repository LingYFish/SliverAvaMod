_serverentitymodule = __builtins__['__import__']('_serverentitymodule')
_serverlevel = __builtins__['__import__']('_serverlevel')
from entity import entity
class level:
    
    @staticmethod
    def get_all_entities():
        #type: () -> list[entity]
        return [entity(entityId) for entityId in _serverlevel.get_level_actors().keys()]
    
    @staticmethod
    def get_all_player():
        #type: () -> list[entity]
        return [entity(entityId) for entityId in _serverlevel.get_player_list()]
    
    @staticmethod
    def remove_all():
        return _serverlevel.remove_all_entity_except_players()
    
    @staticmethod
    def run_command(command,show=True):
        return _serverentitymodule.minecraft_command(command,None,show)
    
    @staticmethod
    def send_msg(msg):
        return _serverlevel.notify_msg_nofilter(msg)
    
    @staticmethod
    def tipMsg(msg):
        return _serverlevel.tip_message(msg)