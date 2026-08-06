from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


# Register all models with Base.metadata
from app.modules.organizations.model import Organization  # noqa: E402, F401
from app.modules.rbac.model import Permission, Role  # noqa: E402, F401
from app.modules.users.model import User  # noqa: E402, F401
from app.modules.auth.model import RefreshToken  # noqa: E402, F401
from app.modules.products.model import Product  # noqa: E402, F401
from app.modules.categories.model import Category  # noqa: E402, F401
from app.modules.brands.model import Brand  # noqa: E402, F401
from app.modules.units.model import Unit  # noqa: E402, F401
