from dataclasses import dataclass

from app.domain.values.email import Email
from app.domain.values.hashed_password import HashedPassword



@dataclass
class User:
    email: Email
    password: HashedPassword
    is_active: bool
