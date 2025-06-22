from __future__ import annotations

from contextlib import asynccontextmanager
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from litestar import Litestar


@asynccontextmanager
async def database_setup(app: Litestar):

    from app.config.app import alchemy
    from app.domain.access.crypt import hash_password
    from app.infrastructure.database import models as m
    from app.domain.access.services import UserService
    from advanced_alchemy.exceptions import DuplicateKeyError

    async with alchemy.get_session() as session:
        user_service = UserService(session)
        try:
            if not await user_service.exists(is_superuser=True):
                await user_service.create(
                    m.User(
                        email="admin@test",
                        password=hash_password("invarost"),
                        is_superuser=True,
                    ),
                    auto_commit=True,
                )
        except DuplicateKeyError:
            app.get_logger().info("Database already setup")
        else:
            app.get_logger().info("Database setup")

        yield
