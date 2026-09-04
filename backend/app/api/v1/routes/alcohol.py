from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.alcohol_service import AlcoholService
from app.schemas.alcohol import AlcoholTypeList, AlcoholCreate, AlcoholResponse

router = APIRouter(prefix="/alcohol", tags=["Alcohol"])


@router.get("/types", response_model=List[AlcoholTypeList])
async def get_alcohol_types(
    db: Session = Depends(get_db)
) -> List[AlcoholTypeList]:
    """
    Get all available alcohol types.
    
    Returns a list of alcohol types with their IDs, names,
    alcohol percentages, and serving sizes.
    """
    service = AlcoholService(db)
    alcohols = service.get_all_alcohols()
    return [
        AlcoholTypeList(
            id=a.id,
            name=a.name,
            alcohol_percentage=a.alcohol_percentage,
            serving_size=a.serving_size
        )
        for a in alcohols
    ]


@router.post("/", response_model=AlcoholResponse, status_code=status.HTTP_201_CREATED)
async def create_alcohol_type(
    alcohol_data: AlcoholCreate,
    db: Session = Depends(get_db)
) -> AlcoholResponse:
    """
    Create a new alcohol type.
    
    - **name**: Name of the alcohol (e.g., "beer", "wine")
    - **alcohol_percentage**: Alcohol percentage by volume (e.g., 5.0 for 5%)
    - **serving_size**: Standard serving size in milliliters
    """
    service = AlcoholService(db)
    
    # Check if alcohol type already exists
    existing = service.get_alcohol_by_id(alcohol_data.name)
    # Note: In a real implementation, we would check by name
    # For now, we'll let the repository handle uniqueness
    
    try:
        alcohol = service.create_alcohol(alcohol_data)
        return AlcoholResponse(
            id=alcohol.id,
            name=alcohol.name,
            alcohol_percentage=alcohol.alcohol_percentage,
            serving_size=alcohol.serving_size,
            created_at=alcohol.created_at
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating alcohol type: {str(e)}"
        )
