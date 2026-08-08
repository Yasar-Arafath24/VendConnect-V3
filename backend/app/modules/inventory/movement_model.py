from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.base import Base


class InventoryMovement(Base):

    __tablename__ = "inventory_movements"

    # ==========================================
    # Primary Key
    # ==========================================

    id = Column(
        String,
        primary_key=True,
        index=True,
    )

    # ==========================================
    # Organization
    # ==========================================

    organization_id = Column(
        String,
        ForeignKey(
            "organizations.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    # ==========================================
    # Inventory
    # ==========================================

    inventory_id = Column(
        String,
        ForeignKey(
            "inventory.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    # ==========================================
    # Product / Warehouse
    # ==========================================

    product_id = Column(
        String,
        ForeignKey(
            "products.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    warehouse_id = Column(
        String,
        ForeignKey(
            "warehouses.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    # ==========================================
    # Movement Information
    # ==========================================

    movement_type = Column(
        String,
        nullable=False,
        index=True,
    )

    quantity = Column(
        Integer,
        nullable=False,
    )

    # ==========================================
    # Stock Snapshot
    # ==========================================

    quantity_before = Column(
        Integer,
        nullable=False,
    )

    quantity_after = Column(
        Integer,
        nullable=False,
    )

    # ==========================================
    # Reference
    # ==========================================

    reference_type = Column(
        String,
        nullable=True,
    )

    reference_id = Column(
        String,
        nullable=True,
    )

    reason = Column(
        String,
        nullable=True,
    )

    # ==========================================
    # Audit
    # ==========================================

    created_by = Column(
        String,
        ForeignKey(
            "users.id",
            ondelete="SET NULL",
        ),
        nullable=True,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    # ==========================================
    # Relationships
    # ==========================================

    organization = relationship(
        "Organization",
    )

    inventory = relationship(
        "Inventory",
    )

    product = relationship(
        "Product",
    )

    warehouse = relationship(
        "Warehouse",
    )

    creator = relationship(
        "User",
        foreign_keys=[created_by],
    )