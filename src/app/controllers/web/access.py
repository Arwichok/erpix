from pprint import pprint
from typing import Any

from litestar import Controller, MediaType, Request, Response, get, post
from litestar.connection import ASGIConnection
from litestar.plugins.htmx import HTMXRequest
from litestar.response import Redirect, Template
from jinja2_fragments.litestar import HTMXBlockTemplate

from app.config.app import alchemy
from app.database import models as m
from app.database.services import UsersService
from app.lib.types import URLEncoded
from app.lib.xrequest import XRequest
from app.server import dto
from .payload import UserCreatePayload
from litestar.exceptions import ValidationException


async def retrieve_user_handler(
    session: dict[str, Any],
    connection: ASGIConnection[Any, Any, Any, Any],
):
    db_session = alchemy.provide_session(connection.state, connection.scope)
    user = await db_session.get(m.User, session["user_id"])
    return user


def validation_exception(request: XRequest, exc: ValidationException) -> Template | Response:
    pprint(exc.extra)
    
    if request.htmx:
        ...
    return Response(
        media_type=MediaType.TEXT,
        content=exc.detail
    )
    # extra = exc.extra
    # if isinstance(extra, list):
    #     extra = extra[0]
    
    # if isinstance(extra, dict):
    #     return HTMXBlockTemplate(
    #         template_name="access.html.j2",
    #         block_name="exception",
    #         context={
    #             "extra": extra
    #         },
    #         re_target=f"#{extra['key']}",
    #         re_swap="afterend",
    #     )
    # return Response(
    #     media_type=MediaType.TEXT,
    #     content=exc.detail
    # )
    
    
    # if isinstance(exc.extra, dict):
    #     return HTMXBlockTemplate(
    #         block_name="exception",
    #         context={
    #             "exc": exc
    #         },
    #         re_target=f"#{exc.extra["key"]}",
    #         re_swap="afterend",
    #     )
    # return Response(
    #     media_type=MediaType.TEXT,
    #     content=exc.detail
    # )
    
    # if exc.extra:
    #     return request.template(
    #         "access.html.j2", 
    #         block_name="exception",
    #         context={
    #             "extra": exc.extra
    #         },
    #     )
    # return Response(
    #     media_type=MediaType.HTML,
    #     content=exc.detail,
    # )


class AccessController(Controller):
    
    exception_handlers = {
        ValidationException: validation_exception,
    } # type: ignore


    @get("/login")
    async def get_login(self, request: XRequest) -> Template:
        return request.template(
            "access.html.j2", push_url="/login", block_name="login"
        )

    @post("/login", dto=dto.UserLogin)
    async def post_login(
        self,
        data: URLEncoded[m.User],
        request: XRequest,
        users_service: UsersService,
    ) -> Template | Redirect:
        # user = await user_service.authenticate(data)
        # if user is None:
        #     return request.template("access.html.j2")
        return Redirect("/")

    @get("/signup")
    async def get_signup(self, request: XRequest) -> Template:
        return request.template(
            "access.html.j2", push_url="/signup", block_name="signup"
        )

    @post("/signup")
    async def post_signup(
        self,
        data: URLEncoded[UserCreatePayload],
        request: XRequest,
        users_service: UsersService,
    ) -> Template | Redirect:
        pprint(data)
        
        return request.template("access.html.j2", block_name="signup")
        
        # check url data to user
        
        
        # check if user exists
        # create user
        # redirect to login
        
        
        # if await user_service.exists(email=data.email):
        #     return request.template("access.html.j2")
        # user = await user_service.create(data, auto_commit=True)
        # return Redirect("/login")
