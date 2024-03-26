from __future__ import annotations


from textual.reactive import reactive
from textual.widget import Widget


class PlayerList(Widget):
    """class used to make the player list on the board screen."""

    player_num : reactive[int | None]= reactive(0)
    pos : reactive[int | None] = reactive(0)
    nickname : reactive[str | None] = reactive("test name")

    def render(self: PlayerList) -> str:
        return f"Player {self.player_num!s} : {self.nickname}\nPosition: {self.pos!s}"
    

class Phase(Widget):
    player_nick : reactive[str | None] = reactive("test name")
    phase: reactive[str | None] = reactive("draw")

    def render(self: Phase) -> str:
        return f"Phase: {self.phase}\nPlayer: {self.player_nick}"

class PlayerListStats(Widget):
    """Class used for displaying stats in the stats menu."""

    player_num : reactive[int | None]= reactive(0)
    pos : reactive[int | None] = reactive(0)
    nickname : reactive[str | None] = reactive("test name")
    draw_chance: reactive[float] = reactive(0.33)
    move_min: reactive[int] = reactive(2)
    move_max: reactive[int] = reactive(8)
    money: reactive[int] = reactive(0)
    luck: reactive[float] = reactive(0.7)
    priority: reactive[int] = reactive(100)


    def render(self: PlayerListStats) -> str:
        return f"""Player {self.player_num!s} : {self.nickname}
Position: {self.pos!s}
Draw Chance: {self.draw_chance!s}
Minimum Move: {self.move_min!s}
Maximum Move: {self.move_max!s}
Money: {self.money!s}
Luck: {self.luck!s}
Priority: {self.priority!s}"""


class CardPanel(Widget):
    name : reactive[str | None] = reactive("Placeholder Name")
    description: reactive[str| None] = reactive("Placeholder description")


    def render(self: CardPanel) -> str:
        return f"Current Card: {self.name}\nDescription: {self.description}"
    

class DecisionPanel(Widget):
    
    decision: reactive[str | None] = reactive("Nothing")

    def render(self: DecisionPanel) ->  str:
        return f"Decision to be made: {self.decision}"

