from __future__ import annotations


from textual.reactive import reactive
from textual.widget import Widget


class PlayerList(Widget):
    """class used to make the player list on the board screen."""

    
    pos : reactive[int | None] = reactive(0)
    nickname : reactive[str | None] = reactive("no name")
    
    def __init__(self, *children: Widget, name: str | None = None, id: str | None = None, classes: str | None = None, disabled: bool = False, player_num:int) -> None:
        super().__init__(*children, name=name, id=id, classes=classes, disabled=disabled)
        self.player_num = player_num

    def render(self: PlayerList) -> str:
        return f"Player {self.player_num!s} : {self.nickname}\nPosition: {self.pos!s}"
    

class Phase(Widget):
    player_nick : reactive[str | None] = reactive("no name")
    phase: reactive[str | None] = reactive("draw")

    def render(self: Phase) -> str:
        return f"Phase: {self.phase}\nPlayer: {self.player_nick}"

class PlayerListStats(Widget):
    """Class used for displaying stats in the stats menu."""

    
    pos : reactive[int | None] = reactive(0)
    nickname : reactive[str | None] = reactive("no name")
    draw_chance: reactive[float] = reactive(0)
    move_min: reactive[int] = reactive(0)
    move_max: reactive[int] = reactive(0)
    money: reactive[int] = reactive(0)
    luck: reactive[float] = reactive(0)
    priority: reactive[int] = reactive(0)
    gems: reactive[int] = reactive(0)
    
    def __init__(self, *children: Widget, name: str | None = None, id: str | None = None, classes: str | None = None, disabled: bool = False, player_num:int) -> None:
        super().__init__(*children, name=name, id=id, classes=classes, disabled=disabled)
        self.player_num = player_num


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
    card_name : reactive[str | None] = reactive("Placeholder Name")
    description: reactive[str| None] = reactive("Placeholder description")


    def render(self: CardPanel) -> str:
        return f"Current Card: {self.description}"
    

class DecisionPanel(Widget):
    
    decision: reactive[str | None] = reactive("Nothing")

    def render(self: DecisionPanel) ->  str:
        return f"Decision to be made: {self.decision}"

