from pprint import pprint
from typing import Any

from litestar import Controller, get, post
from litestar.connection import ASGIConnection
from litestar.response import Redirect, Template

from app.config.app import alchemy
from app.database import models as m
from app.database.services import UsersService
from app.lib.types import URLEncoded
from app.lib.xrequest import XRequest
from app.server import dto
from .payload import UserCreatePayload


async def retrieve_user_handler(
    session: dict[str, Any],
    connection: ASGIConnection[Any, Any, Any, Any],
):
    db_session = alchemy.provide_session(connection.state, connection.scope)
    user = await db_session.get(m.User, session["user_id"])
    return user


class AccessController(Controller):
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

    @post("/signup", dto=dto.UserCreate)
    async def post_signup(
        self,
        data: URLEncoded[m.User],
        request: XRequest,
        users_service: UsersService,
    ) -> Template | Redirect:
        
        return request.template("access.html.j2", block_name="signup")
        
        # check url data to user
        
        
        # check if user exists
        # create user
        # redirect to login
        
        
        # if await user_service.exists(email=data.email):
        #     return request.template("access.html.j2")
        # user = await user_service.create(data, auto_commit=True)
        # return Redirect("/login")
