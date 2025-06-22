from advanced_alchemy.extensions.litestar import service, repository
from litestar.exceptions import NotAuthorizedException

from app.infrastructure.database import models as m
from app.domain.access.schemas import UserPayload
from app.domain.access.crypt import hash_password, check_password


class UserService(service.SQLAlchemyAsyncRepositoryService[m.User]):
    class Repository(repository.SQLAlchemyAsyncRepository[m.User]):
        model_type = m.User

    repository_type = Repository
    
    async def signup(self, payload: UserPayload) -> m.User:
        return await super().create(
            dict(
                email=payload.email,
                password=hash_password(payload.password),
            ),
            auto_commit=True,
        )

    async def authenticate(
        self, payload: UserPayload
    ) -> m.User:
        user = await self.get_one(email=payload.email)
        if check_password(payload.password, user.password):
            return user
        
        raise NotAuthorizedException
