from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main import Main
    from game.game import Game


class Player:
    gems: list[str]
    player_id: int
    game: Game

    def __init__(self: Player, player_id: int, game_object: Game,nick:str) -> None:
        self.nick = nick
        self.draw_chance = 0.33
        self.move_min = 2
        self.move_max = 8
        self.luck = 0.5
        self.priority = 100
        self.cash = 0
        self.position = 0
        self.screen_pos = -1
        self.gems: list[int] = []
        self.player_id: int = player_id
        self.game: Game = game_object


    def set_nick(self: Player, nick: str) -> None:
        self.nick = nick
        game_screen = self.game.network.ui_app.get_screen("game")
        game_screen.query_one(f"#player_list_stats_{self.screen_pos}").nickname = nick
        game_screen.query_one(f"#player_list_{self.screen_pos}").nickname = nick

    def set_position(self: Player, position: int) -> None:
        self.position = position
        game_screen = self.game.network.ui_app.get_screen("game")
        game_screen.query_one(f"#player_list_stats_{self.screen_pos}").pos = position
        game_screen.query_one(f"#player_list_{self.screen_pos}").pos = position

    def set_screen_pos(self: Player, screen_position: int) -> None:
        self.screen_pos = screen_position
        game_screen = self.game.network.ui_app.get_screen("game")
        game_screen.query_one(f"#player_list_stats_{self.screen_pos}").player_num = screen_position
        game_screen.query_one(f"#player_list_{self.screen_pos}").player_num = screen_position

    def set_draw(self: Player, draw: float) -> None:
        self.draw_chance = draw
        game_screen = self.game.network.ui_app.get_screen("game")
        game_screen.query_one(f"#player_list_stats_{self.screen_pos}").draw_chance = draw

    def set_move_min(self: Player, move_min: int) -> None:
        self.move_min = move_min
        game_screen = self.game.network.ui_app.get_screen("game")
        game_screen.query_one(f"#player_list_stats_{self.screen_pos}").move_min = move_min

    def set_move_max(self: Player, move_max: int) -> None:
        self.move_max = move_max
        game_screen = self.game.network.ui_app.get_screen("game")
        game_screen.query_one(f"#player_list_stats_{self.screen_pos}").move_max = move_max

    def set_money(self: Player, money: float) -> None:
        self.money = money
        game_screen = self.game.network.ui_app.get_screen("game")
        game_screen.query_one(f"#player_list_stats_{self.screen_pos}").money = money

    def set_luck(self: Player, luck: float) -> None:
        self.luck = luck
        game_screen = self.game.network.ui_app.get_screen("game")
        game_screen.query_one(f"#player_list_stats_{self.screen_pos}").luck = luck

    def set_priority(self: Player, priority: int) -> None:
        self.priority = priority
        game_screen = self.game.network.ui_app.get_screen("game")
        game_screen.query_one(f"#player_list_stats_{self.screen_pos}").priority = priority

    def give_gem(self: Player, gem_id:int) -> None:
        self.gems.append(gem_id)
        game_screen = self.game.network.ui_app.get_screen("game")
        game_screen.query_one(f"#player_list_stats_{self.screen_pos}").gems = len(self.gems)



