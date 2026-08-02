from sqlalchemy.orm import relationship

from app.database.base import Base
from app.modules.users.model import user_roles


class UserRole(Base):
    """ORM mapping over the user_roles association table."""

    __table__ = user_roles

    user = relationship("User", viewonly=True)

    role = relationship("Role", viewonly=True)
