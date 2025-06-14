from pprint import pprint
from litestar import Controller, MediaType, Response, get, post
from litestar.exceptions import NotAuthorizedException, ValidationException
from litestar.plugins.htmx import HTMXRequest
from msgspec import ValidationError
from jinja2_fragments.litestar import HTMXBlockTemplate
from app.domain.user.dto import UserPayload
from app.infrastructure.database.services.user import UserService

from advanced_alchemy.extensions.litestar.providers import (
    create_service_dependencies,
)

from app.presentation.web.types import URLEncoded
from app.presentation.web.xrequest import XRequest
from litestar.response import Redirect, Template

def handle_not_authorized(request: XRequest, exc: NotAuthorizedException) -> Template:
    return request.template("access.html.j2",)
    

class AccessController(Controller):
    dependencies = {
        **create_service_dependencies(UserService, "user_service")
    }

    @get("/login")
    async def get_login(self, request: XRequest) -> Template:
        return request.template("access.html.j2", block_name="content", push_url="/login")

    @get("/signup")
    async def get_signup(self, request: XRequest) -> Template:
        return request.template("access.html.j2", block_name="content", push_url="/signup")

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
        user = await user_service.signup(data)
        request.set_session({"user_id": user.id})
        return request.template("me.html.j2", push_url="/me")
    