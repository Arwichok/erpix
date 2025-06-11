from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from litestar.connection import ASGIConnection


async def retrieve_user_handler(
    session: dict[str, Any],
    connection: ASGIConnection[Any, Any, Any, Any],
):
    from app.config.app import alchemy
    from app.infrastructure.database.models import User

    return await alchemy.provide_session(
        connection.app.state, connection.scope
    ).get(User, session["user_id"])
