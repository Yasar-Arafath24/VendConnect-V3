from sqlalchemy.orm import Session

from app.modules.rbac.model import Permission, Role
from app.modules.rbac.repository import RBACRepository


class RBACService:

    # =====================================
    # ROLE SERVICES
    # =====================================

    @staticmethod
    def create_role(
        db: Session,
        name: str,
        description: str | None = None,
        organization_id: str | None = None,
        is_system: bool = False,
    ) -> Role:

        existing = RBACRepository.get_role_by_name(db, name)

        if existing:
            raise ValueError("Role already exists.")

        role = Role(
            name=name,
            description=description,
            organization_id=organization_id,
            is_system=is_system,
        )

        return RBACRepository.create_role(db, role)

    @staticmethod
    def get_roles(db: Session):
        return RBACRepository.get_all_roles(db)

    # =====================================
    # PERMISSION SERVICES
    # =====================================

    @staticmethod
    def create_permission(
        db: Session,
        key: str,
        resource: str,
        action: str,
        description: str | None = None,
    ) -> Permission:

        existing = RBACRepository.get_permission_by_key(db, key)

        if existing:
            raise ValueError("Permission already exists.")

        permission = Permission(
            key=key,
            resource=resource,
            action=action,
            description=description,
        )

        return RBACRepository.create_permission(db, permission)

    @staticmethod
    def get_permissions(db: Session):
        return RBACRepository.get_all_permissions(db)

    # =====================================
    # ROLE → PERMISSION
    # =====================================

    @staticmethod
    def assign_permission(
        db: Session,
        role_name: str,
        permission_key: str,
    ):

        role = RBACRepository.get_role_by_name(db, role_name)

        if role is None:
            raise ValueError("Role not found.")

        permission = RBACRepository.get_permission_by_key(
            db,
            permission_key,
        )

        if permission is None:
            raise ValueError("Permission not found.")

        return RBACRepository.assign_permission(
            db,
            role,
            permission,
        )