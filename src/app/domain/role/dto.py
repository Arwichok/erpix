from msgspec import Struct, Meta

from typing import Annotated


class Role(Struct):
    name: str
    description: str
