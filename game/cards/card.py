from __future__ import annotations

import importlib
import os
from enum import Enum
from pathlib import Path
from typing import TYPE_CHECKING

from utils.useful import Result

if TYPE_CHECKING:
    from game.user import Player
    from main import Main

Rarity = Enum("Rarity", ["COMMON", "MEDIUM", "HIGH"])
Theme = Enum("Theme", ["FIRE", "EARTH", "WIND"])
Icons = {
    Theme.FIRE : "󰈸",
    Theme.EARTH: "󰛍",
    Theme.WIND: "",
} # The icons used for the themes (requires a Nerd Font)


class Card:
    name: str
    card_id : int
    rarity: Rarity
    description: str
    theme: Theme
    play_line : str



    def check(self: Card, player: Player)-> bool:
        pass



    def description_generator(self: Card)->str:
        icon = self.rarity.value* Icons[self.theme]
        return f"{icon} {self.name} {icon}\n"



class CardManager:
    card_dict : dict[int,Card] # used for calling functions


    def __init__(self:CardManager,ui: Main) -> None:
        self.card_dict = {}
        self.ui = ui

    def get_card(self: CardManager, card_id: int) -> Result:
        if card_id not in self.card_dict:
            return Result(False,"Card id not found")
        
        return Result(True, value=self.card_dict[card_id])


    def call_card(self:CardManager,card_id: int,player: Player) -> Result:

        if card_id not in self.card_dict:
            return Result(False, "Card not found.")
        card_object = self.card_dict[card_id]

        can_run = card_object.check(player)

        if not can_run:
            return Result(False, "The requirements have not been met")

        return Result(True)




    def setup_cards(self: CardManager) -> Result:
        #get all the folders that contain cards
        themes = [t.name.lower() for t in Theme]
        basedir = str(Path.cwd()) + "/game/cards/"

        #go over the folders



        try:
            for theme in themes:
                for card_file in os.listdir(basedir+theme+"/"):
                    if card_file.endswith("c.py"):
                        card_class = importlib.import_module(f"game.cards.{theme}.{card_file[:-3]}").exports
                        self.card_dict[card_class.card_id]=card_class

        except FileNotFoundError:
            self.ui.trigger_error("Card files not found")
