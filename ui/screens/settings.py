from pathlib import Path


from textual import on
from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import Button
from textual.widgets.option_list import Option

from ui.custom.screens.popup import ConfirmationPopup, ListPopup
from ui.custom.screens.subscreen import SubScreen


class Settings(SubScreen):
    def __init__(self: "Settings", name: str | None = None, id: str | None = None, classes: str | None = None) -> None:
        super().__init__(name, id, classes)
        self.css_path = [*self.CSS_PATH, Path(str(Path.cwd()) + "/ui/css/settings.tcss")]

    def compose(self: "Settings") -> ComposeResult:
        yield from super().compose()  # gets all the elements from super
        with Container(id="content_cont"):
            yield Button("Theme Selection", id="theme_button")
            yield Button("Create an account", id= "create_account_button", disabled=(self.app.network.me.is_registered()))


    @on(Button.Pressed, "#theme_button")
    def test_button(self: "Settings") -> None:

        def select_option(select: str) -> None:
            match select:
                case "Dark":
                    self.app.dark = True
                case "Light":
                    self.app.dark = False

        self.app.push_screen(
            ListPopup(
                items=(
                    Option("Dark Theme", id="Dark"),
                    Option("Light Theme", id="Light"),
                ),
            ),
            select_option,
        )

    @on(Button.Pressed, "#create_account_button")
    def test_button2(self: "Settings") -> None:
        def select_option(select: bool) -> None:
            if select:
                self.run_worker(self.app.network.me.create_user())
                self.query_one("#create_account_button").disabled = True

        self.app.push_screen(
            ConfirmationPopup(),
            select_option,
        )
