from heroicons.jinja import (
    heroicon_micro,
    heroicon_mini,
    heroicon_outline,
    heroicon_solid,
)
from jinja2 import Environment, FileSystemLoader
from litestar.config.compression import CompressionConfig
from litestar.contrib.jinja import JinjaTemplateEngine
from litestar.plugins.sqlalchemy import (
    AlembicAsyncConfig,
    AsyncSessionConfig,
    SQLAlchemyAsyncConfig,
    orm_registry,
)
from litestar.template import TemplateConfig

from .base import get_settings

settings = get_settings()

env = Environment(
    autoescape=True,
    loader=FileSystemLoader(settings.app.TEMPLATES_DIR),
)
env.globals.update(
    {
        "heroicon_micro": heroicon_micro,
        "heroicon_mini": heroicon_mini,
        "heroicon_outline": heroicon_outline,
        "heroicon_solid": heroicon_solid,
    }
)

template = TemplateConfig(
    instance=JinjaTemplateEngine.from_environment(env),
)

alembic = AlembicAsyncConfig(
    script_location=settings.db.MIGRATION_DIR,
    script_config=settings.db.MIGRATION_CONFIG,
)
alchemy = SQLAlchemyAsyncConfig(
    connection_string=settings.db.URL,
    alembic_config=alembic,
    session_config=AsyncSessionConfig(expire_on_commit=False),
    metadata=orm_registry.metadata,
)

compression = CompressionConfig(backend="brotli")
