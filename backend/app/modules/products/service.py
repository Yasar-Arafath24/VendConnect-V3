from uuid import uuid4

from sqlalchemy.orm import Session

from app.modules.organizations.repository import OrganizationRepository
from app.modules.products.model import Product
from app.modules.products.repository import ProductRepository
from app.modules.products.schema import ProductCreate, ProductUpdate
from app.modules.products.utils import generate_sku


class ProductService:

    @staticmethod
    def create(
        db: Session,
        product_data: ProductCreate,
        organization_id: str,
        user_id: str,
    ) -> Product:

        # Validate organization
        organization = OrganizationRepository.get_by_id(
            db,
            organization_id,
        )

        if organization is None:
            raise ValueError("Organization not found.")

        # Business Rule
        if product_data.selling_price < product_data.cost_price:
            raise ValueError(
                "Selling price cannot be less than cost price."
            )

        # Generate SKU
        sku = generate_sku(
            db,
            product_data.name,
        )

        product = Product(
            id=str(uuid4()),
            organization_id=organization_id,

            category_id=product_data.category_id,
            brand_id=product_data.brand_id,

            sku=sku,
            barcode=product_data.barcode,

            name=product_data.name,
            description=product_data.description,
            unit=product_data.unit,

            cost_price=product_data.cost_price,
            selling_price=product_data.selling_price,

            stock=product_data.stock,
            minimum_stock=product_data.minimum_stock,

            is_active=product_data.is_active,

            created_by=user_id,
            updated_by=user_id,
        )

        return ProductRepository.create(
            db,
            product,
        )

    @staticmethod
    def get_by_id(
        db: Session,
        product_id: str,
    ):
        return ProductRepository.get_by_id(
            db,
            product_id,
        )

    @staticmethod
    def get_all(
        db: Session,
    ):
        return ProductRepository.get_all(db)

    @staticmethod
    def update(
        db: Session,
        product_id: str,
        product_data: ProductUpdate,
        user_id: str,
    ):

        product = ProductRepository.get_by_id(
            db,
            product_id,
        )

        if product is None:
            raise ValueError("Product not found.")

        update_data = product_data.model_dump(
            exclude_unset=True
        )

        if (
            "selling_price" in update_data
            and "cost_price" in update_data
            and update_data["selling_price"] < update_data["cost_price"]
        ):
            raise ValueError(
                "Selling price cannot be less than cost price."
            )

        for key, value in update_data.items():
            setattr(product, key, value)

        product.updated_by = user_id

        return ProductRepository.update(
            db,
            product,
        )

    @staticmethod
    def delete(
        db: Session,
        product_id: str,
    ):

        product = ProductRepository.get_by_id(
            db,
            product_id,
        )

        if product is None:
            raise ValueError("Product not found.")

        ProductRepository.delete(
            db,
            product,
        )

        return {
            "message": "Product deleted successfully."
        }