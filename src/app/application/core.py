from __future__ import annotations

from typing import TYPE_CHECKING

from litestar.plugins import InitPluginProtocol

if TYPE_CHECKING:
    from litestar.config.app import AppConfig


class ApplicationCore(InitPluginProtocol):
    def on_app_init(self, app_config: AppConfig) -> AppConfig:
        from litestar.middleware.session.server_side import (
            ServerSideSessionBackend,
            ServerSideSessionConfig,
        )
        from litestar.security.session_auth import SessionAuth
        from litestar.static_files import create_static_files_router

        from app.config import app as config
        from app.config.base import get_settings
        from app.infrastructure.database import models as m
        from app.presentation import api, web

        from . import handlers, plugins, lifespan

        settings = get_settings()

        session_auth = SessionAuth[m.User, ServerSideSessionBackend](
            retrieve_user_handler=handlers.retrieve_user_handler,
            session_backend_config=ServerSideSessionConfig(),
            exclude=["/login", "/signup", "/schema", "/static", "/__reload__"],
        )
        session_auth.on_app_init(app_config)

        app_config.debug = settings.app.DEBUG
        app_config.template_config = config.template
        app_config.compression_config = config.compression
        app_config.signature_namespace.update({"m": m})
        app_config.plugins.extend(
            [plugins.alchemy, plugins.reload, plugins.htmx]
        )
        app_config.lifespan.extend([lifespan.database_setup])
        app_config.route_handlers.extend(
            [
                create_static_files_router(
                    path="/static", directories=[settings.app.PUBLIC_DIR]
                ),
                web.router,
                api.router,
            ]
        )

        return app_config
