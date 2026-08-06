from uuid import uuid4

from sqlalchemy.orm import Session

from app.modules.categories.model import Category
from app.modules.categories.repository import CategoryRepository
from app.modules.categories.schema import (
    CategoryCreate,
    CategoryUpdate,
)
from app.modules.organizations.repository import (
    OrganizationRepository,
)


class CategoryService:

    @staticmethod
    def create(
        db: Session,
        category_data: CategoryCreate,
        organization_id: str,
        user_id: str,
    ) -> Category:

        # Validate organization
        organization = OrganizationRepository.get_by_id(
            db,
            organization_id,
        )

        if organization is None:
            raise ValueError("Organization not found.")

        # Prevent duplicate names
        existing = CategoryRepository.get_by_name(
            db,
            organization_id,
            category_data.name,
        )

        if existing:
            raise ValueError(
                "Category already exists."
            )

        # Validate parent category
        if category_data.parent_id:

            parent = CategoryRepository.get_by_id(
                db,
                category_data.parent_id,
            )

            if parent is None:
                raise ValueError(
                    "Parent category not found."
                )

        category = Category(
            id=str(uuid4()),
            organization_id=organization_id,

            parent_id=category_data.parent_id,

            name=category_data.name,
            description=category_data.description,
            is_active=category_data.is_active,

            created_by=user_id,
            updated_by=user_id,
        )

        return CategoryRepository.create(
            db,
            category,
        )

    @staticmethod
    def get_by_id(
        db: Session,
        category_id: str,
    ):
        return CategoryRepository.get_by_id(
            db,
            category_id,
        )

    @staticmethod
    def get_all(
        db: Session,
        organization_id: str,
    ):
        return CategoryRepository.get_all(
            db,
            organization_id,
        )

    @staticmethod
    def search(
        db: Session,
        organization_id: str,
        keyword: str,
    ):
        return CategoryRepository.search(
            db,
            organization_id,
            keyword,
        )

    @staticmethod
    def update(
        db: Session,
        category_id: str,
        category_data: CategoryUpdate,
        user_id: str,
    ):

        category = CategoryRepository.get_by_id(
            db,
            category_id,
        )

        if category is None:
            raise ValueError(
                "Category not found."
            )

        update_data = category_data.model_dump(
            exclude_unset=True
        )

        # Prevent self-parent
        if (
            "parent_id" in update_data
            and update_data["parent_id"] == category.id
        ):
            raise ValueError(
                "Category cannot be its own parent."
            )

        # Validate parent
        if (
            "parent_id" in update_data
            and update_data["parent_id"] is not None
        ):
            parent = CategoryRepository.get_by_id(
                db,
                update_data["parent_id"],
            )

            if parent is None:
                raise ValueError(
                    "Parent category not found."
                )

        # Prevent duplicate names
        if (
            "name" in update_data
            and update_data["name"] != category.name
        ):
            duplicate = CategoryRepository.get_by_name(
                db,
                category.organization_id,
                update_data["name"],
            )

            if duplicate:
                raise ValueError(
                    "Category name already exists."
                )

        for key, value in update_data.items():
            setattr(category, key, value)

        category.updated_by = user_id

        return CategoryRepository.update(
            db,
            category,
        )

    @staticmethod
    def delete(
        db: Session,
        category_id: str,
    ):

        category = CategoryRepository.get_by_id(
            db,
            category_id,
        )

        if category is None:
            raise ValueError(
                "Category not found."
            )

        # Prevent deleting category with children
        children = CategoryRepository.get_children(
            db,
            category.id,
        )

        if children:
            raise ValueError(
                "Cannot delete a category that has child categories."
            )

        CategoryRepository.delete(
            db,
            category,
        )

        return {
            "message": "Category deleted successfully."
        }