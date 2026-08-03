from app.database.init_db import init_db  # registers all models
from app.database.session import SessionLocal
from app.modules.products.utils import generate_sku

init_db()

db = SessionLocal()

print(generate_sku(
    db,
    "Coca Cola 500ml"
))