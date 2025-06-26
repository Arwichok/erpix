from msgspec import Meta
from typing import Annotated


Email = Annotated[str, Meta(
    pattern=r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
)]
