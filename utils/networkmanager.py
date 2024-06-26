from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING, Any, List

import ujson
from autobahn.asyncio.wamp import ApplicationRunner, ApplicationSession
from autobahn.wamp.request import Subscription
from autobahn.wamp.types import SubscribeOptions

from game.me import Me
from utils.useful import Result

if TYPE_CHECKING:
    from autobahn.wamp.types import ComponentConfig

    from main import Main
    from ui.screens.game import GameScreen

def generate_account() -> str:
    return ""

class NetworkManager(ApplicationSession):

    def __init__(self: NetworkManager, config: ComponentConfig | None = None) -> None:
        super().__init__(config)
        self.ui_app : Main = config.extra["ui"]
        self.ui_app.network = self
        self.me = Me(self.ui_app)

    async def onJoin(self: NetworkManager,_ : Any):
        await self.me.get_file()


    async def process_broadcast(self: NetworkManager,message:str):
        from_json = ujson.loads(message)
        game = self.me.player.game
        game_screen: GameScreen = self.ui_app.get_screen("game")


        match from_json["event"]:
            #each event is specific so needs to be handled differently
            case "NEW_TURN":
                player_id: int = from_json["player"]
                player = self.me.player.game.get_player(player_id)
                game.current_turn = player_id
                game_screen.log_event("The next turn has started.")
                game_screen.log_event(f"It is {player.nick}'s turn now.")

                game.next_turn(player.nick)

                if player.player_id == self.me.player_id:
                    #run as task so it does not block anything else
                    asyncio.create_task(self.me.run_turn(from_json["can_draw"]))

            case "PING":
                #used for checking if a client is still there
                game_screen.log_event("Received the ping")
                await self.call_function("com.games.pong",game.game_id,self.ui_app.me.token)

            case "PLAYER_ELIMINATED":
                #needs to check if player is us and send to menu if so
                #else set nickname to eliminated
                player_id: int = from_json["player"]
                player = self.me.player.game.get_player(player_id)
                player.set_nick("Disconnected")

                if player_id == self.me.player.player_id:
                    self.ui_app.pop_screen()
                    self.ui_app.trigger_error("The game has been disconnected!")
                    return

                game_screen.log_event(f"The player {player.nick} has been disconnected.")
                player.set_nick("Disconnected")
        

            case "PHASE_CHANGE":
                #dictionary to make it so the players a sentence
                phase_dict = {"DRAW":"Drawing",
                              "GET_MOVES": "Move Generation",
                              "CHOOSING_MOVES":"Choosing Moves",
                              "CHOOSING_ACTION":"Choosing Action",
                              "END_TURN":"Ending Turn",
                              }
                phase = from_json["phase"]
                phase_text = phase_dict[phase]
                game.phase_change(phase_text)
                game_screen.log_event(f"It is now {phase_text}")

            case "CARD_DRAW":
                player_id: int = from_json["player"]
                player = self.me.player.game.get_player(player_id)
                game_screen.log_event(f"{player.nick} has drawn a card")

            case "MOVE":
                player_id: int = from_json["player"]
                player = self.me.player.game.get_player(player_id)

                new_pos = from_json["pos"]
                passed_start = from_json["passed_start"]
                player.set_position(new_pos)
                game_screen.log_event(f"{player.nick} has moved {from_json["spaces"]} spaces{"." if passed_start ==0 else f" and passed start {passed_start} times."}")

            case "END_TURN":
                player_id: int = from_json["player"]
                player = self.me.player.game.get_player(player_id)

                game_screen.log_event(f"The player {player.nick} has ender their turn")

            case "STATS_CHANGE":
                player_id: int = from_json["player"]
                player = self.me.player.game.get_player(player_id)


                # set all the player's stats
                player.set_draw(from_json["draw"])
                player.set_money(from_json["cash"])
                player.set_luck(from_json["luck"])
                player.set_priority(from_json["priority"])
                player.set_move_min(from_json["move_min"])
                player.set_move_max(from_json["move_max"])
                player.set_position(from_json["position"])
                player.set_nick(from_json["nick"])
                

            case "DO_ACTION":
                game_screen.log_event(from_json["text"])


            case "BOARD_SYNC":
                pass


            case "PLAY_CARD":
                card = self.ui_app.card_manager.get_card(from_json["card_id"]).value
                player_id = from_json["player"]
                player = game.get_player(player_id)
                game_screen.log_event(card.play_line.format(player=player))


            case "PLAYER_JOIN":
                game_screen.log_event("Player join")
                game_join = self.ui_app.get_screen("game_join")
                player_object = game.add_player(from_json)
                game_join.player_add(player_object)


            case "GAME_START":
                await game.start_game()
            case "GAME_END":
                await game.end_game()
                
            case "GEM_ACQUIRED":
                game_screen.log_event(f"{from_json['player_id']} got a gem!")
                player = game.get_player(from_json["player_id"])
                player.give_gem(from_json["gem_id"])









    async def call_function(self: NetworkManager, address:str, *args: list[Any]) -> Result:
        res = await self.call(address, *args)
        res_object = Result.from_json(res)
        return res_object

    async def pull_card(self: NetworkManager, theme:str) -> Result:
        return await self.call_function("com.not_games.pull_card",theme,self.me.token)

    async def create_user(self: NetworkManager) -> Result:
        return await self.call_function("com.not_games.create_user")

    async def valid_token(self: NetworkManager,token:str) -> Result:
        return await self.call_function("com.not_games.valid_user",token)

    async def draw_card(self: NetworkManager, game_id: int, token: str) -> Result:
        return await self.call_function("com.games.draw_card",game_id,token)



    async def get_moves(self: NetworkManager, game_id:int, token:str) -> Result:
        return await self.call_function("com.games.get_moves",game_id,token)


    async def move(self: NetworkManager, game_id: int, token:str, spaces:int) -> Result:
        return await self.call_function("com.games.move_spaces", game_id, token, spaces)

    async def do_action(self: NetworkManager, game_id:int, token: str, activity_id: int) -> Result:
        return await self.call_function("com.games.do_action", game_id, token, activity_id)

    async def end_turn(self: NetworkManager, game_id:int, token: str) -> Result:
        return await self.call_function("com.games.end_turn", game_id,token)


    async def play_card(self: NetworkManager, game_id:int, token:str)-> Result:
        return await self.call_function("com.games.play_card", game_id, token)


    async def get_games(self: NetworkManager, token:str)-> Result:
        return await self.call_function("com.games.get_games", token)

    async def join_game(self: NetworkManager, token: str, game_id:int,nickname:str,deck: dict[int,int])-> Result:
        deck = {str(card_id):quantity for card_id, quantity in deck.items()}
        return await self.call_function("com.games.join_game", token, game_id,nickname,deck)

    async def create_game(self: NetworkManager,token:str, game_name:str)-> Result:
        return await self.call_function("com.games.create_game", token, game_name)


    async def subscribe_to_game(self: NetworkManager, game_id:int):
        self.subscribe(self.process_broadcast,f"games.{game_id}.events")


    async def get_players(self: NetworkManager,token:str, game_id: int)-> Result:
        return await self.call_function("com.games.get_players", token, game_id)

    async def get_cards(self: NetworkManager, token:str) -> Result:
        return await self.call_function("com.not_games.get_cards", token)

    async def get_money(self: NetworkManager, token:str) -> Result:
        return await self.call_function("com.not_games.money", token)

    async def start_game(self: NetworkManager) -> Result:
        return await self.call_function("com.games.start_game", self.me.token, self.me.player.game.game_id)
    
    async def leave_game(self: NetworkManager):
        return await self.call_function("com.games.leave_game", self.me.token, self.me.player.game.game_id)
