from __future__ import annotations

from typing import TYPE_CHECKING

from game.cards.card import Card, Rarity, Theme

if TYPE_CHECKING:
    from game.user import Player

class Monument(Card):
    def __init__(self) -> None:
        self.card_id = 8
        self.theme = Theme.EARTH
        self.rarity = Rarity.MEDIUM
        self.name = "Monument"
        self.description = self.description_generator()+ "If the players luck is more than 0.3, increase it by 0.35."
        self.play_line = "{player.nick} found a monument and is now luckier!"

    def check(self: Monument, player:Player)-> bool:
        if player.luck >= 0.3:
            return False
        return True



exports = Monument()
