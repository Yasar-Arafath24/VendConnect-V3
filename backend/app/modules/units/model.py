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


class Unit(Base):
    __tablename__ = "units"

    # ==========================
    # Primary Key
    # ==========================
    id = Column(
        String,
        primary_key=True,
        index=True,
    )

    # ==========================
    # Organization
    # ==========================
    organization_id = Column(
        String,
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # ==========================
    # Unit Details
    # ==========================
    name = Column(
        String(100),
        nullable=False,
        index=True,
    )

    symbol = Column(
        String(20),
        nullable=False,
        index=True,
    )

    description = Column(
        Text,
        nullable=True,
    )

    is_active = Column(
        Boolean,
        default=True,
        nullable=False,
    )

    # ==========================
    # Audit Fields
    # ==========================
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

    # ==========================
    # Relationships
    # ==========================
    organization = relationship(
        "Organization",
        back_populates="units",
    )

    products = relationship(
        "Product",
        back_populates="unit",
    )

    creator = relationship(
        "User",
        foreign_keys=[created_by],
    )

    updater = relationship(
        "User",
        foreign_keys=[updated_by],
    )