from typing import Optional
from dataclasses import dataclass
from typing import Optional
from functools import lru_cache
import math




@dataclass(frozen=True)
class Pallet:
    length: int
    width: int
    height: int
    stackable: bool
    weight: Optional[int] = None 


@dataclass(frozen=True)
class FloorUnit:
    length: int
    width: int
