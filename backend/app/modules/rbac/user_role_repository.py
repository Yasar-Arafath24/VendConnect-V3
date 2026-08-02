from sqlalchemy.orm import Session

from app.modules.rbac.model_user_role import UserRole


class UserRoleRepository:

    @staticmethod
    def assign_role(
        db: Session,
        user_id: str,
        role_id: str,
    ) -> UserRole:

        existing = (
            db.query(UserRole)
            .filter(
                UserRole.user_id == user_id,
                UserRole.role_id == role_id,
            )
            .first()
        )

        if existing:
            return existing

        user_role = UserRole(
            user_id=user_id,
            role_id=role_id,
        )

        db.add(user_role)
        db.commit()
        db.refresh(user_role)

        return user_role

    @staticmethod
    def get_roles_by_user(
        db: Session,
        user_id: str,
    ) -> list[UserRole]:

        return (
            db.query(UserRole)
            .filter(UserRole.user_id == user_id)
            .all()
        )

    @staticmethod
    def remove_role(
        db: Session,
        user_id: str,
        role_id: str,
    ) -> bool:

        record = (
            db.query(UserRole)
            .filter(
                UserRole.user_id == user_id,
                UserRole.role_id == role_id,
            )
            .first()
        )

        if record is None:
            return False

        db.delete(record)
        db.commit()

        return True