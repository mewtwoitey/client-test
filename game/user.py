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
        self.luck = 0.5
        self.priority = 100
        self.cash = 0
        self.position = 0
        self.screen_pos = -1

    def set_nick(self: Player, nick:str) -> None:
        self.nick = nick
        game_screen = self.game.network.ui_app.get_screen("game")
        game_screen.query_one(f"#player_list_stats_{self.screen_pos}").nickname = nick
        game_screen.query_one(f"#player_list_{self.screen_pos}").nickname = nick


    def set_position(self: Player, position: int) -> None:
        self.position = position
        game_screen = self.game.network.ui_app.get_screen("game")
        game_screen.query_one(f"#player_list_stats_{self.screen_pos}").pos = position
        game_screen.query_one(f"#player_list_{self.screen_pos}").pos = position


    def set_screen_pos(self: Player, screen_position: int) -> None:
        self.screen_pos = screen_position
        game_screen = self.game.network.ui_app.get_screen("game")
        game_screen.query_one(f"#player_list_stats_{self.screen_pos}").player_num = screen_position
        game_screen.query_one(f"#player_list_{self.screen_pos}").player_num = screen_position

    def set_draw(self: Player, draw: float) -> None:
        self.draw_chance = draw
        game_screen = self.game.network.ui_app.get_screen("game")
        game_screen.query_one(f"#player_list_stats_{self.screen_pos}").draw_chance = draw

    def set_move_min(self: Player, move_min: int) -> None:
        self.move_min = move_min
        game_screen = self.game.network.ui_app.get_screen("game")
        game_screen.query_one(f"#player_list_stats_{self.screen_pos}").move_min = move_min

    def set_move_max(self: Player, move_max: int) -> None:
        self.move_max = move_max
        game_screen = self.game.network.ui_app.get_screen("game")
        game_screen.query_one(f"#player_list_stats_{self.screen_pos}").move_max = move_max

    def set_money(self: Player, money: float) -> None:
        self.money = money
        game_screen = self.game.network.ui_app.get_screen("game")
        game_screen.query_one(f"#player_list_stats_{self.screen_pos}").money = money

    def set_luck(self: Player, luck: float) -> None:
        self.luck = luck
        game_screen = self.game.network.ui_app.get_screen("game")
        game_screen.query_one(f"#player_list_stats_{self.screen_pos}").luck = luck

    def set_priority(self: Player, priority: int) -> None:
        self.priority = priority
        game_screen = self.game.network.ui_app.get_screen("game")
        game_screen.query_one(f"#player_list_stats_{self.screen_pos}").priority = priority


class Me:
    def __init__(self: Me, ui_app: Main) -> None:
        self.token: str = None
        self.decks: dict[str, dict[int, int]] = {}
        self.cards: dict[int, int] = {}
        self.player: Player = None
        self.hand: int = -1
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
        token = self.ui_app.me.token
        game_screen = self.ui_app.get_screen("game")

        # 1 check if the user can draw and if so grab a card
        if can_draw:
            card_res  = await self.ui_app.network.draw_card(game_id, token)
            if card_res.successful:
                self.hand = card_res.value
            # TODO ERROR check this
                


        # 2 prompt for moving spaces
        space_res = await self.ui_app.network.get_moves(game_id, token)
        if not space_res.successful:
            # TODO server probably down
            pass
        game_screen.decision_moves(space_res.value)
        await self.ui_app.decision_made.wait()
        await self.ui_app.decision_made.clear()
        spaces = self.ui_app.decision 


        activities = await self.ui_app.network.move(game_id, token, spaces)
        if not activities.successful:
            pass

        activities = activities.value


        # 3 prompt user to choose an activity
        game_screen.decision_activity(space_res.value)

        await self.ui_app.decision_made.wait()
        await self.ui_app.decision_made.clear()
        activity_id = self.ui_app.decision

        activity_results = await self.ui_app.network.do_action(game_id, token, activity_id)

        if not activity_results.successful:
            pass

        # 4 end turn
        await self.ui_app.decision_made.wait()
        await self.ui_app.decision_made.clear()
        await self.ui_app.network.end_turn()
        game_screen.clear_decision()

    async def play_card(self: Me) -> Result:
        if self.hand == -1:
            # there is no card in the player's hand
            self.ui_app.trigger_error("There is no card that can be played! Report this to the developer.")
            return

        can_be_played = self.ui_app.card_manager.call_card(self.hand, self.player)


        if not can_be_played.successful:
            self.ui_app.trigger_error(can_be_played.error_msg)

        
        await self.ui_app.network.play_card()
