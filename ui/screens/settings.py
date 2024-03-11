from pathlib import Path

from textual import on
from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import Button, Placeholder
from textual.widgets.option_list import Option

from ui.custom.screens.popup import ListPopup, ConfirmationPopup
from ui.custom.screens.subscreen import SubScreen


class Settings(SubScreen):
    def __init__(self: "Settings", name: str | None = None, id: str | None = None, classes: str | None = None) -> None:
        super().__init__(name, id, classes)
        self.CSS_PATH.append(Path(str(Path.cwd()) + "/ui/css/settings.tcss"))

    def compose(self: "Settings") -> ComposeResult:
        yield from super().compose() # gets all the elements from super
        with Container(id="content_cont"):
            yield Button("test 123",id="test_button")
            yield Button("test 321",id="test_button2")


    @on(Button.Pressed,"#test_button")
    def test_button(self:"Settings") -> None:

        def select_option(select: str) -> None:
            self.query_one("#test_button").label = select
        self.app.push_screen(
            ListPopup(
                items = (
                    Option("yes",id="yes"),
                    Option("no",id="no"),
                ),
            ),
            select_option,
        )


    @on(Button.Pressed,"#test_button2")
    def test_button2(self:"Settings") -> None:

        def select_option(select: bool) -> None:
            self.query_one("#test_button2").label = str(select)
        self.app.push_screen(
            ConfirmationPopup(),
            select_option,
        )


