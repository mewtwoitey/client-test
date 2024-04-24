from __future__ import annotations

from typing import TYPE_CHECKING

from game.cards.card import Card, Rarity, Theme

if TYPE_CHECKING:
    from game.user import Player

class Plant(Card):
    def __init__(self) -> None:
        self.card_id = 9
        self.theme = Theme.EARTH
        self.rarity = Rarity.MEDIUM
        self.name = "Plant"
        self.description = self.description_generator()+"If a player is in the 3rd quarter of the board decrease, everyone else's luck by 0.3!"
        self.play_line = "A plant has sprouted but luck has decreased."

    def check(self: Plant, player:Player)-> bool:
        board_half = (player.game.board.length)//2
        board_third_quarter = ((player.game.board.length)//4)*3

        if (player.position <= board_third_quarter) and (player.position >= board_half):
            return True
        return False



exports = Plant()