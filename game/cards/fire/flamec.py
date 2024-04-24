from __future__ import annotations

from typing import TYPE_CHECKING

from game.cards.card import Card, Rarity, Theme

if TYPE_CHECKING:
    from game.user import Player

class Flame(Card):
    def __init__(self) -> None:
        self.card_id = 6
        self.theme = Theme.FIRE
        self.rarity = Rarity.COMMON
        self.name = "Flame"
        self.description = self.description_generator() + "Always decreases the max move and min move by 1."
        self.play_line= "{player.nick} got burnt and now moves slower"


    def check(self:Flame,player:Player)-> bool:
        return True




exports = Flame()