from typing import Annotated, TypeVar

from litestar.enums import RequestEncodingType
from litestar.params import Body


T = TypeVar("T")
URLEncoded = Annotated[T, Body(media_type=RequestEncodingType.URL_ENCODED)]
