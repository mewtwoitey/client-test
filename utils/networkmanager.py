from __future__ import annotations

from typing import TYPE_CHECKING, Any

import ujson
from autobahn.asyncio.wamp import ApplicationRunner, ApplicationSession

from utils.useful import Result
from game.user import Me

if TYPE_CHECKING:
    from autobahn.wamp.types import ComponentConfig

    from main import Main

def generate_account() -> str:
    return ""

class NetworkManager(ApplicationSession):

    def __init__(self: NetworkManager, config: ComponentConfig | None = None) -> None:
        super().__init__(config)
        self.ui_app : Main = config.extra["ui"]
        self.ui_app.network = self
        self.me = Me(self.ui_app)

    async def onJoin(self: NetworkManager,_ : Any):
        await self.me.get_file()


    async def process_broadcast(self: NetworkManager,message:str):
        from_json = ujson.loads(message)
        game_id = self.ui_app.user.me.player.game_id

        match from_json["event"]:
            #each event is specific so needs to be handled differently
            case "NEXT_TURN":
                self.ui.game.current_turn = from_json["player"]

                #TODO(me): expand upon this

            case "PING":
                #used for checking if a client is still there
                await self.call_function("com.games.pong",game_id,self.ui_app.me.token)

            case "PLAYER_ELIMINATED":
                #needs to check if player is us and send to menu if so
                #else set nickname to eliminated
                pass




    async def call_function(self: NetworkManager, address:str, *args: list[Any]) -> Result:
        res = await self.call(address, *args)
        res_object = Result.from_json(res)
        return res_object

    async def pull_card(self: NetworkManager, theme:str):
        result = await self.call_function("com.not_games.pull_card",theme,self.ui_app.me.token)
        return result

    async def create_user(self: NetworkManager) -> Result:
        return await self.call_function("com.not_games.create_user")

    async def valid_token(self: NetworkManager,token:str) -> Result:
        return await self.call_function("com.not_games.valid_user",token)

    async def draw_card(self: NetworkManager, game_id: int, player_id: int) -> Result:
        return await self.call_function("com.games.draw_card",game_id,player_id)



    async def get_moves(self: NetworkManager, game_id:int, player_id: int) -> Result:
        return await self.call_function("com.games.get_moves",game_id,player_id)


    async def move(self: NetworkManager, game_id: int, player_id: int, spaces:int) -> Result:
        return await self.call_function("com.games.move_spaces", game_id, player_id, spaces)

    async def do_action(self: NetworkManager, game_id:int, player_id:int, activity_id: int) -> Result:
        return await self.call_function("com.games.do_action", game_id, player_id, activity_id)