from typing import Tuple
from advanced_alchemy.extensions.litestar import service, repository, providers
import bcrypt
from litestar.exceptions import NotAuthorizedException

from app.infrastructure.database import models as m
from app.domain.user import dto



class RoleService(service.SQLAlchemyAsyncRepositoryService[m.Role]):
    class Repository(repository.SQLAlchemyAsyncRepository[m.Role]):
        model_type = m.Role
        
    repository_type = Repository
    