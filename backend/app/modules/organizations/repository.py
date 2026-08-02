from sqlalchemy.orm import Session

from app.modules.organizations.model import Organization


class OrganizationRepository:

    @staticmethod
    def create(db: Session, organization: Organization) -> Organization:
        db.add(organization)
        db.commit()
        db.refresh(organization)
        return organization

    @staticmethod
    def get_by_id(db: Session, organization_id: str):
        return (
            db.query(Organization)
            .filter(Organization.id == organization_id)
            .first()
        )

    @staticmethod
    def get_by_email(db: Session, email: str):
        return (
            db.query(Organization)
            .filter(Organization.email == email)
            .first()
        )

    @staticmethod
    def get_by_code(db: Session, code: str):
        return (
            db.query(Organization)
            .filter(Organization.organization_code == code)
            .first()
        )

    @staticmethod
    def get_all(db: Session):
        return (
            db.query(Organization)
            .order_by(Organization.created_at.desc())
            .all()
        )

    @staticmethod
    def update(db: Session, organization: Organization):
        db.commit()
        db.refresh(organization)
        return organization

    @staticmethod
    def delete(db: Session, organization: Organization):
        db.delete(organization)
        db.commit()