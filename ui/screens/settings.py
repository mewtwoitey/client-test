from pathlib import Path

from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import Placeholder

from ui.custom.screens.subscreen import SubScreen


class Settings(SubScreen):
    def __init__(self: "Settings", name: str | None = None, id: str | None = None, classes: str | None = None) -> None:
        super().__init__(name, id, classes)
        self.CSS_PATH.append(Path(str(Path.cwd()) + "/ui/css/settings.tcss"))

    def compose(self: "Settings") -> ComposeResult:
        yield from super().compose() # gets all the elements from super
        with Container(id="content_cont"):
            yield Placeholder("settings")



