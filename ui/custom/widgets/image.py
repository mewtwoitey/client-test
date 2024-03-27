import math
from pathlib import Path
from typing import TYPE_CHECKING

from textual.app import RenderResult
from textual.widget import Widget
from PIL import Image as Imgpil
import numpy
from copy import deepcopy

from external.pixels import Pixels, FullcellRenderer

if TYPE_CHECKING:
    from game.game import Game


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


class Board_Image(Widget):
    def __init__(self, *children: Widget, name: str | None = None, id: str | None = None, classes: str | None = None, disabled: bool = False, game: Game) -> None:
        super().__init__(*children, name=name, id=id, classes=classes, disabled=disabled)
        self.board = game.board
        self.char_to_colour = {
            1: (255, 0, 0, 1),
            2: (0, 255, 0, 1),
            3: (0, 0, 255, 1),
            4: (128, 0, 128, 1),
            None: (255,255,224,0.3),
        }
        self.nothing = (0,0,0,0)
        self.board_length = self.board.length //4
        self.array = numpy.full((self.board_length, self.board_length), self.empty)
        self.aspect = 1


    def render(self) -> RenderResult:
        #now to convert this to an image
        #note: help me
        array = deepcopy(self.array)
        dy = 0
        dx = 0
        posx = 0
        posy = 0

        for item in self.board._list:
            if posx == 0:
                if posy == self.board_length -1:
                    dy = -1
                    dx = 0
                elif posy == 0:
                    dy = 0
                    dx = 1
            elif posx == self.board_length -1:
                if posy == self.board_length -1:
                    dy = 0
                    dx = -1
                elif posy == 0:
                    dy = 1
                    dx = 0

            posx += dx
            posy += dy

            if len(item)  == 0:
                array[posx ,posy] = self.char_to_colour[None]
            else:
                array[posx ,posy] = self.char_to_colour[item[0]]




        image_onject = Imgpil.fromarray(array,mode="RGBA")
        # resize the image
        screen_size = self.container_size # get the screen size
        target_height = screen_size.height 
        #keep the height and resize the other bits 
        target_width = math.floor(self.aspect*target_height)
        resized = self.image_object.resize((target_width,target_height), Imgpil.Resampling.NEAREST)


        return Pixels.from_image(resized, renderer=FullcellRenderer)
