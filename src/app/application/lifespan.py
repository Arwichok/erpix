from __future__ import annotations

from contextlib import asynccontextmanager
from pprint import pprint
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from litestar import Litestar


@asynccontextmanager
async def database_setup(app: Litestar):
    from sqlalchemy import Identity

    from app.config.app import alchemy
    from app.domain.user.dto import UserPayload
    from app.infrastructure.database import models as m
    from app.infrastructure.database.services.role import RoleService
    from app.infrastructure.database.services.user import UserService
    from advanced_alchemy.exceptions import DuplicateKeyError

    async with alchemy.get_session() as session:
        user_service = UserService(session)
        role_service = RoleService(session)
        try:
            await role_service.create_many(
                [
                    m.Role(name="guest", description="Guest role"),
                    m.Role(name="admin", description="Admin role"),
                ],
                auto_commit=True,
            )
            await user_service.create(
                m.User(
                    email="admin@test",
                    password=user_service.hash_password("invarost"),
                    role_id=(await role_service.get_one(name="admin")).id,
                ),
                auto_commit=True,
            )
        except DuplicateKeyError:
            app.get_logger().info("Database already setup")
        else:
            app.get_logger().info("Database setup")

        yield
