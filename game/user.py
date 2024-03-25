from __future__ import annotations

from typing import TYPE_CHECKING

from utils.storage import read_from_save, write_to_save
from utils.useful import Result

if TYPE_CHECKING:
    from game.game import Game
    from main import Main

class Player:
    gems: list[str]
    player_id: int
    game: Game

    def __init__(self: Player, nickname: str) -> None:
        self.nick = nickname
        self.draw_chance = 0.33
        self.move_min = 2
        self.move_max = 8
        self.money = 0
        self.luck = 0.5




class Me:
    def __init__(self: Me, ui_app: Main) -> None:
        self.token: str = None
        self.decks: dict[str, dict[int, int]] = {}
        self.cards: dict[int, int] = {}
        self.player: Player = None
        self.hand: int = None
        self.ui_app: Main = ui_app

    def update_file(self: Me) -> Result:
        to_json = {"token": self.token, "decks": self.decks}
        return write_to_save(to_json)

    async def get_file(self: Me) -> Result:
        from_json = read_from_save()
        if not from_json.successful:
            #if a file has not been found usually when it is the first time opening the game
            return Result(False)

        from_json = from_json.value
        await self.set_token(from_json["token"])
        for name, deck in from_json["decks"]:
            self.add_deck(name,deck)
        return Result(True)

    def is_registered(self: Me) -> bool:
        # used to prevent the user from doing action before they are logged in
        return self.token is not None

    async def set_token(self: Me, token: str) -> None:
        res = await self.ui_app.network.valid_token(token)
        valid = res.successful
        if valid:
            self.token = token
        else:
            self.ui_app.trigger_error(res.error_msg)

    def add_deck(self: Me, name: str, deck: dict[int, int]) -> Result:
        """Adds a deck to the user's list of decks.

        Parameters
        ----------
        name : str
            The name of the deck.
        deck : dict[int,int]
            A dict with a key of cardID and a value of the quantity

        Returns
        -------
        Result
            Any error raised particularly if the deck name already exists
        """
        # stop two decks being named the same thing
        if name in self.decks:
            return Result(False, "That deck already exists")

        # check if the user actually owns all those cards
        self.decks[name] = deck
        return Result(True)

    async def pull_card(self: Me, theme: str) -> int:
        card_id = await self.ui_app.network.pull_card(theme)
        if card_id in self.cards:
            self.cards[card_id] += 1
        else:
            self.cards[card_id] = 1

        return card_id

    async def create_user(self: Me):
        if self.is_registered():
            return Result(False,"Account already exists.")
    
        res = await self.ui_app.network.create_user()
        token  = res.value
        await self.set_token(token)
        self.update_file()
        return Result(True)

    async def run_turn(self: Me, can_draw : bool):
        """Runs the user's turn."""

        game_id = self.player.game.game_id
        player_id = self.player.player_id

        # 1 check if the user can draw and if so grab a card
        if can_draw:
            card_res  = await self.ui_app.network.draw_card(game_id, player_id)
            if card_res.successful:
                self.hand = card_res.value
            # TODO ERROR check this
                


        # 2 prompt for moving spaces
        space_res = await self.ui_app.network.get_moves(game_id, player_id)
        if not space_res.successful:
            # TODO server probably down
            pass
        # TODO add to decision tab
        await self.ui_app.decision_made.wait()
        await self.ui_app.decision_made.clear()
        spaces = self.ui_app.decision 


        activities = await self.ui_app.network.move(game_id, player_id, spaces)
        if not activities.successful:
            pass

        activities = activities.value


        # 3 prompt user to choose an activity
        #TODO add to decision tab

        await self.ui_app.decision_made.wait()
        await self.ui_app.decision_made.clear()
        activity_id = self.ui_app.decision 

        activity_results = self.network.do_action(game_id,player_id, activity_id)


        # 4 end turn
        


