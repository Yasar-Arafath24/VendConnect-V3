from uuid import uuid4

from sqlalchemy.orm import Session

from app.modules.products.model import Product


class ProductRepository:

    @staticmethod
    def create(
        db: Session,
        product: Product,
    ) -> Product:

        db.add(product)
        db.commit()
        db.refresh(product)

        return product

    @staticmethod
    def get_by_id(
        db: Session,
        product_id: str,
    ):

        return (
            db.query(Product)
            .filter(Product.id == product_id)
            .first()
        )

    @staticmethod
    def get_by_sku(
        db: Session,
        sku: str,
    ):

        return (
            db.query(Product)
            .filter(Product.sku == sku)
            .first()
        )

    @staticmethod
    def get_all(
        db: Session,
    ):

        return (
            db.query(Product)
            .order_by(Product.created_at.desc())
            .all()
        )

    @staticmethod
    def update(
        db: Session,
        product: Product,
    ):

        db.commit()
        db.refresh(product)

        return product

    @staticmethod
    def delete(
        db: Session,
        product: Product,
    ):

        db.delete(product)
        db.commit()