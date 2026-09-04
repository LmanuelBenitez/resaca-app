from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.alcohol import Alcohol


class AlcoholRepository:
    """Repository for alcohol type operations."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_all(self) -> List[Alcohol]:
        """Get all alcohol types."""
        return self.db.query(Alcohol).order_by(Alcohol.name).all()
    
    def get_by_id(self, alcohol_id: int) -> Optional[Alcohol]:
        """Get an alcohol type by ID."""
        return self.db.query(Alcohol).filter(Alcohol.id == alcohol_id).first()
    
    def get_by_name(self, name: str) -> Optional[Alcohol]:
        """Get an alcohol type by name."""
        return self.db.query(Alcohol).filter(Alcohol.name == name).first()
    
    def create(self, alcohol: Alcohol) -> Alcohol:
        """Create a new alcohol type."""
        self.db.add(alcohol)
        self.db.commit()
        self.db.refresh(alcohol)
        return alcohol
    
    def create_defaults(self) -> None:
        """Create default alcohol types if they don't exist."""
        defaults = [
            {"name": "beer", "alcohol_percentage": 5.0, "serving_size": 330.0},
            {"name": "wine", "alcohol_percentage": 12.0, "serving_size": 150.0},
            {"name": "whisky", "alcohol_percentage": 40.0, "serving_size": 44.0},
            {"name": "vodka", "alcohol_percentage": 40.0, "serving_size": 44.0},
            {"name": "rum", "alcohol_percentage": 40.0, "serving_size": 44.0},
            {"name": "tequila", "alcohol_percentage": 38.0, "serving_size": 44.0},
        ]
        
        for data in defaults:
            existing = self.get_by_name(data["name"])
            if not existing:
                alcohol = Alcohol(
                    name=data["name"],
                    alcohol_percentage=data["alcohol_percentage"],
                    serving_size=data["serving_size"]
                )
                self.db.add(alcohol)
        
        self.db.commit()
