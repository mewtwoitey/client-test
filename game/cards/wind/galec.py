from __future__ import annotations

from typing import TYPE_CHECKING


from game.cards.card import Card, Rarity, Theme

if TYPE_CHECKING:
    from game.user import Player
    
    
class Gale(Card):
    
    def __init__(self) -> None:
        self.card_id = 13
        self.theme = Theme.WIND
        self.rarity = Rarity.HIGH
        self.name = "Gale"
        self.description = self.description_generator()+"If the player has no gems, sacrifice 5 priority to get a gem"
        self.play_line = "{player.nick} got sluggish but found a gem."


    def check(self: Card, player: Player) -> bool:
        if len(player.gems) >= 1:
            return False
        return True
    

        
exports = Gale()