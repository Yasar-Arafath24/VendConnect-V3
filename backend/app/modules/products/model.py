from uuid import uuid4

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Product(Base):
    __tablename__ = "products"

    # ==========================
    # Primary Key
    # ==========================
    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid4()),
    )

    # ==========================
    # Ownership
    # ==========================
    organization_id: Mapped[str] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # ==========================
    # Classification
    # ==========================
    # ForeignKey("categories.id") will be added when the categories module is built
    category_id: Mapped[str | None] = mapped_column(
        String(36),
        nullable=True,
    )

    # ForeignKey("brands.id") will be added when the brands module is built
    brand_id: Mapped[str | None] = mapped_column(
        String(36),
        nullable=True,
    )

    # ==========================
    # Product Details
    # ==========================
    sku: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
        index=True,
    )

    barcode: Mapped[str | None] = mapped_column(
        String(100),
        unique=True,
        nullable=True,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    unit: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    # ==========================
    # Pricing
    # ==========================
    cost_price: Mapped[float] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    selling_price: Mapped[float] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    # ==========================
    # Inventory
    # ==========================
    stock: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    minimum_stock: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    # ==========================
    # Status
    # ==========================
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    # ==========================
    # Audit
    # ==========================
    created_by: Mapped[str | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )

    updated_by: Mapped[str | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # ==========================
    # Relationships
    # ==========================
    organization = relationship(
        "Organization",
        back_populates="products",
    )

    creator = relationship(
        "User",
        foreign_keys=[created_by],
    )

    updater = relationship(
        "User",
        foreign_keys=[updated_by],
    )
