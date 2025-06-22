from __future__ import annotations


from advanced_alchemy import base
from sqlalchemy.orm import Mapped, mapped_column


class User(base.UUIDv7AuditBase):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(nullable=True, unique=True)
    password: Mapped[str] = mapped_column(nullable=False)
    is_superuser: Mapped[bool] = mapped_column(nullable=False, default=False)
    is_active: Mapped[bool] = mapped_column(nullable=False, default=True)
    is_verified: Mapped[bool] = mapped_column(nullable=False, default=False)
