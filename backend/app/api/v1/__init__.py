from fastapi import APIRouter
from app.api.v1.routes import alcohol_router, consumption_router, calculation_router

router = APIRouter(prefix="/api/v1")

# Include all route modules
router.include_router(alcohol_router)
router.include_router(consumption_router)
router.include_router(calculation_router)

__all__ = ["router"]
