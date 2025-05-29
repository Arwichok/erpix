from __future__ import annotations

from typing import TYPE_CHECKING, Any

from jinja2_fragments.litestar import HTMXBlockTemplate
from litestar.plugins.htmx import HTMXRequest
from litestar.status_codes import HTTP_200_OK

if TYPE_CHECKING:
    from litestar_htmx.types import (
        EventAfterType,
        PushUrlType,
        ReSwapMethod,
    )
    from litestar.enums import MediaType
    from litestar.response import Template
    from litestar.background_tasks import BackgroundTask, BackgroundTasks
    from litestar.types import ResponseCookies


class XRequest(HTMXRequest):
    def template(
        self,
        template_name: str | None = None,
        *,
        template_str: str | None = None,
        background: BackgroundTask | BackgroundTasks | None = None,
        context: dict[str, Any] | None = None,
        cookies: ResponseCookies | None = None,
        encoding: str = "utf-8",
        headers: dict[str, Any] | None = None,
        media_type: MediaType | str | None = None,
        status_code: int = HTTP_200_OK,
        push_url: PushUrlType | None = None,
        re_swap: ReSwapMethod | None = None,
        re_target: str | None = None,
        trigger_event: str | None = None,
        params: dict[str, Any] | None = None,
        after: EventAfterType | None = None,
        block_name: str | None = None,
        block_names: list[str] | None = None,
        **kwargs,
    ) -> Template:
        if context is None:
            context = {}
        if not self.htmx:
            block_name = None
            block_names = None
        return HTMXBlockTemplate(
            push_url=push_url,
            re_swap=re_swap,
            re_target=re_target,
            trigger_event=trigger_event,
            params=params,
            after=after,
            block_name=block_name,
            block_names=block_names,
            template_name=template_name,
            template_str=template_str,
            context=context,
            cookies=cookies,
            encoding=encoding,
            headers=headers,
            media_type=media_type,
            status_code=status_code,
            background=background,
            **kwargs,
        )
