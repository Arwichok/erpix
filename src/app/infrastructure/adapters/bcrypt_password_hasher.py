import bcrypt

from app.domain.ports.password_hasher import PasswordHasher
from app.domain.values.hashed_password import HashedPassword
from app.domain.values.raw_password import RawPassword



class BcryptPasswordHasher(PasswordHasher):
    def hash(self, raw_password: RawPassword) -> HashedPassword:
        return bcrypt.hashpw(raw_password.encode(), bcrypt.gensalt())

    def check(self, raw_password: RawPassword, hashed_password: HashedPassword) -> bool:
        return bcrypt.checkpw(raw_password.encode(), hashed_password)
