from sqlalchemy.orm import Session

from app.modules.users.repository import UserRepository
from app.modules.rbac.repository import RBACRepository
from app.modules.rbac.user_role_repository import UserRoleRepository


class UserRoleService:

    @staticmethod
    def assign_role(
        db: Session,
        user_id: str,
        role_id: str,
    ):

        # Check user exists
        user = UserRepository.get_by_id(
            db,
            user_id,
        )

        if user is None:
            raise ValueError("User not found.")

        # Check role exists
        role = RBACRepository.get_role_by_id(
            db,
            role_id,
        )

        if role is None:
            raise ValueError("Role not found.")

        return UserRoleRepository.assign_role(
            db,
            user_id,
            role_id,
        )

    @staticmethod
    def get_roles(
        db: Session,
        user_id: str,
    ):

        return UserRoleRepository.get_roles_by_user(
            db,
            user_id,
        )

    @staticmethod
    def remove_role(
        db: Session,
        user_id: str,
        role_id: str,
    ):

        return UserRoleRepository.remove_role(
            db,
            user_id,
            role_id,
        )