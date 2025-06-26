from msgspec import Meta

from typing import Annotated

RawPassword = Annotated[str, Meta(
    min_length=4,
    max_length=100
)]
