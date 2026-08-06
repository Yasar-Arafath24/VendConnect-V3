from sqlalchemy import func
from sqlalchemy.orm import Session

from app.modules.units.model import Unit


class UnitRepository:

    @staticmethod
    def create(
        db: Session,
        unit: Unit,
    ) -> Unit:

        db.add(unit)
        db.commit()
        db.refresh(unit)

        return unit

    @staticmethod
    def get_by_id(
        db: Session,
        unit_id: str,
    ):

        return (
            db.query(Unit)
            .filter(Unit.id == unit_id)
            .first()
        )

    @staticmethod
    def get_by_name(
        db: Session,
        organization_id: str,
        name: str,
    ):

        return (
            db.query(Unit)
            .filter(
                Unit.organization_id == organization_id,
                func.lower(Unit.name) == name.lower(),
            )
            .first()
        )

    @staticmethod
    def get_by_symbol(
        db: Session,
        organization_id: str,
        symbol: str,
    ):

        return (
            db.query(Unit)
            .filter(
                Unit.organization_id == organization_id,
                func.lower(Unit.symbol) == symbol.lower(),
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
            db.query(Unit)
            .filter(
                Unit.organization_id == organization_id
            )
            .order_by(Unit.name.asc())
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
            db.query(Unit)
            .filter(
                Unit.organization_id == organization_id
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
            db.query(Unit)
            .filter(
                Unit.organization_id == organization_id,
                Unit.name.ilike(f"%{keyword}%"),
            )
            .order_by(Unit.name.asc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    @staticmethod
    def update(
        db: Session,
        unit: Unit,
    ) -> Unit:

        db.commit()
        db.refresh(unit)

        return unit

    @staticmethod
    def delete(
        db: Session,
        unit: Unit,
    ):

        db.delete(unit)
        db.commit()
