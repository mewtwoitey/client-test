from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import ujson


# used for handling errors
@dataclass
class Result:
    successful : bool
    error_msg : str = ""
    value: Any = None



    def from_json(self: Result,json_str: str) -> :
        dumped = ujson.loads(json_str)
        self.successful = dumped["suc"]
        self.error_msg = dumped["err_msg"]
        self.value = dumped["val"]



