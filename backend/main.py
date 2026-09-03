from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import router as v1_router
from app.core.database import init_db

app = FastAPI(
    title="Hydration Calculator API",
    version="1.0.0",
    description="API for calculating hydration needs based on alcohol consumption"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(v1_router)


@app.get("/")
def root():
    """Root endpoint."""
    return {
        "message": "Hydration Calculator API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs"
    }


@app.on_event("startup")
async def startup_event():
    """Initialize database and seed default alcohol types on startup."""
    init_db()
    
    # Seed default alcohol types
    from app.services.alcohol_service import AlcoholService
    from app.core.database import SessionLocal
    
    db = SessionLocal()
    try:
        service = AlcoholService(db)
        service.ensure_defaults()
    finally:
        db.close()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
