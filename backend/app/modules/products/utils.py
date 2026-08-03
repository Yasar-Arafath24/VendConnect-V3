import re

from sqlalchemy.orm import Session

from app.modules.products.model import Product


def generate_sku(
    db: Session,
    product_name: str,
) -> str:
    """
    Generate a unique SKU.

    Example:
        Coca Cola 500ml -> COC-COL-0001
        Nestle Coffee -> NES-COF-0002
    """

    # Keep only letters
    words = re.findall(r"[A-Za-z]+", product_name)

    if len(words) >= 2:
        prefix = (
            words[0][:3] + "-" + words[1][:3]
        ).upper()
    elif len(words) == 1:
        prefix = words[0][:6].upper()
    else:
        prefix = "PRD"

    count = db.query(Product).count() + 1

    return f"{prefix}-{count:04d}"