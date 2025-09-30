# API Routes
from .products import router as products_router
from .customers import router as customers_router
from .orders import router as orders_router
from .payments import router as payments_router
from .repairs import router as repairs_router
from .analytics import router as analytics_router
from .settings import router as settings_router

__all__ = [
    "products_router", "customers_router", "orders_router", 
    "payments_router", "repairs_router", "analytics_router", "settings_router"
]