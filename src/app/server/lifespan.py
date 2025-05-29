from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator
from pprint import pprint

from litestar import Litestar

from app.database.services import UsersService




@asynccontextmanager
async def on_startup(app: Litestar) -> AsyncGenerator[None, None]:
    yield 