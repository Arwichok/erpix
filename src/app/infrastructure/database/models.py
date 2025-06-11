from __future__ import annotations
from uuid import UUID


from advanced_alchemy import base

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship



class User(base.UUIDv7AuditBase):
    __tablename__ = "users"
    
    email: Mapped[str] = mapped_column(nullable=True, unique=True)
    password: Mapped[str] = mapped_column(nullable=False)
    role: Mapped[Role] = relationship("Role", back_populates="users")
    role_id: Mapped[UUID] = mapped_column(ForeignKey("roles.id"), nullable=False)


class Role(base.UUIDv7AuditBase):
    __tablename__ = "roles"
    
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    description: Mapped[str] = mapped_column(nullable=False)
    users: Mapped[list[User]] = relationship(back_populates="role")
    