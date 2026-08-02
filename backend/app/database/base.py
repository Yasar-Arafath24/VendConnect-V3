from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


# Import all models here
from app.modules.organizations.model import Organization
from app.modules.rbac.model import Permission, Role
from app.modules.users.model import User  # noqa: F401
from app.modules.users.model import User