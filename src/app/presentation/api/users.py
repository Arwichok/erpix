from typing import Sequence
from litestar import Controller, get

from app.domain.access.services import UserService

from advanced_alchemy.extensions.litestar.providers import (
    create_service_dependencies,
)




class UsersAPIController(Controller):
    dependencies = {
        **create_service_dependencies(UserService, "user_service")
    }

    @get("/users")
    async def get_users(self, user_service: UserService) -> Sequence[dict]:
        return [
            {
                "id": u.id,
                "email": u.email,
                "created_at": u.created_at,
            }
            for u in await user_service.list()
        ]