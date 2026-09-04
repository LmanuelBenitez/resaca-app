from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import router as v1_router
# Elimina esta línea: from app.core.database import init_db

app = FastAPI(
    title="Hydration API",
    description="API para calcular hidratación",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(v1_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Hydration API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}