from __future__ import annotations

from typing import TYPE_CHECKING

from game.cards.card import Card, Rarity, Theme

if TYPE_CHECKING:
    from game.user import Player

class EarthQuake(Card):
    def __init__(self) -> None:
        self.name = "EarthQuake"
        self.card_id = 7
        self.theme = Theme.EARTH
        self.rarity = Rarity.HIGH
        self.description = self.description_generator()+"If the player has no gems, increase luck to 0.9."
        self.play_line = "{player.nick} has gotten luckier!"


    def check(self:EarthQuake, player:Player)-> bool:
        if len(player.gems) >= 1:
            return False
        return True




exports = EarthQuake()
