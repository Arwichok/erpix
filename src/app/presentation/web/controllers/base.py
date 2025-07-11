from litestar import (
    Controller,
    get,
)
from litestar.response import Redirect, Template

from app.presentation.web.xrequest import XRequest



class BaseController(Controller):
    path = "/"

    @get("/", exclude_from_auth=True)
    async def index(self, request: XRequest) -> Redirect:
        return Redirect("/login")

    @get("/favicon.ico", exclude_from_auth=True)
    async def favicon(self, request: XRequest) -> Redirect:
        return Redirect("/static/favicon.ico")

    @get("/dashboard", exclude_from_auth=True)
    async def dashboard(self, request: XRequest) -> Template:
        return request.template("dashboard.html.j2")