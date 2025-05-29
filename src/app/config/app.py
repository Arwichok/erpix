from litestar.config.compression import CompressionConfig
from litestar.plugins.sqlalchemy import (
    AlembicAsyncConfig,
    AsyncSessionConfig,
    SQLAlchemyAsyncConfig,
)
from litestar.template import TemplateConfig
from litestar.contrib.jinja import JinjaTemplateEngine
from .base import get_settings


settings = get_settings()


template = TemplateConfig(
    directory=settings.app.TEMPLATES_DIR, engine=JinjaTemplateEngine
)

alembic = AlembicAsyncConfig(
    script_location=settings.db.MIGRATION_DIR,
    script_config=settings.db.MIGRATION_CONFIG,
)
alchemy = SQLAlchemyAsyncConfig(
    connection_string=settings.db.url,
    alembic_config=alembic,
    session_config=AsyncSessionConfig(expire_on_commit=False),
    create_all=settings.app.DEBUG,
)

compression = CompressionConfig(backend="brotli")
