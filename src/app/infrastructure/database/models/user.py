from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from advanced_alchemy import base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from .role import Role


class User(base.UUIDv7AuditBase):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(nullable=True, unique=True)
    password: Mapped[str] = mapped_column(nullable=False)
    role: Mapped[Role] = relationship(
        lazy="joined", innerjoin=True, viewonly=True
    )
    role_id: Mapped[UUID] = mapped_column(
        ForeignKey("roles.id"), nullable=False
    )
