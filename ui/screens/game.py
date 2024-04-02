from __future__ import annotations

from pathlib import Path

from textual import on
from textual.app import ComposeResult
from textual.containers import Center, Container, Horizontal
from textual.screen import Screen
from textual.widgets import Button, Placeholder, RichLog, TabbedContent, TabPane
from textual.widgets.option_list import Option

from ui.custom.screens.popup import ConfirmationPopup, ListPopup
from ui.custom.widgets.games import CardPanel, DecisionPanel, Phase, PlayerList, PlayerListStats


class GameScreen(Screen):
    CSS_PATH = Path(str(Path.cwd()) + "/ui/css/game.tcss")
    decision_function = None
    options = []

    def compose(self: GameScreen) -> ComposeResult:
        with TabbedContent():
            with TabPane("Board"):
                with Horizontal():
                    with Container(id="board_cont"):
                        yield Placeholder()


                    with Center():
                        with Container(id="board_side_cont"):

                            #for the player listing
                            yield PlayerList(id="player_list_1")
                            yield PlayerList(id="player_list_2")
                            yield PlayerList(id="player_list_3")
                            yield PlayerList(id="player_list_4")

                            #current phase
                            yield Phase(id="phase_text")


                            #surrendering button
                            yield Button("Surrender?", "error", id="surrender_button")


            with TabPane("Event Log"):
                with Container(id = "event_log_cont"):
                    yield RichLog(id = "event_log")

            with TabPane("Statistics"):
                    with Container(id = "stats_cont"):
                            yield PlayerListStats(id = "player_list_stats_1")
                            yield PlayerListStats(id = "player_list_stats_2")
                            yield PlayerListStats(id = "player_list_stats_3")
                            yield PlayerListStats(id = "player_list_stats_4")

            with TabPane("Decision"):
                with Container(classes = "vertical_cont"):
                    yield CardPanel()
                    yield DecisionPanel()

                with Container(classes="vertical_cont"):
                    yield Button("Play Card", id = "play_card_button")
                    yield Button("Take Decision", id = "decision_button")


    def log_event(self, text: str):
        log  = self.query_one(RichLog)

        log.write(text)

    def clear_decision(self: GameScreen):
        self.query_one("#decision_button").disabled = True
        self.query_one("#player_card_button").disabled = True


    def decision_moves(self: GameScreen, moves: list[int]):
        self.query_one("#decision_button").disabled = False
        self.query_one("#player_card_button").disabled = False
        self.options = [Option(str(num), id= str(num) ) for num in moves]
        self.decision_function = self.choose_button_function




    async def choose_button_function(self: GameScreen):

        async def select_option(num):
            self.app.decision = int(num)
            await self.app.decision_made.set()


        await self.app.push_screen(
            ListPopup(
                items=self.options,
            ),
            select_option,
        )

    def decision_activity(self:GameScreen, activities: dict[int,str]):
        self.options = [Option(name, id= str(id) ) for id, name in activities]
        self.decision_function = self.choose_button_function

    def decision_end(self:GameScreen):
        self.decision_function = self.end_button_function


    async def end_button_function(self: GameScreen):
        async def select_option(select: bool) -> None:
            if select:
                await self.app.decision_made.set()

        await self.app.push_screen(
            ConfirmationPopup()
        )

    @on(Button.Pressed, "#decision_button")
    async def decision_button_pressed(self:GameScreen):
        await self.decision_function()


    @on(Button.Pressed, "#player_card_button")
    async def card_button_pressed(self:GameScreen):
        if self.app.network.me.hand == -1:
            self.query_one("#player_card_button").disabled = True


