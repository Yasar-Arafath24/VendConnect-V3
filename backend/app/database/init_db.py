from app.database.base import Base
from app.database.database import engine

# Import all models so they register with Base.metadata
from app.modules.organizations import model  # noqa: F401
from app.modules.rbac import model  # noqa: F401
from app.modules.users import model  # noqa: F401
from app.modules.products import model  # noqa: F401


def init_db() -> None:
    """Create all tables that don't yet exist in the database."""
    Base.metadata.create_all(bind=engine)
