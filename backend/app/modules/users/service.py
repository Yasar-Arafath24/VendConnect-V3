from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.modules.organizations.repository import OrganizationRepository
from app.modules.users.model import User
from app.modules.users.repository import UserRepository
from app.modules.users.schema import UserCreate


class UserService:

    @staticmethod
    def create_user(
        db: Session,
        user_data: UserCreate,
    ) -> User:

        organization = OrganizationRepository.get_by_id(
            db,
            user_data.organization_id,
        )

        if organization is None:
            raise ValueError("Organization not found.")

        existing = UserRepository.get_by_email(
            db,
            user_data.email,
        )

        if existing:
            raise ValueError("User with this email already exists.")

        user = User(
            organization_id=user_data.organization_id,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            email=user_data.email,
            phone=user_data.phone,
            password_hash=hash_password(user_data.password),
            profile_image=user_data.profile_image,
        )

        return UserRepository.create(db, user)

    @staticmethod
    def get_user(
        db: Session,
        user_id: str,
    ):
        return UserRepository.get_by_id(db, user_id)

    @staticmethod
    def list_users(db: Session):
        return UserRepository.get_all(db)

    @staticmethod
    def get_users_by_organization(
        db: Session,
        organization_id: str,
    ):
        return UserRepository.get_by_organization(
            db,
            organization_id,
        )
