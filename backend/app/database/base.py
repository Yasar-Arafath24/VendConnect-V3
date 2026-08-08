from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


# Import all models here (ORDER MATTERS: users must load before rbac,
# because rbac/model.py imports the `user_roles` table from users.model)
from app.modules.organizations.model import Organization  # noqa: E402, F401
from app.modules.users.model import User  # noqa: E402, F401
from app.modules.auth.model import RefreshToken  # noqa: E402, F401
from app.modules.rbac.model import Permission, Role  # noqa: E402, F401
from app.modules.products.model import Product  # noqa: E402, F401
from app.modules.categories.model import Category  # noqa: E402, F401
from app.modules.brands.model import Brand  # noqa: E402, F401
from app.modules.units.model import Unit  # noqa: E402, F401
from app.modules.warehouses.model import Warehouse  # noqa: E402, F401
from app.modules.inventory.model import Inventory  # noqa: E402, F401
from app.modules.inventory.movement_model import InventoryMovement  # noqa: E402, F401
