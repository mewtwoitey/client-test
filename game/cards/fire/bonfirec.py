from __future__ import annotations

from typing import TYPE_CHECKING

from game.cards.card import Card, Rarity, Theme

if TYPE_CHECKING:
    from game.user import Player

class Bonfire(Card):
    def __init__(self) -> None:
        self.name = "Bonfire"
        self.card_id = 4
        self.theme = Theme.FIRE
        self.rarity = Rarity.COMMON
        self.description = self.description_generator()+"Always gives the player +1 to their min/max speed."
        self.play_line = "{player.nick} has deployed a bonfire and is now faster!"


    def check(self:Bonfire,player:Player)-> bool:
        return True

    def run(self,player:Player):
        player.move_min += 1
        player.move_max += 1


exports = Bonfire()