from abc import abstractmethod
from typing import Protocol

from app.domain.entities.user import User
from app.domain.values.email import Email
from app.domain.values.raw_password import RawPassword


class UserService(Protocol):

    @abstractmethod
    def authenticate(self, email: Email, raw_password: RawPassword) -> User:
        ...
    
    @abstractmethod
    def signup(self, email: Email, raw_password: RawPassword) -> User:
        ...
