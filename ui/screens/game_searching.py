from __future__ import annotations

from pathlib import Path

from textual import on
from textual.app import ComposeResult
from textual.containers import Container, Horizontal
from textual.widgets import Button, OptionList
from textual.widgets.option_list import Option
from textual.widget import Widget
from ui.custom.screens.subscreen import SubScreen
from textual.reactive import reactive

class GameInfo(Widget):
    player_names : reactive[list] = reactive([])
    game_name : reactive[str] = reactive("None")

    def render(self) -> str:
        return f"{self.game_name}\nPlayers:{len(self.player_names)}/4\nPlayer Names:{", ".join(self.player_names)}"

    def get_from_dict(self, game_dict: dict):
        self.player_names = game_dict["player_names"]
        self.game_name = game_dict["game_name"]



class SearchScreen(SubScreen):
    

    def __init__(self: SubScreen, name: str | None = None, id: str | None = None, classes: str | None = None) -> None:
        super().__init__(name, id, classes)
        self.game_cache = {}
        self.css_path = [*self.CSS_PATH, Path(str(Path.cwd()) + "/ui/css/search.tcss")]


    def compose(self) -> ComposeResult:
        yield from super().compose()
        with Container(id="content_cont"):
            
            with Container(id="left_side_container"):
                with Container(id="buttons_container"):
                    yield Button("Create Game", id="create_game_button")
                    yield Button("Join Highlighted", id="join_game_button")
                yield GameInfo()
            with Container(id = "right_side_content"):
                yield OptionList(id="games_list")
    

    async def populate(self):
        games = await self.app.network.get_games(self.app.me.token).value
        options = []
        for game in games:
            self.game_cache[game["game_id"]] = game
            options.append(Option(game["game_name"],id=game["game_id"]))
        options_list = self.query_one("#games_list")
        options_list.clear_options()
        options_list.add_options(*options)
    

    @on(OptionList.OptionHighlighted)
    def game_higlighted(self, details):
        game_id = details.option_id
        game_info = self.game_cache[game_id]

        self.query_one(GameInfo).get_from_dict(game_info)

    @on(OptionList.OptionSelected)
    async def join_game(self, details):
        game_id = details.option_id

        await self.app.network.join_game(self.app.me.token, game_id)
        #TODO ERRORS here




        