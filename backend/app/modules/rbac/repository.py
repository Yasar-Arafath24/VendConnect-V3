from sqlalchemy.orm import Session

from app.modules.rbac.model import Permission, Role


class RBACRepository:

    # ==========================
    # Role Operations
    # ==========================

    @staticmethod
    def create_role(db: Session, role: Role) -> Role:
        db.add(role)
        db.commit()
        db.refresh(role)
        return role

    @staticmethod
    def get_role_by_id(db: Session, role_id: str):
        return (
            db.query(Role)
            .filter(Role.id == role_id)
            .first()
        )

    @staticmethod
    def get_role_by_name(db: Session, role_name: str):
        return (
            db.query(Role)
            .filter(Role.name == role_name)
            .first()
        )

    @staticmethod
    def get_all_roles(db: Session):
        return (
            db.query(Role)
            .order_by(Role.name.asc())
            .all()
        )

    # ==========================
    # Permission Operations
    # ==========================

    @staticmethod
    def create_permission(
        db: Session,
        permission: Permission,
    ) -> Permission:

        db.add(permission)
        db.commit()
        db.refresh(permission)

        return permission

    @staticmethod
    def get_permission_by_key(
        db: Session,
        key: str,
    ):

        return (
            db.query(Permission)
            .filter(Permission.key == key)
            .first()
        )

    @staticmethod
    def get_all_permissions(db: Session):
        return (
            db.query(Permission)
            .order_by(Permission.resource.asc())
            .all()
        )

    # ==========================
    # Role-Permission
    # ==========================

    @staticmethod
    def assign_permission(
        db: Session,
        role: Role,
        permission: Permission,
    ):

        if permission not in role.permissions:
            role.permissions.append(permission)

            db.commit()

            db.refresh(role)

        return role