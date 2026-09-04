from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class AlcoholBase(BaseModel):
    """Base alcohol schema."""
    name: str
    alcohol_percentage: float
    serving_size: float = 250.0


class AlcoholCreate(AlcoholBase):
    """Schema for creating an alcohol type."""
    pass


class AlcoholResponse(AlcoholBase):
    """Schema for alcohol type response."""
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class AlcoholTypeList(BaseModel):
    """Schema for a simple alcohol type list item."""
    id: int
    name: str
    alcohol_percentage: float
    serving_size: float
    
    class Config:
        from_attributes = True
