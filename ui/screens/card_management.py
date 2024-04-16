from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any

from textual.containers import Container
from textual.reactive import Reactive
from textual.widget import Widget
from textual.widgets import Button, SelectionList
from textual.widgets.selection_list import Selection

from ui.custom.screens.popup import ConfirmationPopup, ListPopup, TextPopup
from ui.custom.screens.subscreen import SubScreen

from game.cards.card import Rarity

if TYPE_CHECKING:
    from main import Main
    from game.cards.card import Card

class CardInfo(Widget):
    description: Reactive[str] = Reactive("No Name")
    card_id: Reactive[int] = Reactive(0)


    def render(self:CardInfo) -> str:
        return f"Card Number: {self.card_id}\n{self.description}"

class OptionListDivider(Selection):
    def __init__(self, prompt: str, value: Any, initial_state: bool = False, id: str | None = None):
        super().__init__(prompt, value, initial_state, id, disabled=True)


class CardManagement(SubScreen):
    app : Main
    
    def __init__(self: SubScreen, name: str | None = None, id: str | None = None, classes: str | None = None) -> None:
        super().__init__(name, id, classes)

        self.css_path = [*self.CSS_PATH, Path(str(Path.cwd()) + "/ui/css/search.tcss")]
        self.current_deck = ""

    def compose(self: SubScreen) :
        yield from super().compose()

        with Container(id="content_cont"):
            with Container(id ="card_container"):
                yield CardInfo(id="card_information")
            with Container(id="card_selector"):
                yield Button("Select Deck", id="deck_selector")
                yield SelectionList(id="card_selector").

    async def refresh_card_list(self):
        
        possible_cards = self.app.network.me.cards
        options = []

        #get what cards are in the current deck
        if self.current_deck == "":
            in_deck = {} # track which cards are in the current deck
        else:
            in_deck = self.app.network.me.decks[self.current_deck]





        rarity_dict = {rarity: [] for rarity in Rarity} # puts all the player's cards into rarities

        #organize them by rarity
        for card_id,occurrences in possible_cards.items():
            card: Card = self.app.card_manager.get_card(card_id).value

            rarity_dict[card.rarity].extend([card for _ in range(occurrences)])

        #reverse the order so the highest cards get put first
        for value in range(1,len(rarity_dict),-1):

            current_rarity  = Rarity(value)
            options.append(OptionListDivider(current_rarity.name.lower().capitalize())) # class divider


            cards_in_rarity = rarity_dict[current_rarity].sort()
            for card_id in cards_in_rarity:

                card_object: Card = self.app.card_manager.get_card(card_id).value


                active_card = False
                if card_id in in_deck:
                    active_card = True
                    if in_deck[card_id] == 1:
                        del in_deck[card_id]
                    else:
                        in_deck[card_id] -= 1


                options.append(Selection(prompt=card_object.name,id=card_id,initial_state=active_card))

        card_selection: SelectionList = self.query_one("#card_selector")
        card_selection.clear_options()
        card_selection.add_options(options)







    async def create_new_deck(self):
        default = {}

        deck_name :str = await self.app.push_screen_wait(TextPopup(str="Please enter a deck name:"))

        confirmation: bool = await self.app.push_screen_wait(ConfirmationPopup())

        if not confirmation:
            return

        result = self.app.network.me.add_deck(deck_name,default)


        if not result.successful:
            self.app.trigger_error("That deck already exists")

        self.app.network.me.update_file()

    async def deck_selection(self):
        
        deck_names = []
        # get all the decks here

        deck_name = await self.app.push_screen_wait(ListPopup(items=deck_names))

        if deck_name == "creation_request":
            await self.create_new_deck()

        self.current_deck = deck_name



