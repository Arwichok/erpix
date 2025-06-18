from pprint import pprint

from advanced_alchemy.extensions.litestar.providers import (
    create_service_dependencies,
)
from jinja2_fragments.litestar import HTMXBlockTemplate
from litestar import Controller, MediaType, Response, get, post
from litestar.exceptions import NotAuthorizedException, ValidationException
from litestar.plugins.htmx import HTMXRequest
from litestar.response import Redirect, Template
from msgspec import ValidationError

from app.domain.access.services import RoleService, UserService
from app.domain.access.schemas import UserPayload
from app.presentation.web.types import URLEncoded
from app.presentation.web.xrequest import XRequest


def handle_not_authorized(
    request: XRequest, exc: NotAuthorizedException
) -> Template:
    return request.template(
        "access.html.j2",
    )


class AccessController(Controller):
    dependencies = {
        **create_service_dependencies(UserService, "user_service"),
        **create_service_dependencies(RoleService, "role_service"),
    }

    @get("/login")
    async def get_login(self, request: XRequest) -> Template:
        return request.template(
            "access.html.j2", block_name="content", push_url="/login"
        )

    @get("/signup")
    async def get_signup(self, request: XRequest) -> Template:
        return request.template(
            "access.html.j2", block_name="content", push_url="/signup"
        )

    @post("/login")
    async def post_login(
        self,
        request: XRequest,
        data: URLEncoded[UserPayload],
        user_service: UserService,
    ) -> Response:
        user = await user_service.authenticate(data)
        request.set_session({"user_id": user.id})
        return Redirect("/me")

    @get("/me")
    async def get_me(self, request: XRequest) -> Template:
        return request.template("me.html.j2", push_url="/me")

    @get("/logout")
    async def get_logout(self, request: XRequest) -> Response:
        request.clear_session()
        return Redirect("/")

    @post("/signup")
    async def post_singup(
        self,
        request: XRequest,
        data: URLEncoded[UserPayload],
        user_service: UserService,
    ) -> Response:
        user = await user_service.signup(data, role_id=2)
        request.set_session({"user_id": user.id})
        return request.template("me.html.j2", push_url="/me")
