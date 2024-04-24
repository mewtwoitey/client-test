from __future__ import annotations

from typing import TYPE_CHECKING

from game.cards.card import Card, Rarity, Theme

if TYPE_CHECKING:
    from game.user import Player


class Kai(Card):
    def __init__(self) -> None:
        self.card_id = 3
        self.rarity = Rarity.MEDIUM
        self.theme = Theme.FIRE
        self.name = "Kai"
        self.description = self.description_generator()+"If the player has luck less than 0.4, the player can decrease everyone else's min move by 3"
        self.play_line = "Because {player.nick} is unlucky everyone else's min move has decreased"

    def check(self: Card, player: Player) -> bool:
        # check if the player is unlucky
        if player.luck <= 0.4:
            return True

        return False





exports = Kai()
