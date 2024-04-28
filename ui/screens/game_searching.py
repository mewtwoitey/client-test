from __future__ import annotations

from pathlib import Path

from textual import on
from textual.app import ComposeResult
from textual.containers import Container, Horizontal
from textual.events import Mount
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Button, OptionList
from textual.widgets.option_list import Option

from ui.custom.screens.popup import TextPopup, ListPopup
from ui.custom.screens.subscreen import SubScreen
from utils.useful import Result, get_base_path


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
        self.css_path = [*self.CSS_PATH, Path(get_base_path() + "/ui/css/search.tcss")]


    def compose(self) -> ComposeResult:
        yield from super().compose()
        with Container(id="content_cont"):
            
            with Container(id="left_side_container"):
                with Container(id="buttons_container"):
                    yield Button("Create Game", id="create_game_button")
                    yield Button("Join Highlighted", id="join_game_button")
                    yield Button("Refresh", id="refresh_games")
                yield GameInfo()
            with Container(id = "right_side_content"):
                yield OptionList(id="games_list")
    

    async def populate(self):
        games = await self.app.network.get_games(self.app.network.me.token)
        games = games.value
        options = []
        
        for game in games:
            self.game_cache[game["game_id"]] = game
            options.append(Option(game["game_name"],id=game["game_id"]))

        options_list = self.query_one("#games_list")
        #redo list from scratch
        options_list.clear_options()
        options_list.add_options(options)
    




    @on(OptionList.OptionSelected)
    @on(OptionList.OptionHighlighted)
    def game_higlighted(self, details):
        game_id = details.option_id
        game_info = self.game_cache[game_id]

        self.query_one(GameInfo).get_from_dict(game_info)

    @on(Button.Pressed, "#join_game_button")
    async def run_join_game(self):
        self.run_worker(self.join_game())


    @on(Button.Pressed, "#refresh_games")
    async def run_refresh_game(self):
        await self.populate()

    async def join_game(self):
        game_list = self.query_one(OptionList)
        higlight_index = game_list.highlighted
        game_id = game_list.get_option_at_index(higlight_index)
        await self.app.network.me.get_cards()



        nickname = await self.app.push_screen_wait(TextPopup(text="Enter nickname", default="No Name"))

        deck_names = [
            Option(deck_name, id=deck_name)
            for deck_name, _ in
            self.app.network.me.decks.items()
        ]
        deck_names.append(Option("Exit", "make_sure_this_is_long"))
        got_deck = False

        while not got_deck:
            deck_name = await self.app.push_screen_wait(ListPopup(items = deck_names))
            if deck_name == "make_sure_this_is_long":
                return

            deck = self.app.network.me.decks[deck_name]
            if len(deck) == 0:
                self.app.trigger_error("That deck is empty")
                return
            valid_res: Result = self.app.network.me.validate_deck(deck)
            if not valid_res.successful:
                self.app.trigger_error(valid_res.error_msg)
                return
            got_deck = True


        await self.app.network.me.join_game(game_id.id, nickname, game_id.prompt,deck)


    @on(Button.Pressed,"#create_game_button")
    async def run_create_game(self,details):
        self.run_worker(self.create_game())


    async def create_game(self):
        game_name = await self.app.push_screen_wait(TextPopup(text="Enter game name", default="No Name"))

        nickname = await self.app.push_screen_wait(TextPopup(text="Enter nickname", default="No Name"))
        
        deck_names = [
            Option(deck_name, id=deck_name)
            for deck_name, _ in
            self.app.network.me.decks.items()
        ]
        deck_names.append(Option("Exit", "make_sure_this_is_long"))
        got_deck = False
        while not got_deck:
            deck_name = await self.app.push_screen_wait(ListPopup(items = deck_names))
            if deck_name == "make_sure_this_is_long":
                return

            deck = self.app.network.me.decks[deck_name]
            if len(deck) == 0:
                self.app.trigger_error("That deck is empty")
                return
            got_deck = True


        await self.app.network.me.create_game(game_name,nickname,deck)

    @on(Mount)
    async def mounted(self, details):
        await self.populate()




        