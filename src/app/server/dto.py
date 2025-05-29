from litestar.plugins.sqlalchemy import SQLAlchemyDTO, SQLAlchemyDTOConfig

from app.database import models as m



class UserCreate(SQLAlchemyDTO[m.User]):
    config = SQLAlchemyDTOConfig(
        include={
            "name",
            "email",
            "password",
        }
    )

class UserLogin(SQLAlchemyDTO[m.User]):
    config = SQLAlchemyDTOConfig(
        include={
            "email",
            "password",
        }
    )