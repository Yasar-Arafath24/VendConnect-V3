from sqlalchemy.orm import Session

from app.modules.users.model import User


class UserRepository:

    @staticmethod
    def create(db: Session, user: User) -> User:
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def get_by_id(db: Session, user_id: str):
        return (
            db.query(User)
            .filter(User.id == user_id)
            .first()
        )

    @staticmethod
    def get_by_email(db: Session, email: str):
        return (
            db.query(User)
            .filter(User.email == email)
            .first()
        )

    @staticmethod
    def get_all(db: Session):
        return (
            db.query(User)
            .order_by(User.created_at.desc())
            .all()
        )

    @staticmethod
    def get_by_organization(db: Session, organization_id: str):
        return (
            db.query(User)
            .filter(User.organization_id == organization_id)
            .order_by(User.created_at.desc())
            .all()
        )
