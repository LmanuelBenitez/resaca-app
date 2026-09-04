from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from app.core.database import Base


class Alcohol(Base):
    """Alcohol type model."""
    
    __tablename__ = "alcohols"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    alcohol_percentage = Column(Float, nullable=False)
    serving_size = Column(Float, nullable=False, default=250.0)  # mL
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self) -> str:
        return f"<Alcohol(id={self.id}, name='{self.name}', percentage={self.alcohol_percentage})>"
