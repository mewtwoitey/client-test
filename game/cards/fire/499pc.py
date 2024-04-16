from __future__ import annotations

from typing import TYPE_CHECKING

from game.cards.card import Card, Rarity, Theme

if TYPE_CHECKING:
    from game.user import Player

class H499P(Card):
    def __init__(self) -> None:
        self.name = "499P"
        self.card_id = 1
        self.theme = Theme.FIRE
        self.rarity = Rarity.HIGH
        self.description = self.description_generator() + "When this card is played the player will gain +3 to their max and min speed. Can only be played when you have no gems."
        self.play_line = "The 499p is added and now {player.nick} is faster!"


    def check(self:H499P,player:Player)-> bool:
        if len(player.gems) >= 1: 
            return False
        return True


exports = H499P()
