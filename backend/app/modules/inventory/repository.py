from sqlalchemy import and_, func
from sqlalchemy.orm import Session

from app.modules.inventory.model import Inventory


class InventoryRepository:

    @staticmethod
    def create(
        db: Session,
        inventory: Inventory,
        commit: bool = True,
    ) -> Inventory:

        db.add(inventory)

        if commit:
            db.commit()
            db.refresh(inventory)

        return inventory

    @staticmethod
    def get_by_id(
        db: Session,
        inventory_id: str,
    ):

        return (
            db.query(Inventory)
            .filter(
                Inventory.id == inventory_id
            )
            .first()
        )

    @staticmethod
    def get_by_product_and_warehouse(
        db: Session,
        organization_id: str,
        product_id: str,
        warehouse_id: str,
    ):

        return (
            db.query(Inventory)
            .filter(
                and_(
                    Inventory.organization_id == organization_id,
                    Inventory.product_id == product_id,
                    Inventory.warehouse_id == warehouse_id,
                )
            )
            .first()
        )

    @staticmethod
    def get_by_product(
        db: Session,
        organization_id: str,
        product_id: str,
    ):

        return (
            db.query(Inventory)
            .filter(
                Inventory.organization_id == organization_id,
                Inventory.product_id == product_id,
            )
            .all()
        )

    @staticmethod
    def get_by_warehouse(
        db: Session,
        organization_id: str,
        warehouse_id: str,
    ):

        return (
            db.query(Inventory)
            .filter(
                Inventory.organization_id == organization_id,
                Inventory.warehouse_id == warehouse_id,
            )
            .all()
        )

    @staticmethod
    def get_all(
        db: Session,
        organization_id: str,
        warehouse_id: str | None = None,
        product_id: str | None = None,
        skip: int = 0,
        limit: int = 20,
    ):

        query = db.query(Inventory).filter(
            Inventory.organization_id == organization_id
        )

        if warehouse_id:
            query = query.filter(
                Inventory.warehouse_id == warehouse_id
            )

        if product_id:
            query = query.filter(
                Inventory.product_id == product_id
            )

        return (
            query.order_by(Inventory.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    @staticmethod
    def count(
        db: Session,
        organization_id: str,
        warehouse_id: str | None = None,
        product_id: str | None = None,
    ) -> int:

        query = db.query(func.count(Inventory.id)).filter(
            Inventory.organization_id == organization_id
        )

        if warehouse_id:
            query = query.filter(
                Inventory.warehouse_id == warehouse_id
            )

        if product_id:
            query = query.filter(
                Inventory.product_id == product_id
            )

        return query.scalar() or 0

    @staticmethod
    def get_low_stock(
        db: Session,
        organization_id: str,
    ):

        records = (
            db.query(Inventory)
            .filter(
                Inventory.organization_id == organization_id
            )
            .all()
        )

        return [
            item
            for item in records
            if item.available_quantity <= item.reorder_level
        ]

    @staticmethod
    def update(
        db: Session,
        inventory: Inventory,
        commit: bool = True,
    ) -> Inventory:

        if commit:
            db.commit()
            db.refresh(inventory)

        return inventory

    @staticmethod
    def delete(
        db: Session,
        inventory: Inventory,
        commit: bool = True,
    ):

        db.delete(inventory)

        if commit:
            db.commit()