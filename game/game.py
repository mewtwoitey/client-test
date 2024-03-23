from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from utils.networkmanager import NetworkManager


class Game:
    current_turn : int
    game_id: int

    def __init__(self, network: NetworkManager) -> None:
        self.network = network


    async def my_turn(self: Game, draw: bool):

        if candraw:
            await self.network.draw(game_id)



