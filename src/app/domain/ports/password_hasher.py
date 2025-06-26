from abc import abstractmethod
from typing import Protocol

from app.domain.values.raw_password import RawPassword
from app.domain.values.hashed_password import HashedPassword


class PasswordHasher(Protocol):

    @abstractmethod
    def hash(self, raw_password: RawPassword) -> HashedPassword:
        ...

    @abstractmethod
    def check(self, raw_password: RawPassword, hashed_password: HashedPassword) -> bool:
        ...
