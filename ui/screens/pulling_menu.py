from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any


from textual import on
from textual.containers import Container

from textual.events import Mount
from textual.widgets import Button, Placeholder, RichLog, TabbedContent, TabPane
from textual.widget import AwaitMount, Widget
from textual.reactive import Reactive

from game.cards.card import Theme

from ui.custom.screens.subscreen import SubScreen
from ui.custom.screens.popup import InformationPopup


if TYPE_CHECKING:
    from main import Main
    from game.cards.card import Card


class Money(Widget):
    app : Main
    money : Reactive[int] = Reactive(0)
    
    
    def render(self) -> str:
        return f"Money: {self.money}"
    
    async def on_mount(self, event: Mount) -> None:
        #get the money the players have
        money = await self.app.network.get_money(self.app.network.me.token)
        self.money = money.value

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
                yield Button("Management", id="management_button")
                
                
    @on(Button.Pressed, "#pull_button")
    async def pull_card_button(self, details: Button.Pressed):
        
        #check the user can by a card first
        if self.app.network.me.money < 200:
            self.app.trigger_error("Not enough funds to buy a card")
            return

        card_selector: TabbedContent = self.query_one("#theme_selector")
        theme:TabPane = card_selector.active_pane
        theme_name = theme.id.split("_")[0]



        card_res = await self.app.network.pull_card(theme_name)


        if not card_res.successful:
            self.app.trigger_error(card_res.error_msg)
            return

        card_id = card_res.value


        card_object_res = self.app.card_manager.get_card(card_id)

        if not card_object_res.successful:
            self.app.trigger_error(card_object_res.error_msg)

        card_object: Card = card_object_res.value


        card_text = f"You have obtained the card {card_object.name} with rarity {card_object.rarity.name}."

        await self.app.push_screen(
            InformationPopup(information=card_text)
        )
    
    @on(Button.Pressed, "#management_button")
    async def management(self):
        self.app.push_screen("card_management")
