
from pprint import pprint
from typing import Any
from advanced_alchemy.extensions.litestar.providers import (
    create_service_dependencies,
)
from litestar import Controller, Response, get, post
from litestar.exceptions import NotAuthorizedException, ValidationException, HTTPException
from litestar.plugins.htmx import HTMXRequest, HTMXTemplate
from litestar.repository import NotFoundError
from litestar.response import Redirect, Template

from app.domain.access.services import UserService
from app.domain.access.schemas import UserPayload
from app.domain.entities.user import User
from app.presentation.web.types import Form, URLEncoded
from app.presentation.web.utils import htmx_template
from app.presentation.web.xrequest import XRequest


def handle_exception(request: HTMXRequest, exc: HTTPException):
    pprint((
        "#"*50,
        {
        "args": exc.args,
        "detail": exc.detail,
        "extra": exc.extra,
        "headers": exc.headers,
        "status_code": exc.status_code},
        "#"*50
    ))
    if isinstance(exc.extra, list):
        exc.extra = {e['key']: e for e in exc.extra}
    
    if isinstance(exc.extra, dict) and isinstance(exc, ValidationException):
        if "password" in exc.extra:
            exc.extra["password"]["message"] = "Password must be at least 8 characters long."
        if "email" in exc.extra:
            exc.extra["email"]["message"] = "Invalid email address."
    return htmx_template(request, "access/form.html.j2", context={"exc": exc}, block_name="content")


class AccessController(Controller):
    dependencies = {
        **create_service_dependencies(UserService, "user_service"),
    }
    exception_handlers = {ValidationException: handle_exception} # type: ignore

    @get("/login")
    async def get_login(self, request: XRequest) -> Template:
        return request.template(
            "access/form.html.j2", push_url="/login"
        )

    @get("/signup")
    async def get_signup(self, request: XRequest) -> Template:
        return request.template(
            "access/form.html.j2", push_url="/signup"
        )

    @post("/login")
    async def post_login(
        self,
        request: XRequest,
        data: URLEncoded[User],
        user_service: UserService,
    ) -> Response:
        return Redirect("/me")
        # try:
        #     user = await user_service.authenticate(data)
        #     request.set_session({"user_id": user.id})
        #     return Redirect("/me")
        # except NotAuthorizedException:
        #     return request.template(
        #         "access/login.html.j2", push_url="/login", block_name="password", context={"error": "Invalid credentials"}, re_target="label > #password", re_swap="outerHTML"
        #     )
        # except NotFoundError as e:
        #     return request.template(
        #         "access/login.html.j2", push_url="/login", block_name="email", context={"error": "User not found"}, re_target="label > #email", re_swap="outerHTML"
        #     )
        # except ValidationException as e:
            
        #     return request.template(
        #         "access/login.html.j2", push_url="/login", block_name="email", context={"error": "Invalid email"}, re_target="label > #email", re_swap="outerHTML"
        #     )

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


    @post("/validate", exclude_from_auth=True)
    async def validate(self, request: XRequest,
        data: URLEncoded[dict],
    ) -> Template:
        email = data.get("email")
        if not (email and len(email) > 4):
            return request.template(
                "access/exception.html.j2",
                context={"message": "Invalid email"},
                re_swap="beforeend",
                re_target="#email-label",
            )
        return request.template(template_str="_", re_swap="none")