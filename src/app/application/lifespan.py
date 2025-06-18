from __future__ import annotations

from contextlib import asynccontextmanager
from pprint import pprint
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from litestar import Litestar


@asynccontextmanager
async def database_setup(app: Litestar):

    from app.config.app import alchemy
    from app.domain.access.crypt import hash_password
    from app.infrastructure.database import models as m
    from app.domain.access.services import RoleService, UserService
    from advanced_alchemy.exceptions import DuplicateKeyError

    async with alchemy.get_session() as session:
        user_service = UserService(session)
        role_service = RoleService(session)
        try:
            await role_service.create_many(
                [
                    m.Role(id=1, name="admin", description="Admin role"),
                    m.Role(id=2, name="guest", description="Guest role"),
                ],
                auto_commit=True,
            )
            await user_service.create(
                m.User(
                    email="admin@test",
                    password=hash_password("invarost"),
                    role_id=1
                ),
                auto_commit=True,
            )
        except DuplicateKeyError:
            app.get_logger().info("Database already setup")
        else:
            app.get_logger().info("Database setup")

        yield
