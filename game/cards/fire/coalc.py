from __future__ import annotations

from typing import TYPE_CHECKING


from game.cards.card import Card, Rarity, Theme
from utils.useful import Result

if TYPE_CHECKING:
    from game.user import Player


class Coal(Card):
    def __init__(self) -> None:
        self.name = "Coal"
        self.card_id = 2
        self.rarity = Rarity.MEDIUM
        self.theme = Theme.FIRE
        self.description = self.description_generator()+"Decreases everyone elses max move by 3. Can only be played while the player is in the second half of the board."
        self.play_line = "{player.nick} has given everyone coal! Slow down."


    def check(self: Card, player: Player) -> bool:
        # should be true when the player is in the second part of the board
        if player.position > (player.game.board.length)//2:
            return True

        return False





exports = Coal()