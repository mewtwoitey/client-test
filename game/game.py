from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from utils.networkmanager import NetworkManager
    from game.user import Player


class Game:
    current_turn : int
    game_id: int
    players: list[Player]

    def __init__(self, network: NetworkManager) -> None:
        self.network = network

    def get_player(self: Game,player_id:int) -> Player | None:
        try:
            to_return = self._players[player_id]
        except IndexError:
            to_return = None
        return to_return

    def phase_change(self: Game, phase: str):
        game_screen = self.network.ui_app.get_screen("game")
        game_screen.query_one("phase_text").phase = phase

    def next_turn(self: Game, player_nick: str):
        game_screen = self.network.ui_app.get_screen("game")
        game_screen.query_one("phase_text").player_nick = player_nick

    




