from litestar.plugins.htmx import HTMXPlugin
from litestar.plugins.sqlalchemy import SQLAlchemyInitPlugin
from litestar_browser_reload import BrowserReloadPlugin
from watchfiles import DefaultFilter

from app.config.base import get_settings
from app.config import app as config

settings = get_settings()


alchemy = SQLAlchemyInitPlugin(config=config.alchemy)
htmx = HTMXPlugin()
reload = BrowserReloadPlugin(
    watch_paths=(
        settings.app.TEMPLATES_DIR,
        settings.app.PUBLIC_DIR,
    ),
    watch_filter=DefaultFilter(ignore_dirs=(".git", ".hg", ".svn", ".tox")),
)
