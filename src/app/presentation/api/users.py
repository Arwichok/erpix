from typing import Sequence
from litestar import Controller, get, post

from app.infrastructure.database.services.user import UserService

from advanced_alchemy.extensions.litestar.providers import (
    create_service_dependencies,
)


from app.infrastructure.database import models as m


class UsersAPIController(Controller):
    dependencies = {
        **create_service_dependencies(UserService, "user_service")
    }

    @get("/users")
    async def get_users(self, user_service: UserService) -> Sequence[m.User]:
        return await user_service.list()