from sqlalchemy import func
from sqlalchemy.orm import Session

from app.modules.brands.model import Brand


class BrandRepository:

    @staticmethod
    def create(
        db: Session,
        brand: Brand,
    ) -> Brand:

        db.add(brand)
        db.commit()
        db.refresh(brand)

        return brand

    @staticmethod
    def get_by_id(
        db: Session,
        brand_id: str,
    ):

        return (
            db.query(Brand)
            .filter(Brand.id == brand_id)
            .first()
        )

    @staticmethod
    def get_by_name(
        db: Session,
        organization_id: str,
        name: str,
    ):

        return (
            db.query(Brand)
            .filter(
                Brand.organization_id == organization_id,
                func.lower(Brand.name) == name.lower(),
            )
            .first()
        )

    @staticmethod
    def get_all(
        db: Session,
        organization_id: str,
        skip: int = 0,
        limit: int = 20,
    ):

        return (
            db.query(Brand)
            .filter(
                Brand.organization_id == organization_id
            )
            .order_by(Brand.name.asc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    @staticmethod
    def count(
        db: Session,
        organization_id: str,
    ):

        return (
            db.query(Brand)
            .filter(
                Brand.organization_id == organization_id
            )
            .count()
        )

    @staticmethod
    def search(
        db: Session,
        organization_id: str,
        keyword: str,
        skip: int = 0,
        limit: int = 20,
    ):

        return (
            db.query(Brand)
            .filter(
                Brand.organization_id == organization_id,
                Brand.name.ilike(f"%{keyword}%"),
            )
            .order_by(Brand.name.asc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    @staticmethod
    def update(
        db: Session,
        brand: Brand,
    ) -> Brand:

        db.commit()
        db.refresh(brand)

        return brand

    @staticmethod
    def delete(
        db: Session,
        brand: Brand,
    ):

        db.delete(brand)
        db.commit()