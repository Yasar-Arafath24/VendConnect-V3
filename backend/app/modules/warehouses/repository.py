from sqlalchemy import func, or_
from sqlalchemy.orm import Session

from app.modules.warehouses.model import Warehouse


class WarehouseRepository:

    @staticmethod
    def create(
        db: Session,
        warehouse: Warehouse,
    ) -> Warehouse:

        db.add(warehouse)
        db.commit()
        db.refresh(warehouse)

        return warehouse

    @staticmethod
    def get_by_id(
        db: Session,
        warehouse_id: str,
    ):

        return (
            db.query(Warehouse)
            .filter(
                Warehouse.id == warehouse_id
            )
            .first()
        )

    @staticmethod
    def get_by_name(
        db: Session,
        organization_id: str,
        name: str,
    ):

        return (
            db.query(Warehouse)
            .filter(
                Warehouse.organization_id == organization_id,
                func.lower(Warehouse.name) == name.lower(),
            )
            .first()
        )

    @staticmethod
    def get_by_code(
        db: Session,
        organization_id: str,
        code: str,
    ):

        return (
            db.query(Warehouse)
            .filter(
                Warehouse.organization_id == organization_id,
                func.lower(Warehouse.code) == code.lower(),
            )
            .first()
        )

    @staticmethod
    def get_default(
        db: Session,
        organization_id: str,
    ):

        return (
            db.query(Warehouse)
            .filter(
                Warehouse.organization_id == organization_id,
                Warehouse.is_default == True,
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
            db.query(Warehouse)
            .filter(
                Warehouse.organization_id == organization_id
            )
            .order_by(Warehouse.name.asc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    @staticmethod
    def count(
        db: Session,
        organization_id: str,
    ) -> int:

        return (
            db.query(Warehouse)
            .filter(
                Warehouse.organization_id == organization_id
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
            db.query(Warehouse)
            .filter(
                Warehouse.organization_id == organization_id,
                or_(
                    Warehouse.name.ilike(f"%{keyword}%"),
                    Warehouse.code.ilike(f"%{keyword}%"),
                ),
            )
            .order_by(Warehouse.name.asc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    @staticmethod
    def update(
        db: Session,
        warehouse: Warehouse,
    ) -> Warehouse:

        db.commit()
        db.refresh(warehouse)

        return warehouse

    @staticmethod
    def delete(
        db: Session,
        warehouse: Warehouse,
    ):

        db.delete(warehouse)
        db.commit()