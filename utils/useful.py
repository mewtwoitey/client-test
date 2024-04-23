from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

import ujson
import sys

if TYPE_CHECKING:
    from typing import Any, Self

# used for handling errors
@dataclass
class Result:
    successful : bool
    error_msg : str = ""
    value: Any = None



    def from_json(json_str: str) -> Self:
        dumped = ujson.loads(json_str)
        res = Result(
            dumped["suc"],
            dumped["err_msg"],
            dumped["val"],
        )
        return res



def get_base_path():
    """Returns the base path of any resources."""
    if hasattr(sys, "_MEIPASS"):
        return sys._MEIPASS
    return str(Path.cwd())
