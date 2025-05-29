from typing import Tuple
from advanced_alchemy.extensions.litestar import (
    service,
    repository,
    providers
)

from app.lib.wrong import Wrong

from . import models as m


class UsersService(service.SQLAlchemyAsyncRepositoryService[m.User]):
    
    class Repository(repository.SQLAlchemyAsyncRepository[m.User]):
        model_type = m.User
        
    repository_type = Repository


    async def signup(self, data: m.User) -> Tuple[m.User|None, Wrong]:
        wrong = Wrong()
        user: m.User | None = None
        
        
        
        
        