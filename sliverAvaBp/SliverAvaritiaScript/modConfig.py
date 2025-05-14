modName = 'SliverAvaritiaScript'
modClientName = 'SliverAvaritiaClientSystem'
modServerName = 'SliverAvaritiaServerSystem'
modVersion = '1.0.0'
class SystemInit:
    ServerSystem = [
        (
            "SliverAvaritiaServerSystem",
            "SliverAvaritiaScript.server.SliverAvaritiaServerSystem.SliverAvaritiaServerSystem"
        )
    ]
    ClientSystem = [
        (
            "SliverAvaritiaClientSystem",
            "SliverAvaritiaScript.client.SliverAvaritiaClientSystem.SliverAvaritiaClientSystem"   
        )
    ]
    UiScreenNode = [
    ]