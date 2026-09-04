from pydantic import BaseModel, Field
from typing import Literal, List, Optional


class CalculationRequest(BaseModel):
    """Schema for hydration calculation request."""
    alcohol_type: str = Field(..., description="Tipo de alcohol: cerveza, vino, whisky, etc.")
    alcohol_id: int = Field(..., gt=0, description="ID del tipo de alcohol desde la base de datos")
    volume_ml: float = Field(..., ge=50, le=5000, description="Volumen en mililitros")
    weight_kg: float = Field(..., ge=20, le=300, description="Peso en kilogramos")
    gender: Literal["male", "female"] = Field(..., description="Género: male o female")


class CalculationResponse(BaseModel):
    """Schema for hydration calculation response."""
    grams: float = Field(..., description="Gramos de alcohol consumido")
    bac: float = Field(..., description="Nivel de alcohol en sangre")
    waterMl: float = Field(..., description="Agua recomendada en mililitros")
    glasses: float = Field(..., description="Vasos de agua (250ml)")
    hydrationLevel: Literal["Bajo", "Moderado", "Alto"] = Field(..., description="Nivel de hidratación")