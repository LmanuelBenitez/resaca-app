from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Optional
from app.models.consumption import Consumption


class ConsumptionRepository:
    """Repository for consumption record operations."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, consumption: Consumption) -> Consumption:
        """Create a new consumption record."""
        self.db.add(consumption)
        self.db.commit()
        self.db.refresh(consumption)
        return consumption
    
    def get_by_id(self, consumption_id: int) -> Optional[Consumption]:
        """Get a consumption record by ID."""
        return self.db.query(Consumption).filter(Consumption.id == consumption_id).first()
    
    def get_by_user_id(self, user_id: str, limit: int = 50) -> List[Consumption]:
        """Get consumption records for a user, ordered by date descending."""
        return (
            self.db.query(Consumption)
            .filter(Consumption.user_id == user_id)
            .order_by(desc(Consumption.consumption_date))
            .limit(limit)
            .all()
        )
    
    def get_history_with_alcohol(self, user_id: str, limit: int = 50) -> List:
        """Get consumption history with alcohol details."""
        from sqlalchemy.orm import joinedload
        
        return (
            self.db.query(Consumption)
            .options(joinedload(Consumption.alcohol))
            .filter(Consumption.user_id == user_id)
            .order_by(desc(Consumption.consumption_date))
            .limit(limit)
            .all()
        )
