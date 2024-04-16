from __future__ import annotations

from typing import TYPE_CHECKING

from game.cards.card import Card, Rarity, Theme

if TYPE_CHECKING:
    from game.users import Player

class Elixir(Card):
    def __init__(self) -> None:
        self.card_id = 12
        self.theme = Theme.EARTH
        self.rarity = Rarity.COMMON
        self.name="Elixir"
        self.description= self.description_generator()+"If a player's luck is within 0.15 of the original value increase it by 0.1"
        self.play_line= "{player.nick} has gotten luckier."


    def check(self: Elixir, player:Player)-> bool:
        #get the distance from the starting value
        distance = abs(0.5 - player.luck)
        if distance >= 0.15:
            return True
        return False



exports = Elixir()
