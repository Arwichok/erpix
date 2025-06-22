from litestar import Controller, Request, get
from litestar.exceptions import NotAuthorizedException
from litestar.response import Template

from app.domain.access.services import UserService
from app.presentation.web.xrequest import XRequest

from advanced_alchemy.extensions.litestar.providers import (
    create_service_dependencies,
)


def not_authorized(request: Request, exc: NotAuthorizedException) -> Template:
    return Template("404.html.j2", status_code=404)


class UsersController(Controller):
    path = "/users"
    exception_handlers = {
        NotAuthorizedException: not_authorized,
    }
    dependencies = {**create_service_dependencies(UserService, "user_service")}

    @get("/")
    async def get_users(
        self, request: XRequest, user_service: UserService
    ) -> Template:
        return request.template(
            "users.html.j2", context={"users": await user_service.list()}
        )
