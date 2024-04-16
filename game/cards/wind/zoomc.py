from __future__ import annotations

from typing import TYPE_CHECKING

from game.cards.card import Card, Rarity, Theme

if TYPE_CHECKING:
    from game.user import Player
    
    
class Zoom(Card):
    
    def __init__(self) -> None:
        self.card_id = 18
        self.theme = Theme.WIND
        self.rarity = Rarity.COMMON
        self.name = "Zoom"
        self.description = self.description_generator()+"Sacrifice 1 priority to always draw cards"
        self.play_line = "{player.nick} feels sluggish but believes in the cards"

    def check(self: Card, player: Player) -> bool:
        return True
    


exports = Zoom()