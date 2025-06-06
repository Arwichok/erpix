from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator
from pprint import pprint

from litestar import Litestar
from litestar.types import Scope

from app.database.services import UsersService
import logging
from app.config.app import alchemy
import secrets


@asynccontextmanager
async def on_startup(app: Litestar) -> AsyncGenerator[None, None]:
    async with alchemy.get_session() as db_session:
        users_service = UsersService(db_session)
        
        if not await users_service.exists(name="admin"):
            password = secrets.token_hex(8)
            pprint(password)
            app.get_logger().info("Creating admin user\n Password: %s", password)
            
            ...
            
            
        yield 