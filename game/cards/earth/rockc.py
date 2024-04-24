from __future__ import annotations

from typing import TYPE_CHECKING

from game.cards.card import Card, Rarity, Theme

if TYPE_CHECKING:
    from game.user import Player

class Rock(Card):
    def __init__(self) -> None:
        self.card_id = 10
        self.theme = Theme.EARTH
        self.rarity = Rarity.COMMON
        self.name = "Rock"
        self.description = self.description_generator()+"Always resets luck to 0.5."
        self.play_line = "{player.nick} got hit by a rock and their luck got reset."


    def check(self: Rock, player:Player)-> bool:
        return True


exports = Rock()
