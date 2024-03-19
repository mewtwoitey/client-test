import math
from pathlib import Path

from textual.app import RenderResult
from textual.widget import Widget
from PIL import Image as Imgpil

from external.pixels import Pixels


class Image(Widget):
    def __init__(self: "Image", *children: Widget, name: str | None = None, id: str | None = None, classes: str | None = None, disabled: bool = False,filename:str="") -> None:  # noqa: PLR0913, A002, E501
        super().__init__(*children, name=name, id=id, classes=classes, disabled=disabled)
        path = Path(str(Path.cwd()) + f"/aseprite/{filename}")
        self.file_path = path
        self.image_object = Imgpil.open(self.file_path)
        self.aspect = self.image_object.width / self.image_object.height

    def render(self) -> RenderResult:
        screen_size = self.container_size # get the screen size
        target_height = screen_size.height *2
        #keep the height and resize the other bits 
        target_width = math.floor(self.aspect*target_height)
        resized = self.image_object.resize((target_width,target_height), Imgpil.Resampling.NEAREST)


        return Pixels.from_image(resized)


