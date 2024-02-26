import asyncio
from collections.abc import Iterable

from textual.app import App, ComposeResult
from textual.widget import Widget
from textual.widgets import Button


class TestWidget(App):
    def compose(self) -> Iterable[Widget]:
        yield Button("test",id="test")

    async def on_load(self) -> None:

        self.bind("escape", "quit")

class Component(ApplicationSession):
    """
    An application component that subscribes and receives events, and
    stop after having received 5 events.
    """

    async def onJoin(self, details):

        self.received = 0

        def on_event(i):
            print("Got event: {}".format(i))
            self.received += 1
            if self.received > 5:
                self.leave()
        
        await self.subscribe(on_event, 'com.myapp.topic1')

    def onDisconnect(self):
        asyncio.get_event_loop().stop()

t = TestWidget()
t.run()
