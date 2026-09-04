from app.api.v1.routes.alcohol import router as alcohol_router
from app.api.v1.routes.consumption import router as consumption_router
from app.api.v1.routes.calculation import router as calculation_router

__all__ = [
    "alcohol_router",
    "consumption_router",
    "calculation_router"
]
