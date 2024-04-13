from __future__ import annotations

from pathlib import Path

from textual import on
from textual.app import ComposeResult
from textual.containers import Container, Horizontal
from textual.screen import Screen
from textual.widgets import Label, ProgressBar
from textual.widget import Widget
from textual.reactive import reactive

from game.user import Player



class PlayerName(Widget):
    """class used to make the player list on the board screen."""

    def __init__(self, *children: Widget, name: str | None = None, id: str | None = None, classes: str | None = None, disabled: bool = False, pos:int = 0) -> None:
        super().__init__(*children, name=name, id=id, classes=classes, disabled=disabled)
        self.player_num = pos

    nickname : reactive[str | None] = reactive("test name")

    def render(self: PlayerName) -> str:
        return f"Player {self.player_num!s} : {self.nickname}"

class GameName(Widget):

    game_name : reactive[str] = reactive("No Name")


    def render(self: GameName) -> str:
        return f"{self.game_name}"
class GameJoinScreen(Screen):
    CSS_PATH = Path(str(Path.cwd()) + "/ui/css/game_join.tcss")

    def __init__(self, name: str | None = None, id: str | None = None, classes: str | None = None) -> None:
        super().__init__(name, id, classes)
        self.current_pos = 1


    def compose(self) -> ComposeResult:
        yield GameName(id="game_name_label")
        with Container(id = "player_names_list"):
            yield PlayerName(id="player_name_1",pos=1)
            yield PlayerName(id="player_name_2",pos=2)
            yield PlayerName(id="player_name_3",pos=3)
            yield PlayerName(id="player_name_4",pos=4)
        yield ProgressBar(total=4,id="player_load_bar",show_eta=False)



    def player_add(self: GameJoinScreen, player_object : Player):
        self.query_one(f"#player_name_{player_object.screen_pos}").nickname = player_object.nick

        self.query_one("#player_load_bar").progress = player_object.screen_pos



    def set_game_name(self: GameJoinScreen, game_name :str):
        self.query_one("#game_name_label").game_name = game_name



