from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Consumption(Base):
    """Alcohol consumption record model."""
    
    __tablename__ = "consumptions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(50), nullable=False, index=True)
    alcohol_id = Column(Integer, ForeignKey("alcohols.id"), nullable=False)
    volume_ml = Column(Float, nullable=False)
    estimated_bac = Column(Float, nullable=False)
    water_recommended = Column(Float, nullable=False)
    consumption_date = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationship
    alcohol = relationship("Alcohol", backref="consumptions")
    
    def __repr__(self) -> str:
        return f"<Consumption(id={self.id}, user_id='{self.user_id}', alcohol_id={self.alcohol_id}, bac={self.estimated_bac})>"
