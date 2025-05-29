from litestar import (
    Controller,
    get,
)
from litestar.response import Template

from app.lib.xrequest import XRequest


class BaseController(Controller):
    path = "/"

    @get("/", exclude_from_auth=True)
    async def index(self, request: XRequest) -> Template:
        return request.template("index.html.j2")
