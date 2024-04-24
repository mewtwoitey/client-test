from __future__ import annotations

from typing import TYPE_CHECKING

from game.cards.card import Card, Rarity, Theme

if TYPE_CHECKING:
    from game.user import Player


class Tornado(Card):

    def __init__(self) -> None:
        self.card_id = 17
        self.theme = Theme.WIND
        self.rarity = Rarity.COMMON
        self.name = "Tornado"
        self.description = self.description_generator() + "Sacrifice 1 priority for 100 cash."
        self.play_line = "{player.nick} is sluggish but gains some cash."

    def check(self: Card, player: Player) -> bool:
        return True


    async def run(self: Card, player: Player) -> None:
        player.cash += 100
        player.priority -= 1

exports = Tornado()