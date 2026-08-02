from sqlalchemy.orm import Session

from app.modules.rbac.service import RBACService

DEFAULT_PERMISSIONS = [
    ("product:create", "product", "create"),
    ("product:update", "product", "update"),
    ("product:delete", "product", "delete"),
    ("product:view", "product", "view"),

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