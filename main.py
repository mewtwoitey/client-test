from __future__ import annotations

from typing import TYPE_CHECKING

import asyncio
#from collections.abc import Iterable
#from os import environ
from autobahn.asyncio.wamp import ApplicationRunner
from textual.app import App

from game.user import Me
from ui.screens.home import Home
from ui.screens.settings import Settings
from ui.screens.game import GameScreen
from utils.networkmanager import NetworkManager




class Main(App):

    network: NetworkManager
    me : Me
    SCREENS = {"home": Home(), "settings": Settings(), "game": GameScreen()}  # noqa: RUF012
    def __init__(self) -> None: #session:ApplicationSession,runner:ApplicationRunner
        super().__init__()


    def on_mount(self) -> None:
        self.push_screen("game")

    def trigger_error(self: Main,message: str):
        #TODO: do an error scree
        pass


    async def on_load(self) -> None:

        #start the networking on the load
        runner = ApplicationRunner("ws://127.0.0.1:1234/ws","game")
        runner.extra = {"ui":self}
        b = runner.run(NetworkManager,start_loop=False)
        asyncio.create_task(b)











#url = environ.get("AUTOBAHN_DEMO_ROUTER", "ws://127.0.0.1:1234/ws")
#realm = "crossbardemo"
#runner = ApplicationRunner(url, realm)

t = Main()#runner=runner,session=Component)
t.run()