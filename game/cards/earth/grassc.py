from __future__ import annotations

from typing import TYPE_CHECKING

from game.cards.card import Card, Rarity, Theme

if TYPE_CHECKING:
    from game.user import Player

class Grass(Card):
    def __init__(self) -> None:
        self.card_id = 11
        self.theme = Theme.EARTH
        self.rarity = Rarity.COMMON
        self.name= "Grass"
        self.description = self.description_generator()+"If a player's luck is within 0.15 of the original value, reset it to 0.6"
        self.play_line = "{player.nick}'s luck has been set to 0.6."

    def check(self: Grass, player:Player)-> bool:
        #get the distance from the starting value
        distance = abs(0.5 - player.luck)
        if distance >= 0.15:
            return True
        return False



exports = Grass()