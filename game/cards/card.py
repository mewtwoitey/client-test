from __future__ import annotations

import importlib
import logging
import os
import random
from enum import Enum
from pathlib import Path
from typing import TYPE_CHECKING

from utils.useful import Result

if TYPE_CHECKING:
    from game.user import Me,Player
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


    def call_card(self:CardManager,card_id: int,player: Player) -> Result:


    def pull_card(self: CardManager,theme:Theme) -> Card:
        rare = random.choices(self.rarities,cum_weights=self.chances)[0]
        choose_from = self.card_list[theme][rare]
        return random.choice(choose_from)

    def setup_cards(self: CardManager) -> Result:
        #get all the folders that contain cards
        themes = [t.name.lower() for t in Theme]
        basedir = str(Path.cwd()) + "/src/cards/"

        #go over the folders
        for theme in themes:
            #add nessary lists to cache
            theme_enum = convert_enum_value(Theme,theme)
            self.card_list[theme_enum] = {key:[] for key in Rarity}

            try:
                for card_file in os.listdir(basedir+theme+"/"):

                    if card_file.endswith("c.py"):
                        card_class = importlib.import_module(f"src.cards.{theme}.{card_file[:-3]}").exports
                        rarer = card_class.rarity

                        self.card_list[theme_enum][rarer].append(card_class)
                        self.card_dict[card_class.card_id]=card_class

            except FileNotFoundError:
                logging.critical("A card file is missing, please ensure that all theme directories are there")
                critical()
                return Result(False)
        return Result(True,"")
