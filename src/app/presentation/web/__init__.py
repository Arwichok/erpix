from litestar import Router

from app.presentation.web.base import BaseController
from app.presentation.web.controllers.access import AccessController
from app.presentation.web.controllers.users import UsersController
from app.presentation.web.xrequest import XRequest


router = Router(
    path="/",
    request_class=XRequest,
    route_handlers=[
        AccessController,
        BaseController,
        UsersController,
    ]
)