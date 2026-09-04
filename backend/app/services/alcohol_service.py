from typing import List, Optional
from sqlalchemy.orm import Session
from app.repositories.alcohol_repository import AlcoholRepository
from app.models.alcohol import Alcohol
from app.schemas.alcohol import AlcoholCreate


class AlcoholService:
    """Service for alcohol type business logic."""
    
    def __init__(self, db: Session):
        self.repository = AlcoholRepository(db)
    
    def get_all_alcohols(self) -> List[Alcohol]:
        """Get all alcohol types."""
        return self.repository.get_all()
    
    def get_alcohol_by_id(self, alcohol_id: int) -> Optional[Alcohol]:
        """Get an alcohol type by ID."""
        return self.repository.get_by_id(alcohol_id)
    
    def create_alcohol(self, alcohol_data: AlcoholCreate) -> Alcohol:
        """Create a new alcohol type."""
        alcohol = Alcohol(
            name=alcohol_data.name,
            alcohol_percentage=alcohol_data.alcohol_percentage,
            serving_size=alcohol_data.serving_size
        )
        return self.repository.create(alcohol)
    
    def ensure_defaults(self) -> None:
        """Ensure default alcohol types exist."""
        self.repository.create_defaults()
