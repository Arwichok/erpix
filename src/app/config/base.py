from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path
from typing import Any, Type

from environs import Env

BASE_DIR = Path(__file__).parent.parent.parent.parent
_env = Env()


def env(type: Type | str, name: str, default: Any = ..., **kwargs):
    return field(
        default_factory=lambda: getattr(
            _env, type if isinstance(type, str) else type.__name__
        )(name, default, **kwargs),
    )


@dataclass
class AppSettings:
    DEBUG: bool = env(bool, "DEBUG", False)
    PUBLIC_DIR: Path = BASE_DIR / "public"
    TEMPLATES_DIR: Path = BASE_DIR / "src/app/presentation/web/templates"


@dataclass
class DatabaseSettings:
    URL: str = env(str, "DATABASE_URL", "sqlite+aiosqlite:///db.sqlite3")
    ECHO: bool = env(bool, "DATABASE_ECHO", False)
    MIGRATION_DIR: str = str(BASE_DIR / "src/app/infrastructure/database/migrations")
    MIGRATION_CONFIG: str = str(BASE_DIR / "src/app/infrastructure/database/migrations/alembic.ini")


@dataclass
class Settings:
    app: AppSettings = field(default_factory=AppSettings)
    db: DatabaseSettings = field(default_factory=DatabaseSettings)


@lru_cache(maxsize=1, typed=True)
def get_settings() -> Settings:
    return Settings()
