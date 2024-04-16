from __future__ import annotations

from typing import TYPE_CHECKING

from game.cards.card import Card, Rarity, Theme

if TYPE_CHECKING:
    from game.user import Player


class Hurricane(Card):

    def __init__(self) -> None:
        self.card_id = 14
        self.theme = Theme.WIND
        self.rarity = Rarity.MEDIUM
        self.name = "Hurricane"
        self.description = self.description_generator()+"Sacrifice 100 cash for 2 priority."
        self.play_line = "A hurricane come through and stole 100 cash from {player.nick} and they became motivated."

    def check(self: Card, player: Player) -> bool:
        if player.cash >= 100:  # noqa: PLR2004
            return False
        return True


exports = Hurricane()
