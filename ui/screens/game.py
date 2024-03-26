from __future__ import annotations

from pathlib import Path

from textual import on
from textual.app import ComposeResult
from textual.containers import Center, Container, Horizontal
from textual.screen import Screen
from textual.widgets import Button, Placeholder, TabbedContent, TabPane, RichLog

from ui.custom.widgets.games import PlayerList, PlayerListStats, Phase, CardPanel, DecisionPanel


class GameScreen(Screen):
    CSS_PATH = Path(str(Path.cwd()) + "/ui/css/game.tcss")


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
