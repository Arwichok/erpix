from dataclasses import dataclass, field
from typing import Annotated, Any, TypeVar

from litestar.enums import RequestEncodingType
from litestar.params import Body


T = TypeVar("T")
URLEncoded = Annotated[T, Body(media_type=RequestEncodingType.URL_ENCODED)]

@dataclass
class FormField[T]:
    value: T | None = None
    error: Exception | None = None


@dataclass
class Form:
    email: FormField[str] = field(default_factory=FormField[str])
    password: FormField[str] = field(default_factory=FormField[str])
