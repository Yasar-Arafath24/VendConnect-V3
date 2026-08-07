from sqlalchemy.orm import Session

# Import Base first so all models register with metadata
# (base.py imports every model module itself)
from app.database.base import Base  # noqa: F401

from app.modules.rbac.model import Permission, Role
from app.modules.rbac.repository import RBACRepository

DEFAULT_PERMISSIONS = [
    ("product:create", "product", "create"),
    ("product:update", "product", "update"),
    ("product:delete", "product", "delete"),
    ("product:view", "product", "view"),

    ("brand:create", "brand", "create"),
    ("brand:update", "brand", "update"),
    ("brand:delete", "brand", "delete"),
    ("brand:view", "brand", "view"),

    ("category:create", "category", "create"),
    ("category:update", "category", "update"),
    ("category:delete", "category", "delete"),
    ("category:view", "category", "view"),

    ("unit:create", "unit", "create"),
    ("unit:update", "unit", "update"),
    ("unit:delete", "unit", "delete"),
    ("unit:view", "unit", "view"),

    ("warehouse:create", "warehouse", "create"),
    ("warehouse:update", "warehouse", "update"),
    ("warehouse:delete", "warehouse", "delete"),
    ("warehouse:view", "warehouse", "view"),

    ("inventory:view", "inventory", "view"),
    ("inventory:update", "inventory", "update"),

    ("order:create", "order", "create"),
    ("order:update", "order", "update"),
    ("order:view", "order", "view"),

    ("analytics:view", "analytics", "view"),

    ("user:create", "user", "create"),
    ("user:update", "user", "update"),
    ("user:view", "user", "view"),
]


def seed_default_permissions(db: Session):
    """Create any missing default permissions. Idempotent."""

    created = []

    for key, resource, action in DEFAULT_PERMISSIONS:

        existing = RBACRepository.get_permission_by_key(
            db,
            key,
        )

        if existing:
            continue

        permission = Permission(
            key=key,
            resource=resource,
            action=action,
        )

        db.add(permission)
        created.append(permission)

    if created:
        db.commit()

        for permission in created:
            db.refresh(permission)

    return created


def seed_system_roles(db: Session):
    """Grant every default permission to all system roles. Idempotent."""

    permissions = db.query(Permission).all()
    roles = (
        db.query(Role)
        .filter(Role.is_system.is_(True))
        .all()
    )

    changed = False

    for role in roles:
        for permission in permissions:
            if permission not in role.permissions:
                role.permissions.append(permission)
                changed = True

    if changed:
        db.commit()
