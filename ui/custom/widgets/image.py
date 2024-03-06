from pathlib import Path

from textual.app import RenderResult
from textual.widget import Widget

from external.pixels import Pixels


class Image(Widget):
    def __init__(self: "Image", *children: Widget, name: str | None = None, id: str | None = None, classes: str | None = None, disabled: bool = False,filename:str="") -> None:  # noqa: PLR0913, A002, E501
        super().__init__(*children, name=name, id=id, classes=classes, disabled=disabled)
        path = Path(str(Path.cwd()) + f"/aseprite/{filename}")
        self.file_path = path

    def render(self) -> RenderResult:
        
        return Pixels.from_image_path(self.file_path)


