from sqlalchemy.orm import Session

from app.modules.categories.model import Category


class CategoryRepository:

    @staticmethod
    def create(
        db: Session,
        category: Category,
    ) -> Category:

        db.add(category)
        db.commit()
        db.refresh(category)

        return category

    @staticmethod
    def get_by_id(
        db: Session,
        category_id: str,
    ):

        return (
            db.query(Category)
            .filter(Category.id == category_id)
            .first()
        )

    @staticmethod
    def get_by_name(
        db: Session,
        organization_id: str,
        name: str,
    ):

        return (
            db.query(Category)
            .filter(
                Category.organization_id == organization_id,
                Category.name == name,
            )
            .first()
        )

    @staticmethod
    def get_all(
        db: Session,
        organization_id: str,
    ):

        return (
            db.query(Category)
            .filter(
                Category.organization_id == organization_id
            )
            .order_by(Category.name.asc())
            .all()
        )

    @staticmethod
    def get_root_categories(
        db: Session,
        organization_id: str,
    ):

        return (
            db.query(Category)
            .filter(
                Category.organization_id == organization_id,
                Category.parent_id.is_(None),
            )
            .order_by(Category.name.asc())
            .all()
        )

    @staticmethod
    def get_children(
        db: Session,
        parent_id: str,
    ):

        return (
            db.query(Category)
            .filter(Category.parent_id == parent_id)
            .order_by(Category.name.asc())
            .all()
        )

    @staticmethod
    def search(
        db: Session,
        organization_id: str,
        keyword: str,
    ):

        return (
            db.query(Category)
            .filter(
                Category.organization_id == organization_id,
                Category.name.ilike(f"%{keyword}%"),
            )
            .order_by(Category.name.asc())
            .all()
        )

    @staticmethod
    def update(
        db: Session,
        category: Category,
    ):

        db.commit()
        db.refresh(category)

        return category

    @staticmethod
    def delete(
        db: Session,
        category: Category,
    ):

        db.delete(category)
        db.commit()