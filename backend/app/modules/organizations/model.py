from uuid import uuid4

from sqlalchemy import Boolean, DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Organization(Base):
    __tablename__ = "organizations"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid4())
    )

    organization_code: Mapped[str] = mapped_column(
        String(20),
        unique=True,
        nullable=False,
        index=True
    )

    organization_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
        index=True
    )

    owner_name: Mapped[str] = mapped_column(
        String(120),
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        String(120),
        unique=True,
        nullable=False
    )

    phone: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    gst_number: Mapped[str] = mapped_column(
        String(30),
        nullable=True
    )

    address: Mapped[str] = mapped_column(
        String(500),
        nullable=True
    )

    city: Mapped[str] = mapped_column(
        String(100),
        nullable=True
    )

    state: Mapped[str] = mapped_column(
        String(100),
        nullable=True
    )

    pincode: Mapped[str] = mapped_column(
        String(10),
        nullable=True
    )

    logo_url: Mapped[str] = mapped_column(
        String(500),
        nullable=True
    )

    subscription_plan: Mapped[str] = mapped_column(
        String(20),
        default="FREE"
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    products = relationship(
        "Product",
        back_populates="organization",
    )

    categories = relationship(
        "Category",
        back_populates="organization",
    )

    brands = relationship(
        "Brand",
        back_populates="organization",
    )

    units = relationship(
        "Unit",
        back_populates="organization",
    )

    warehouses = relationship(
        "Warehouse",
        back_populates="organization",
    )