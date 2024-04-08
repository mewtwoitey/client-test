from pathlib import Path

from textual import on
from textual.app import ComposeResult
from textual.containers import Center, Container, Horizontal
from textual.screen import Screen
from textual.widgets import Button, Placeholder

from ui.custom.widgets.image import Image
from ui.custom.screens.popup import TextPopup


class Home(Screen):
    CSS_PATH = Path(str(Path.cwd()) + "/ui/css/home.tcss")
    BINDINGS = [  # noqa: RUF012
        ("escape, backspace","quit()","Exits the game"),
    ]



    def compose(self: "Home") -> ComposeResult:

        #header at the top specifcally for settings button
        with Container(id="settings_cont"):
            yield Button("",id="settings_button")

            
        with Container(id="image_cont"):
            yield Image(id="image",filename="logo.png")
        # used for allowing the the play button to be centred
        with Container(id="middle_cont"):
            with Center():
                yield Button("Play",id="play_button",variant="success")

        # to keep the three button level
        with Horizontal(id="bottom_cont"):
            yield Button("Pull Cards",id="pull_button",classes="small_button")
            yield Button("Quit",id="quit_button",classes="small_button",variant="error")
            yield Button("Instructions",id="instructions_button",classes="small_button")

    @on(Button.Pressed,"#quit_button")
    async def quit_button(self:"Home") -> None:
        await self.app.action_quit()


    #the next functions are just dedicated to navigation
    @on(Button.Pressed,"#settings_button")
    def settings_button(self:"Home") -> None:
        self.app.push_screen("settings")


    @on(Button.Pressed,"#pull_button")
    def pull_button(self:"Home") -> None:
        self.app.trigger_error("This is not implemented yet")


    @on(Button.Pressed, "#play_button")
    def player_button(self):


        def change_text(text: str):
            self.query_one("#play_button").text = text

        self.app.push_screen(
            TextPopup(text="test"),
            change_text,
        )