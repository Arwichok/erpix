from __future__ import annotations


from advanced_alchemy import base

from sqlalchemy import BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship



# Core
class User(base.UUIDv7AuditBase):
    __tablename__ = "users"
    
    name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    password: Mapped[str] = mapped_column(nullable=False)
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"), nullable=False)
    roles: Mapped[list[Role]] = relationship(back_populates="users")


class Role(base.AdvancedDeclarativeBase):
    __tablename__ = "roles"
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    users: Mapped[list[User]] = relationship(back_populates="roles")