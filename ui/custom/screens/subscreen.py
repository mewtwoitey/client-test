from pathlib import Path

from textual import on
from textual.app import ComposeResult
from textual.containers import Container
from textual.screen import Screen
from textual.widgets import Button

from utils.useful import get_base_path


class SubScreen(Screen):
    # a screen dedicated to being a sub menu like the settings or instructions
    CSS_PATH = [Path(get_base_path() + "/ui/css/sub.tcss")]  # noqa: RUF012
    BINDINGS = [  # noqa: RUF012
        ("escape, backspace ","pop_screen()","goes back a screen"),
    ]

    def __init__(self: "SubScreen", name: str | None = None, id: str | None = None, classes: str | None = None) -> None:
        super().__init__(name, id, classes)


    def compose(self: "SubScreen") -> ComposeResult:
        with Container(id="top_cont"):
            yield Button("Back",id="back_button")

    @on(Button.Pressed,"#back_button")
    def back_button(self:"SubScreen") -> None:
        #used to go back a screen, should hopefully not pop when not needed
        self.app.pop_screen()
