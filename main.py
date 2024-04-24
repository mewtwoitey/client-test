from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

#from collections.abc import Iterable
#from os import environ
from autobahn.asyncio.wamp import ApplicationRunner
from textual.app import App

from game.cards.card import CardManager
from ui.custom.screens.popup import ErrorPopup
from ui.screens.game import GameScreen
from ui.screens.game_join import GameJoinScreen
from ui.screens.game_searching import SearchScreen
from ui.screens.home import Home
from ui.screens.settings import Settings
from ui.screens.pulling_menu import PullingMenu
from ui.screens.card_management import CardManagement
from utils.networkmanager import NetworkManager

if TYPE_CHECKING:
    from game.me import Me
import sys
import os

#gotten from https://pyinstaller.org/en/stable/runtime-information.html it is not my code

class Main(App):

    network: NetworkManager
    me : Me
    SCREENS = {"home": Home(),
            "settings": Settings(),
            "game": GameScreen(),
            "searching": SearchScreen(),
            "game_join": GameJoinScreen(),
            "card_pull": PullingMenu(),
            "card_management": CardManagement()}  # noqa: RUF012
    decision_made = asyncio.Event()
    decision = None
    def __init__(self) -> None: #session:ApplicationSession,runner:ApplicationRunner
        super().__init__()
        self.card_manager = CardManager(self)
        self.card_manager.setup_cards()
        self.decision_made = asyncio.Event()
        self.decision = None


    def on_mount(self) -> None:
        self.push_screen("game")
        self.push_screen("home")

    def trigger_error(self: Main,message: str):
        self.app.push_screen(
            ErrorPopup(err_msg=message),
        )



    async def on_load(self) -> None:
        if os.path.exists("ip.txt"):
            with open("ip.txt") as f:
                ip_addr = f.read()
        else:
            ip_addr = "127.0.0.1"
        #start the networking on the load
        runner = ApplicationRunner(f"ws://{ip_addr}:1234/ws","game")
        runner.extra = {"ui":self}
        b = runner.run(NetworkManager,start_loop=False)
        asyncio.create_task(b)











#url = environ.get("AUTOBAHN_DEMO_ROUTER", "ws://127.0.0.1:1234/ws")
#realm = "crossbardemo"
#runner = ApplicationRunner(url, realm)

t = Main()#runner=runner,session=Component)
t.run()