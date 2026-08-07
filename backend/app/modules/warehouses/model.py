from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    String,
    Text,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.base import Base


class Warehouse(Base):
    __tablename__ = "warehouses"

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
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # ==========================================
    # Warehouse Details
    # ==========================================
    name = Column(
        String(150),
        nullable=False,
        index=True,
    )

    code = Column(
        String(30),
        nullable=False,
        index=True,
    )

    address = Column(
        Text,
        nullable=True,
    )

    city = Column(
        String(100),
        nullable=True,
    )

    state = Column(
        String(100),
        nullable=True,
    )

    country = Column(
        String(100),
        nullable=True,
    )

    postal_code = Column(
        String(20),
        nullable=True,
    )

    phone = Column(
        String(20),
        nullable=True,
    )

    email = Column(
        String(150),
        nullable=True,
    )

    manager_name = Column(
        String(150),
        nullable=True,
    )

    is_default = Column(
        Boolean,
        default=False,
        nullable=False,
    )

    is_active = Column(
        Boolean,
        default=True,
        nullable=False,
    )

    # ==========================================
    # Audit Fields
    # ==========================================
    created_by = Column(
        String,
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )

    updated_by = Column(
        String,
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # ==========================================
    # Relationships
    # ==========================================
    organization = relationship(
        "Organization",
        back_populates="warehouses",
    )

    creator = relationship(
        "User",
        foreign_keys=[created_by],
    )

    updater = relationship(
        "User",
        foreign_keys=[updated_by],
    )