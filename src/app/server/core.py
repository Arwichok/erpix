from __future__ import annotations


from typing import TYPE_CHECKING

from litestar.middleware.session.server_side import ServerSideSessionBackend, ServerSideSessionConfig
from litestar.plugins import InitPluginProtocol
from litestar.security.session_auth import SessionAuth

if TYPE_CHECKING:
    from litestar.config.app import AppConfig


class ApplicationCore(InitPluginProtocol):
    
    def on_app_init(self, app_config: AppConfig) -> AppConfig:
        from app.config import app as config
        from app.server import plugins
        from app.config.base import get_settings
        from app.controllers.web.base import BaseController
        from app.controllers.web.access import AccessController, retrieve_user_handler
        from app.lib.xrequest import XRequest
        from app.database import models as m
        from app.database import services as s
        from app.server import lifespan
        from litestar.static_files import create_static_files_router
        from advanced_alchemy.extensions.litestar.providers import create_service_dependencies
        
        settings = get_settings()
        
        session_auth = SessionAuth[m.User, ServerSideSessionBackend](
            retrieve_user_handler=retrieve_user_handler,
            session_backend_config=ServerSideSessionConfig(),
            exclude=["/login", "/signup", "/schema", "/static", "/__reload__"],
        )
        session_auth.on_app_init(app_config)
        
        app_config.lifespan.extend([
            lifespan.on_startup
        ])

        app_config.debug = settings.app.DEBUG
        app_config.request_class = XRequest
        app_config.template_config = config.template
        app_config.compression_config = config.compression
        app_config.plugins.extend(
            [plugins.alchemy, plugins.reload, plugins.htmx]
        )
        app_config.dependencies.update({
            **create_service_dependencies(s.UsersService, "users_service"),
        })
        app_config.route_handlers.extend(
            [
                create_static_files_router(
                    path="/static", directories=[settings.app.PUBLIC_DIR]
                ),
                BaseController,
                AccessController,
            ]
        )
        app_config
        app_config.signature_namespace.update({"m": m})

        return app_config
