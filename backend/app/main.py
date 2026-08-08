from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import settings
from app.core.exceptions import register_exception_handlers
from app.core.logging import app_logger
from app.database.init_db import init_db
from app.modules.organizations.router import router as organization_router
from app.modules.rbac.router import router as rbac_router
from app.modules.rbac.user_role_router import router as user_role_router
from app.modules.users.router import router as users_router
from app.modules.auth.router import router as auth_router
from app.modules.products.router import (
    router as product_router,
)
from app.modules.categories.router import (
    router as category_router,
)
from app.modules.brands.router import (
    router as brand_router,
)
from app.modules.units.router import (
    router as unit_router,
)
from app.modules.warehouses.router import (
    router as warehouse_router,
)
from app.modules.inventory.router import (
    router as inventory_router,
)
from app.modules.inventory.router import (
    router as inventory_router,
)
from app.modules.inventory.movement_router import (
    router as inventory_movement_router,
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    app_logger.info("VendConnect Server Started")
    yield


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-Powered B2B Wholesale SaaS Platform",
    lifespan=lifespan,
)

app.include_router(organization_router)
app.include_router(rbac_router)
app.include_router(users_router)
app.include_router(auth_router)
app.include_router(user_role_router)
app.include_router(product_router)
app.include_router(category_router)
app.include_router(brand_router)
app.include_router(unit_router)
app.include_router(warehouse_router)
app.include_router(inventory_movement_router)
app.include_router(inventory_router)
register_exception_handlers(app)


@app.get("/")
async def root():
    app_logger.info("Root endpoint accessed")

    return {
        "application": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "Running",
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy",
    }