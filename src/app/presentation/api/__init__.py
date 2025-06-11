from litestar import Router

from app.presentation.api.users import UsersAPIController




router = Router(
    path="/api",
    route_handlers=[
        UsersAPIController,
    ]
)