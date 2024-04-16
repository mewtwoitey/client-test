from __future__ import annotations

from typing import TYPE_CHECKING

from game.cards.card import Card, Rarity, Theme

if TYPE_CHECKING:
    from game.user import Player


class Razor(Card):

    def __init__(self) -> None:
        self.card_id = 16
        self.theme = Theme.WIND
        self.rarity = Rarity.COMMON
        self.name = "Razor"
        self.description = self.description_generator()+"Sacrifice 2 max move speed for 1 priority."
        self.play_line = "The wind cuts into {player.nick} but they become motivated"


    def check(self: Card, player: Player) -> bool:
        if (player.move_max - player.move_min) > 3:  # noqa: PLR2004
            return True
        return False


exports = Razor()