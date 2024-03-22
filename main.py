from __future__ import annotations

from typing import TYPE_CHECKING

#import asyncio
#from collections.abc import Iterable
#from os import environ
#from autobahn.asyncio.wamp import ApplicationRunner, ApplicationSession
#from autobahn.wamp.types import ComponentConfig
from textual.app import App

from game.user import Me
from ui.screens.home import Home
from ui.screens.settings import Settings

if TYPE_CHECKING:
    from utils.networkmanager import NetworkManager
    


class Main(App):

    network: NetworkManager
    me : Me
    SCREENS = {"home": Home(), "settings": Settings()}  # noqa: RUF012
    def __init__(self) -> None: #session:ApplicationSession,runner:ApplicationRunner
        super().__init__()
        self.me = Me()
        self.me.get_file()


    def on_mount(self) -> None:
        self.push_screen("home")

    def trigger_error(self: Main,message: str):
        #TODO: do an error scree
        pass


    async def on_load(self) -> None:
        #self.runner.extra = {"ui":self}
        #b = self.runner.run(self.session,start_loop=False)
        #asyncio.create_task(b)
        pass








"""class Component(ApplicationSession):

    def __init__(self, config: ComponentConfig | None = None):
        super().__init__(config)
        self.ui = config.extra["ui"]
        self.ui.comp = self


    async def onJoin(self,details):
        pass"""



#url = environ.get("AUTOBAHN_DEMO_ROUTER", "ws://127.0.0.1:1234/ws")
#realm = "crossbardemo"
#runner = ApplicationRunner(url, realm)

t = Main()#runner=runner,session=Component)
t.run()