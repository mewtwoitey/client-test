from __future__ import annotations

from typing import TYPE_CHECKING

from game.cards.card import Card, Rarity, Theme

if TYPE_CHECKING:
    from game.user import Player

class Explosion(Card):
    def __init__(self) -> None:
        self.name = "Explosion"
        self.card_id = 5
        self.theme = Theme.FIRE
        self.rarity = Rarity.COMMON
        self.description = self.description_generator()+"Always gives the player a +2 max move."
        self.play_line = "Explosion! {player.nick} now move faster!"


    def check(self:Explosion,player:Player)-> bool:
        return True




exports = Explosion()