from __future__ import annotations

from typing import TYPE_CHECKING

from game.game import Game
from game.user import Player
from utils.storage import read_from_save, write_to_save
from utils.useful import Result
from game.cards.card import Rarity

if TYPE_CHECKING:
    from main import Main
    from game.cards.card import Card


class Me:
    def __init__(self: Me, ui_app: Main) -> None:
        self.token: str = None
        self.decks: dict[str, dict[int, int]] = {}
        self.cards: dict[int, int] = {}
        self.player: Player = None
        self.hand: int = -1
        self.money = 0
        self.ui_app: Main = ui_app

    def update_file(self: Me) -> Result:
        to_json = {"token": self.token, "decks": self.decks}
        return write_to_save(to_json)

    async def get_file(self: Me) -> Result:
        from_json = read_from_save()
        if not from_json.successful:
            # if a file has not been found usually when it is the first time opening the game
            return Result(False)

        from_json = from_json.value
        await self.set_token(from_json["token"])
        for name, deck in from_json["decks"].items():
            self.add_deck(name, {int(card_id) : quantity for card_id,quantity in deck.items()})
        return Result(True)

    def is_registered(self: Me) -> bool:
        # used to prevent the user from doing action before they are logged in
        return self.token is not None

    async def set_token(self: Me, token: str) -> None:
        res = await self.ui_app.network.valid_token(token)
        valid = res.successful
        if valid:
            self.token = token
            self.player_id = int(token.split("{}")[0])
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
            return Result(False, "Account already exists.")

        res = await self.ui_app.network.create_user()
        token = res.value
        await self.set_token(token)
        self.update_file()
        return Result(True)

    async def run_turn(self: Me, can_draw: bool):
        """Runs the user's turn."""

        game_id = self.player.game.game_id
        token = self.ui_app.network.me.token
        game_screen = self.ui_app.get_screen("game")

        # 1 check if the user can draw and if so grab a card
        if can_draw:
            card_res = await self.ui_app.network.draw_card(game_id, token)
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

    async def join_game(self: Me, game_id: int, nickname: str, game_name: str):
        res = await self.ui_app.network.join_game(self.token, game_id, nickname)

        if not res.successful:
            self.ui_app.trigger_error(res.error_msg)

        game_object = Game(self.ui_app.network, game_id)

        await self.ui_app.network.subscribe_to_game(game_id)

        await self.ui_app.push_screen("game_join")

        game_join_screen = self.ui_app.get_screen("game_join")
        game_join_screen.set_game_name(game_name)

        players = await self.ui_app.network.get_players(self.token, game_id)

        for player_dict in players.value:
            player_object = game_object.add_player(player_dict)
            game_join_screen.player_add(player_object)

        self.player = game_object.players[self.player_id]

    async def create_game(self: Me, game_name: str, nickname: str):
        game_res = await self.ui_app.network.create_game(self.token, game_name)
        if not game_res.successful:
            self.trigger_error(game_res.error_msg)

        game_id = game_res.value


        await self.join_game(game_id, nickname=nickname, game_name=game_name)

    async def set_hand(self: Me, card_id: int) -> None:
        card_object_res = self.ui_app.card_manager.get_card(card_id=int)

        if not card_object_res.successful:
            self.ui_app.trigger_error("Card not found, the cards stored may not be up to date")

        card_object: Card = card_object_res.value

        game_screen = self.ui_app.get_screen("game")

        card_panel = game_screen.query_one("#card_information")

        card_panel.card_name = card_object.name
        card_panel.description = card_object.description

        self.hand = card_id

    def add_card_to_deck(self, deck_name:str, card_id: int):
        if deck_name not in self.decks:
            return Result(False, "deck not found")

        deck = self.decks[deck_name]

        # the the current number of occurrences

        occurrences = deck.get(card_id, 0)

        occurrences += 1

        # check it does not go above card limit
        if card_id not in self.cards:
            return Result(False, "Don't have that card.")

        allowed_occurrences = self.cards[card_id]

        if allowed_occurrences < occurrences:
            return Result(False, "To many card have been added to the deck")

        deck[card_id] = occurrences

        return Result(True)

    def remove_card_from_deck(self, deck_name:str, card_id:int):
        if deck_name not in self.decks:
            return Result(False, "deck not found")

        deck = self.decks[deck_name]

        # the the current number of occurrences

        occurrences = deck.get(card_id, 0)

        occurrences -= 1

        # check it does not go above card limit
        if card_id not in self.cards:
            return Result(False, "Don't have that card.")

        allowed_occurrences = self.cards[card_id]

        if allowed_occurrences < occurrences:
            return Result(False, "To many card have been added to the deck")

        deck[card_id] = occurrences

        return Result(True)


    def update_deck(self, deck_name:str, card_ids: list[int]):
        if deck_name not in self.decks:
            return Result(False, "deck not found")

        del self.decks[deck_name]


        self.add_deck(deck_name, {})

        for card_id in card_ids:
            res = self.add_card_to_deck(deck_name, card_id)
            if not res.successful:
                return res

        return Result(True)



    async def get_cards(self) -> Result:
        cards_res = await self.ui_app.network.get_cards(self.token)
        self.cards = {int(card_id): quantity for card_id, quantity in cards_res.value.items()}

    def validate_deck(self, deck: dict[int, int]) -> Result:
        """Checks if a deck complies with the rule around card limits and makes sure they own the cards.

        Parameters
        ----------
        deck : dict[int, int]
            the deck to check

        Returns
        -------
        Result
            successful -> valid, err_msg -> why it failed
        """
        has_high_tier_card = False #flag to check if there is already a 'high' tier card



        for card_id,quantity in deck.items():
            card_object_res = self.ui_app.card_manager.get_card(card_id=card_id)

            #usually if the card does not exist
            if not card_object_res.successful:
                return card_object_res

            card_object: Card = card_object_res.value

            if card_id not in self.cards:
                return Result(False, f"card not owned: {card_object.name}")




            max_quantity = self.cards[card_id]

            if quantity > max_quantity:
                return Result(False, f"You do not own {quantity} of {card_object.name}")



            card_object: Card = card_object_res.value

            rarity = card_object.rarity


            match rarity:


                case Rarity.HIGH:
                    if has_high_tier_card:
                        return Result(False, "More than 1 high rarity card.")


                    has_high_tier_card = True


                case Rarity.MEDIUM:
                    if quantity > 1:
                        return Result(False, f"You can only have 1 of {card_object.name}")

                case Rarity.COMMON:
                    if quantity > 3:
                        return Result(False, f"You can only have 3 of {card_object.name}")


        return Result(True)
