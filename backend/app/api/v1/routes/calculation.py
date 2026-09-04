from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.calculation_service import CalculationService
from app.services.alcohol_service import AlcoholService
from app.schemas.calculation import CalculationRequest, CalculationResponse

router = APIRouter(tags=["Calculation"])


@router.post("/calculate", response_model=CalculationResponse)
async def calculate_hydration(
    request: CalculationRequest,
    db: Session = Depends(get_db)
) -> CalculationResponse:
    """
    Calculate hydration needs based on alcohol consumption.
    
    This endpoint calculates:
    - Blood Alcohol Concentration (BAC) using the Widmark formula
    - Recommended water intake to rehydrate
    - Number of glasses needed
    - Time required to hydrate
    - Status message and tips
    
    **Request body:**
    - **weight**: User's weight in kilograms (20-300 kg)
    - **gender**: "male" or "female"
    - **alcohol_id**: ID of the alcohol type (from GET /alcohol/types)
    - **volume_ml**: Volume per drink in milliliters (50-2000 ml)
    - **drink_count**: Number of drinks consumed (0.5-50)
    - **time_elapsed**: Hours since first drink (0-24 hours)
    - **hydration_level**: "normal", "dehydrated", or "wellHydrated"
    
    **Response:**
    - **water_needed_ml**: Recommended water intake in milliliters
    - **glasses_needed**: Number of 250ml glasses needed
    - **time_to_hydrate_minutes**: Estimated time to hydrate
    - **bac**: Calculated Blood Alcohol Concentration (%)
    - **status_text**: Descriptive status message
    - **status_class**: CSS class for styling (status-safe, status-moderate, status-danger)
    - **tips**: List of hydration tips
    - **total_alcohol_ml**: Total pure alcohol consumed in milliliters
    - **total_alcohol_grams**: Total pure alcohol consumed in grams
    """
    
    # Get alcohol type
    alcohol_service = AlcoholService(db)
    alcohol = alcohol_service.get_alcohol_by_id(request.alcohol_id)
    
    if not alcohol:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Alcohol type with ID {request.alcohol_id} not found"
        )
    
    # Perform calculation
    calculation_service = CalculationService(db)
    
    try:
        result = calculation_service.calculate(
            weight_kg=request.weight_kg,
            gender=request.gender,
            alcohol_type=request.alcohol_type,
            volume_ml=request.volume_ml,
        )
        
        return CalculationResponse(
            waterMl=result["water_ml"],
            glasses=result["glasses"],
            bac=result["bac"],
            grams=result["grams"],
            hydrationLevel=result["hydration_level"],
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error performing calculation: {str(e)}"
        )
