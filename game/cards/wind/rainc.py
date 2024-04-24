from __future__ import annotations

from typing import TYPE_CHECKING


from game.cards.card import Card, Rarity, Theme

if TYPE_CHECKING:
    from game.user import Player


class Rain(Card):

    def __init__(self) -> None:
        self.card_id = 15
        self.theme = Theme.WIND
        self.rarity = Rarity.MEDIUM
        self.name = "Rain"
        self.description = self.description_generator()+"Sacrifice 2 min move speed for 1 priority."
        self.play_line = "Rain made {player.nick} wet, but they are now motivated."

    def check(self: Card, player: Player) -> bool:
        if player.move_min >= 3:  # noqa: PLR2004
            return True
        return False



exports = Rain()