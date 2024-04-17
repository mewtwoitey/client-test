from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any


from textual.containers import Container

from textual.widgets import Button, Placeholder, RichLog, TabbedContent, TabPane
from textual.widget import Widget
from textual.reactive import Reactive

from game.cards.card import Theme

from ui.custom.screens.subscreen import SubScreen


if TYPE_CHECKING:
    from main import Main
    from game.cards.card import Card


class Money(Widget):
    
    money : Reactive[int] = Reactive(0)
    
    
    def render(self) -> str:
        return f"Money: {self.money}"

class PullingMenu(SubScreen):
    app : Main
    
    def __init__(self: SubScreen, name: str | None = None, id: str | None = None, classes: str | None = None) -> None:
        super().__init__(name, id, classes)

        self.css_path = [*self.CSS_PATH, Path(str(Path.cwd()) + "/ui/css/card_pulling.tcss")]


    def compose(self: SubScreen) :
        yield from super().compose()
        with Container(id="content_cont"):
            with Container(id="selection_cont"):
                with TabbedContent(id="theme_selector"):
                    with TabPane("fire", id="fire_theme"):
                        yield Placeholder(id="card_banner_fire", classes="banner_image")
                    with TabPane("wind", id="wind_theme"):
                        yield Placeholder(id="card_banner_wind", classes="banner_image")
                    with TabPane("earth", id="earth_theme"):
                        yield Placeholder(id="card_banner_earth", classes="banner_image")
            with Container(id="money_cont"):
                yield Money()
                yield Button("Pull",id="pull_button")