from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ConsumptionBase(BaseModel):
    """Base consumption schema."""
    user_id: str
    alcohol_id: int
    volume_ml: float


class ConsumptionCreate(ConsumptionBase):
    """Schema for creating a consumption record."""
    pass


class ConsumptionResponse(ConsumptionBase):
    """Schema for consumption response."""
    id: int
    estimated_bac: float
    water_recommended: float
    consumption_date: datetime
    created_at: datetime
    
    class Config:
        from_attributes = True


class ConsumptionHistoryResponse(BaseModel):
    """Schema for consumption history response."""
    id: int
    user_id: str
    alcohol_name: str
    alcohol_percentage: float
    volume_ml: float
    estimated_bac: float
    water_recommended: float
    consumption_date: datetime
    
    class Config:
        from_attributes = True
