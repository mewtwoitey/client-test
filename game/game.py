from __future__ import annotations

from typing import TYPE_CHECKING

import ujson

from game.user import Player
from ui.custom.screens.popup import InformationPopup

if TYPE_CHECKING:
    from utils.networkmanager import NetworkManager


class Game:


    def __init__(self, network: NetworkManager, game_id: int) -> None:
        self.network = network
        self.board = Board(self)
        self.current_turn : int = 0
        self.game_id: int = game_id
        self.players: dict[str,Player] = {}

    def get_player(self: Game,player_id: int) -> Player | None:
        try:
            to_return = self.players[player_id]
        except IndexError:
            to_return = None
        return to_return

    def phase_change(self: Game, phase: str):
        game_screen = self.network.ui_app.get_screen("game")
        game_screen.query_one("#phase_text").phase = phase

    def next_turn(self: Game, player_nick: str):
        game_screen = self.network.ui_app.get_screen("game")
        game_screen.query_one("#phase_text").player_nick = player_nick

    def add_player(self: Game, info: dict) -> Player:
        player_object = Player(player_id=info["player_id"],
                                game_object=self,nick=info["nickname"])
        
        player_object.screen_pos = len(self.players) + 1
        self.players[info["player_id"]] = player_object
        return player_object

    def start_game(self: Game):
        self.network.ui_app.switch_screen("game")

    async def end_game(self: Game):
        await self.network.ui_app.push_screen("home")
        await self.network.ui_app.push_screen(InformationPopup(information="The game has ended!"))

class Board:
    def __init__(self: Board,game: Game,length: int=20) -> None:
        self._list = []
        self.game = game
        self.length = length
        for _ in range(length):
            self._list.append([])



    def json_convert(self: Board, json_str: str)-> str:
        converted = ujson.loads(json_str)
        for count, space in enumerate(converted):
            for item in space:
                match item.split("_"):
                    case ["player", player_id]:
                        player = self.game.get_player(player_id)
                        if not player:
                            continue

                        screen_pos = player.screen_pos
                        self._list[count].append(screen_pos)






