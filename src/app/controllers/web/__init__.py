from litestar import Router

from app.lib.xrequest import XRequest


base_router = Router(
    path="/",
    request_class=XRequest,
    route_handlers=[
        
    ]
)