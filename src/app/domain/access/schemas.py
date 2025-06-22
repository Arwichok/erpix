from dataclasses import dataclass
from datetime import datetime
from uuid import UUID
from litestar.plugins.sqlalchemy import SQLAlchemyDTO
from msgspec import Struct, Meta
from typing import Annotated
from app.infrastructure.database import models as m

RawPassword = Annotated[str, Meta(min_length=8, max_length=255)]


class UserPayload(Struct):
    email: Annotated[str, Meta(
        min_length=2,
        max_length=320
    )]
    password: RawPassword


@dataclass
class UserRead:
    id: UUID
    email: str
    created_at: datetime
