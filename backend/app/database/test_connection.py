from sqlalchemy import text

from app.database.database import engine


def test_connection():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT version();"))
        print(result.fetchone())


if __name__ == "__main__":
    test_connection()