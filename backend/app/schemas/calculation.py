from pydantic import BaseModel, Field
from typing import Optional, List


class CalculationRequest(BaseModel):
    """Schema for hydration calculation request."""
    weight: float = Field(..., ge=20, le=300, description="Weight in kilograms")
    gender: str = Field(..., pattern="^(male|female)$", description="Gender: male or female")
    alcohol_id: int = Field(..., description="ID of the alcohol type")
    volume_ml: float = Field(..., ge=50, le=2000, description="Volume in milliliters")
    drink_count: float = Field(..., ge=0.5, le=50, description="Number of drinks consumed")
    time_elapsed: float = Field(0, ge=0, le=24, description="Time elapsed in hours")
    hydration_level: str = Field("normal", pattern="^(normal|dehydrated|wellHydrated)$", description="Hydration level")


class CalculationResponse(BaseModel):
    """Schema for hydration calculation response."""
    water_needed_ml: float
    glasses_needed: int
    time_to_hydrate_minutes: int
    bac: float
    status_text: str
    status_class: str
    tips: List[str]
    total_alcohol_ml: float
    total_alcohol_grams: float
