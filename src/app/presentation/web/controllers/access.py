
from advanced_alchemy.extensions.litestar.providers import (
    create_service_dependencies,
)
from litestar import Controller, Response, get, post
from litestar.exceptions import NotAuthorizedException, ValidationException
from litestar.plugins.htmx import HTMXRequest, HTMXTemplate
from litestar.repository import NotFoundError
from litestar.response import Redirect, Template

from app.domain.access.services import UserService
from app.domain.access.schemas import UserPayload
from app.presentation.web.types import URLEncoded
from app.presentation.web.xrequest import XRequest



class AccessController(Controller):
    dependencies = {
        **create_service_dependencies(UserService, "user_service"),
    }

    @get("/login")
    async def get_login(self, request: XRequest) -> Template:
        return request.template(
            "access/login.html.j2", push_url="/login"
        )

    @get("/signup")
    async def get_signup(self, request: XRequest) -> Template:
        return request.template(
            "access/signup.html.j2", push_url="/signup"
        )

    @post("/login")
    async def post_login(
        self,
        request: XRequest,
        data: URLEncoded[UserPayload],
        user_service: UserService,
    ) -> Response:
        try:
            user = await user_service.authenticate(data)
            request.set_session({"user_id": user.id})
            return Redirect("/me")
        except NotAuthorizedException:
            return request.template(
                "access/login.html.j2", push_url="/login", block_name="password", context={"error": "Invalid credentials"}, re_target="label > #password", re_swap="outerHTML"
            )
        except NotFoundError as e:
            return request.template(
                "access/login.html.j2", push_url="/login", block_name="email", context={"error": "User not found"}, re_target="label > #email", re_swap="outerHTML"
            )
        except ValidationException as e:
            
            return request.template(
                "access/login.html.j2", push_url="/login", block_name="email", context={"error": "Invalid email"}, re_target="label > #email", re_swap="outerHTML"
            )

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

