from dataclasses import dataclass
from msgspec import Meta, convert
from typing import Annotated
from litestar.params import Parameter


Email = Annotated[str, Meta(
    pattern=r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
)]
