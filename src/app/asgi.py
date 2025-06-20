from __future__ import annotations


from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from litestar import Litestar


def create_app() -> Litestar:
    from litestar import Litestar
    from app.application.core import ApplicationCore

    return Litestar(plugins=[ApplicationCore()])
