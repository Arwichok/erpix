from __future__ import annotations
from typing import TYPE_CHECKING

from advanced_alchemy import base

from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from .user import User



class Role(base.DefaultBase):
    __tablename__ = "roles"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    description: Mapped[str] = mapped_column(nullable=False)
    users: Mapped[list[User]] = relationship(back_populates="role", lazy="selectin")
    