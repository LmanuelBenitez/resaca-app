from typing import List, Optional
from sqlalchemy.orm import Session
from datetime import datetime
from app.repositories.consumption_repository import ConsumptionRepository
from app.models.consumption import Consumption
from app.models.alcohol import Alcohol
from app.schemas.consumption import ConsumptionCreate
from app.services.calculation_service import CalculationService


class ConsumptionService:
    """Service for consumption record business logic."""
    
    def __init__(self, db: Session):
        self.repository = ConsumptionRepository(db)
        self.calculation_service = CalculationService(db)
    
    def create_consumption(
        self,
        consumption_data: ConsumptionCreate,
        alcohol: Alcohol,
        weight: float,
        gender: str,
        time_elapsed: float = 0,
        hydration_level: str = "normal"
    ) -> Consumption:
        """Create a consumption record with calculated BAC and water recommendation."""
        
        # Calculate BAC and water recommendation
        result = self.calculation_service.calculate(
            weight=weight,
            gender=gender,
            alcohol=alcohol,
            volume_ml=consumption_data.volume_ml,
            drink_count=1.0,  # Single drink for consumption record
            time_elapsed=time_elapsed,
            hydration_level=hydration_level
        )
        
        # Create consumption record
        consumption = Consumption(
            user_id=consumption_data.user_id,
            alcohol_id=consumption_data.alcohol_id,
            volume_ml=consumption_data.volume_ml,
            estimated_bac=result["bac"],
            water_recommended=result["water_needed_ml"],
            consumption_date=datetime.now()
        )
        
        return self.repository.create(consumption)
    
    def get_user_history(self, user_id: str, limit: int = 50) -> List[Consumption]:
        """Get consumption history for a user."""
        return self.repository.get_by_user_id(user_id, limit)
    
    def get_history_with_alcohol(self, user_id: str, limit: int = 50) -> List:
        """Get consumption history with alcohol details."""
        return self.repository.get_history_with_alcohol(user_id, limit)
