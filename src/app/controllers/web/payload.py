from dataclasses import dataclass
from app.lib.wrong import Wrong


@dataclass
class UserCreatePayload:
    name: str | None = None
    email: str | None = None
    password: str | None = None

    def wrong(self) -> Wrong:
        _wrong = Wrong()
        if not self.name:
            _wrong.name = True

        return _wrong