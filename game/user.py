from __future__ import annotations

from utils.storage import write_to_save, read_from_save
from utils.networkmanager import NetworkManager
from utils.useful import Result

class Player:
    gems : list[str]

    def __init__(self: Player, nickname:str) -> None:
        self.nick = nickname
        self.draw_chance = 0.33
        self.move_min = 2
        self.move_max = 8
        self.money =  0
        self.luck = 0.7


    def get_id(self: Player)-> str:
        return "player_" + self._user.userid


class Me:
    token : str
    decks: dict[str,dict[int, int]] = {}
    cards: dict[int,int] = {}
    player: Player
    hand: int


    def update_file(self: Me):
        to_json = {"token": self.token, "decks": self.decks}
        return write_to_save(to_json)

    def get_file(self: Me):
        from_json = read_from_save()
        if not from_json.successful:
            return

        from_json = from_json.value
        self.token = from_json["token"]
        self.decks = from_json["decks"]

    def is_registered(self: Me) -> bool:
        #used to prevent the user from doing action before they are logged in
        return self.token is not None

    def set_token(self: Me,token: str) -> None:
        # verify token works here
        self.token = token

    def add_deck(self:Me, name: str, deck: dict[int,int]) -> Result:
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
        #stop two decks being named the same thing
        if name in self.decks:
            return Result(False,"That deck already exists")

        # check if the user actually owns all those cards
        self.decks[name] = deck
        return Result(True)


