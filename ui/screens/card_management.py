from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any

from textual import on
from textual.containers import Container
from textual.reactive import Reactive
from textual.widget import Widget
from textual.widgets import Button, SelectionList
from textual.widgets.selection_list import Selection
from textual.widgets.option_list import Option
from textual.events import Mount

from ui.custom.screens.popup import ConfirmationPopup, ListPopup, TextPopup
from ui.custom.screens.subscreen import SubScreen

from game.cards.card import Rarity
from utils.useful import get_base_path

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

        self.css_path = [*self.CSS_PATH, Path(get_base_path() + "/ui/css/card_selection.tcss")]
        self.current_deck = ""

    def compose(self: SubScreen) :
        yield from super().compose()

        with Container(id="content_cont"):
            with Container(id ="card_container"):
                yield CardInfo(id="card_information")
            with Container(id="card_selector_cont"):
                with Container(id="button_container"):
                    yield Button("Select Deck", id="deck_selector")
                    yield Button("Save Deck", id="save_deck_button")
                yield SelectionList(id="card_selector")

    async def refresh_card_list(self):
        #get all cards here
        await self.app.network.me.get_cards()
        possible_cards = self.app.network.me.cards
        options = []
        card_num_arb = 0 # arbitrary number to make sure that entries don't merge

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
        for value in range(len(rarity_dict),0,-1):

            current_rarity  = Rarity(value)
            options.append(OptionListDivider(current_rarity.name.lower().capitalize(),0)) # class divider


            cards_in_rarity = rarity_dict[current_rarity]
            cards_in_rarity.sort(key=lambda x: x.name) #sort them by card name to make it organised
            for card_object in cards_in_rarity:
                card_id = card_object.card_id


                active_card = False
                if card_id in in_deck:
                    active_card = True
                    if in_deck[card_id] == 1:
                        del in_deck[card_id]
                    else:
                        in_deck[card_id] -= 1

                options.append(Selection(prompt=card_object.name,value=str(card_id)+" "*card_num_arb,initial_state=active_card))

                card_num_arb += 1

        card_selection: SelectionList = self.query_one("#card_selector")
        #re-do the menu from scratch
        card_selection.clear_options()
        card_selection.add_options(options)







    async def create_new_deck(self):
        default = {}

        deck_name :str = await self.app.push_screen_wait(TextPopup(text="Please enter a deck name:"))

        confirmation: bool = await self.app.push_screen_wait(ConfirmationPopup())

        if not confirmation:
            return

        result = self.app.network.me.add_deck(deck_name,default)

        if not result.successful:
            self.app.trigger_error("That deck already exists")
        self.current_deck = deck_name
        self.app.network.me.update_file()
        

    @on(Button.Pressed, "#deck_selector")
    async def deck_selection_button(self):
        #need to run in worker so this executes it
        self.run_worker(self.deck_selection())

    async def deck_selection(self):

        deck_names = []
        deck_names.append(Option("Create a deck", id="creation_request"))
        deck_names.extend([
            Option(deck_name, id=deck_name)
            for deck_name, _ in
            self.app.network.me.decks.items()
        ])

        deck_name = await self.app.push_screen_wait(ListPopup(items=deck_names))

        if deck_name == "creation_request":
            await self.create_new_deck()
            return

        self.current_deck = deck_name
        self.query_one("#deck_selector").label = deck_name
        await self.refresh_card_list()



    @on(Button.Pressed, "#save_deck_button")
    async def add_card(self, details):
        selected = self.query_one("#card_selector").selected
        if self.current_deck == "":
            return



        card_ids = [int(selection.rstrip()) for selection in selected]

        res = self.app.network.me.update_deck(self.current_deck, card_ids)
        
        if not res.successful:
            self.app.trigger_error(res.error_msg)
            return


        self.app.network.me.update_file()


    @on(SelectionList.SelectionHighlighted)
    async def refresh_card_info(self, details: SelectionList.SelectionHighlighted):
        card_id = details.selection.value

        card_object:Card = self.app.card_manager.get_card(int(card_id.rstrip(" "))).value
        card_widget = self.query_one(CardInfo)
        card_widget.card_id = card_id
        card_widget.description = card_object.description

    @on(Mount)
    async def mounted(self, details):
        await self.refresh_card_list()


