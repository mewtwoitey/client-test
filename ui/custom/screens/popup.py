from __future__ import annotations

from pathlib import Path
from typing import Any

from textual import on
from textual.app import ComposeResult
from textual.containers import Container
from textual.screen import Screen
from textual.widgets import Button, Label, OptionList
from textual.widgets.option_list import Option


class PopupScreen(Screen):
    #class to handle css for making a popup widget
    CSS_PATH = [Path(str(Path.cwd()) + "/ui/css/popup.tcss")]  # noqa: RUF012


    def __init__(self: "PopupScreen", name: str | None = None, id: str | None = None, classes: str | None = None) -> None:
        super().__init__(name, id, classes)


class ConfirmationPopup(PopupScreen):

    def __init__(self: "ConfirmationPopup", name: str | None = None, id: str | None = None, classes: str | None = None) -> None:
        super().__init__(name, id, classes)

    def compose(self: "ConfirmationPopup") -> ComposeResult:
        with Container(id="main_content"):
            yield Label("Are you sure you want to do this?")
            yield Button("Yes", variant="success",id="yes_button")
            yield Button("No",variant="error",id="no_button")

    @on(Button.Pressed)
    def close_screen(self,details) -> None:
        match details.button.id:
            case "yes_button":
                self.dismiss(True)
            case "no_button":
                self.dismiss(False)

class ListPopup(PopupScreen):
    def __init__(self: "ListPopup", name: str | None = None, id: str | None = None, classes: str | None = None,items: list[Option] | None = None) -> None:
        # items is a list of options that you want to display
        super().__init__(name, id, classes)
        self.items = items
    def compose(self: "ListPopup") -> ComposeResult:

        with Container(id="main_content"):
            yield OptionList(
                *self.items,
                id = "list_options",
            )



    @on(OptionList.OptionSelected)
    def chosen(self:"ListPopup", details) -> None:
        self.dismiss(details.option_id)


class ErrorPopup(PopupScreen):
    #screen to display errors

    def __init__(self: PopupScreen, name: str | None = None, id: str | None = None, classes: str | None = None, err_msg: str = "An error has occured") -> None:
        super().__init__(name, id, classes)
        self.err_msg = err_msg


    def compose(self) -> ComposeResult:
        with Container(id="main_content"):
            with Container(id="error_display"):
                yield Label(f"ERROR: {self.err_msg}")
                with Container(id="error_buttons"):
                    yield Button("Dismiss", id="dismiss_button")
                    yield Button("Leave Game", id="leave_button")


    @on(Button.Pressed)
    def button_pressed(self: ErrorPopup, )
