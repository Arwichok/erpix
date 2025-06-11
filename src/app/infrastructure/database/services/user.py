from typing import Tuple
from advanced_alchemy.extensions.litestar import service, repository, providers
import bcrypt
from litestar.exceptions import NotAuthorizedException

from app.infrastructure.database import models as m
from app.domain.user import dto


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode(
        "utf-8"
    )


def check_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        password.encode("utf-8"), hashed_password.encode("utf-8")
    )


class UserService(service.SQLAlchemyAsyncRepositoryService[m.User]):
    class Repository(repository.SQLAlchemyAsyncRepository[m.User]):
        model_type = m.User

    repository_type = Repository
    
    @staticmethod
    def hash_password(password: str) -> str:
        return hash_password(password)

    @staticmethod
    def check_password(password: str, hashed_password: str) -> bool:
        return check_password(password, hashed_password)

    async def signup(self, payload: dto.UserPayload) -> m.User:
        return await super().create(
            m.User(
                email=payload.email,
                password=hash_password(payload.password),
                role_id=(await self.get_one(name="guest")).id,
            ),
            auto_commit=True,
        )

    async def authenticate(
        self, payload: dto.UserPayload
    ) -> m.User:
        user = await self.get_one(email=payload.email)
        if check_password(payload.password, user.password):
            return user
        
        raise NotAuthorizedException
