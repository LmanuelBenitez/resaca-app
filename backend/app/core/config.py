from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Database
    DATABASE_URL: str = "sqlite:///./hydration.db"
    
    # API
    API_V1_PREFIX: str = "/api/v1"
    
    # CORS
    CORS_ORIGINS: list[str] = ["*"]
    
    # Hydration constants
    ALCOHOL_DENSITY: float = 0.789  # g/mL
    WATER_PER_ALCOHOL_ML: float = 4.0  # mL of water per mL of pure alcohol
    METABOLISM_RATE: float = 0.015  # % BAC per hour
    MAX_SAFE_BAC: float = 0.05
    GLASS_SIZE: int = 250  # mL
    HYDRATION_RATE: int = 250  # mL per hour
    
    # Widmark factors
    WIDMARK_MALE: float = 0.73
    WIDMARK_FEMALE: float = 0.66
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
