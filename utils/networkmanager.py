from __future__ import annotations

from typing import TYPE_CHECKING, Any

import ujson
from autobahn.asyncio.wamp import ApplicationRunner, ApplicationSession

if TYPE_CHECKING:
    from autobahn.wamp.types import ComponentConfig
    from textual.app import App

def generate_account() -> str:
    return ""

class NetworkManager(ApplicationSession):

    def __init__(self: NetworkManager, config: ComponentConfig | None = None) -> None:
        super().__init__(config)
        self.ui_app : App = config.extra["ui"]


    def process_broadcast(self: NetworkManager,message:str):
        from_json = ujson.loads(message)

        match from_json["event"]:
            #each event is specific so needs to be handled differently
            case "NEXT_TURN":
                self.ui.game.current_turn = from_json["player"]

                if
                


    async def call_function(self: NetworkManager, address:str, *args: list[Any]):
        res = await self.call(address, *args)
        


