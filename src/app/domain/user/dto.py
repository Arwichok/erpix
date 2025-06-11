from msgspec import Struct, Meta
from typing import Annotated


RawPassword = Annotated[str, Meta(min_length=8, max_length=255)]


class UserPayload(Struct):
    email: Annotated[str, Meta(
        min_length=2,
        max_length=320
    )]
    password: RawPassword
