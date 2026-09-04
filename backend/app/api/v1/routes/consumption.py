from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.consumption_service import ConsumptionService
from app.services.alcohol_service import AlcoholService
from app.schemas.consumption import ConsumptionCreate, ConsumptionResponse, ConsumptionHistoryResponse

router = APIRouter(prefix="/consumption", tags=["Consumption"])


@router.post("/", response_model=ConsumptionResponse, status_code=status.HTTP_201_CREATED)
async def create_consumption(
    consumption_data: ConsumptionCreate,
    weight: float = Query(..., ge=20, le=300, description="Weight in kilograms"),
    gender: str = Query(..., pattern="^(male|female)$", description="Gender: male or female"),
    time_elapsed: float = Query(0, ge=0, le=24, description="Time elapsed in hours"),
    hydration_level: str = Query("normal", pattern="^(normal|dehydrated|wellHydrated)$", description="Hydration level"),
    db: Session = Depends(get_db)
) -> ConsumptionResponse:
    """
    Create a new consumption record.
    
    Records a drink consumption event with calculated BAC and water recommendation.
    
    - **user_id**: Unique identifier for the user
    - **alcohol_id**: ID of the alcohol type consumed
    - **volume_ml**: Volume consumed in milliliters
    - **weight**: User's weight in kilograms (query parameter)
    - **gender**: User's gender (query parameter)
    - **time_elapsed**: Hours since first drink (query parameter)
    - **hydration_level**: Pre-hydration status (query parameter)
    """
    
    # Get alcohol type
    alcohol_service = AlcoholService(db)
    alcohol = alcohol_service.get_alcohol_by_id(consumption_data.alcohol_id)
    
    if not alcohol:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Alcohol type with ID {consumption_data.alcohol_id} not found"
        )
    
    # Create consumption record
    consumption_service = ConsumptionService(db)
    
    try:
        consumption = consumption_service.create_consumption(
            consumption_data=consumption_data,
            alcohol=alcohol,
            weight=weight,
            gender=gender,
            time_elapsed=time_elapsed,
            hydration_level=hydration_level
        )
        
        return ConsumptionResponse(
            id=consumption.id,
            user_id=consumption.user_id,
            alcohol_id=consumption.alcohol_id,
            volume_ml=consumption.volume_ml,
            estimated_bac=consumption.estimated_bac,
            water_recommended=consumption.water_recommended,
            consumption_date=consumption.consumption_date,
            created_at=consumption.created_at
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating consumption record: {str(e)}"
        )


@router.get("/history", response_model=List[ConsumptionHistoryResponse])
async def get_consumption_history(
    user_id: str = Query(..., description="User ID to fetch history for"),
    limit: int = Query(50, ge=1, le=100, description="Maximum number of records to return"),
    db: Session = Depends(get_db)
) -> List[ConsumptionHistoryResponse]:
    """
    Get consumption history for a user.
    
    Returns a list of consumption records with alcohol details,
    ordered by consumption date (newest first).
    
    - **user_id**: Unique identifier for the user
    - **limit**: Maximum number of records to return (default: 50)
    """
    
    consumption_service = ConsumptionService(db)
    
    try:
        consumptions = consumption_service.get_history_with_alcohol(user_id, limit)
        
        return [
            ConsumptionHistoryResponse(
                id=c.id,
                user_id=c.user_id,
                alcohol_name=c.alcohol.name,
                alcohol_percentage=c.alcohol.alcohol_percentage,
                volume_ml=c.volume_ml,
                estimated_bac=c.estimated_bac,
                water_recommended=c.water_recommended,
                consumption_date=c.consumption_date
            )
            for c in consumptions
        ]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching consumption history: {str(e)}"
        )
