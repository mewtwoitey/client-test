from pathlib import Path

from textual import on
from textual.app import ComposeResult
from textual.containers import Container
from textual.screen import Screen
from textual.widgets import Button,Label


from typing import Any

class PopupScreen(Screen):
    #class to handle css for making a popup widget
    CSS_PATH = [Path(str(Path.cwd()) + "/ui/css/popup.tcss")]  # noqa: RUF012


    def __init__(self: "PopupScreen", name: str | None = None, id: str | None = None, classes: str | None = None,default: Any) -> None:
        super().__init__(name, id, classes)


class ConfirmationPopup(PopupScreen):

    def __init__(self: "ConfirmationPopup", name: str | None = None, id: str | None = None, classes: str | None = None,default: Any) -> None:
        super().__init__(name, id, classes)

    def compose(self: "ConfirmationPopup") -> ComposeResult:
        with Container(id="main_content"):
            yield Label("Are you sure you want to do this?")
            yield Button("Yes", variant="success",id="yes_button")
            yield Button("No",variant="error",id="no_button")

    @on(Button.Pressed)
    def close_screen(self,details):
        match details.button.id:
            case "yes_button":
                self.dismiss(True)
            case "no_button":
                self.action_dismiss(False)

class ListPopup(PopupScreen)