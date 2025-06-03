from dataclasses import dataclass
from app.lib.wrong import Wrong
from msgspec import Struct, Meta
from typing import Annotated


class UserCreatePayload(Struct):
    name: Annotated[str, Meta(min_length=2)]
