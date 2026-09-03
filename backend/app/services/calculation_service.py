import math
from typing import Dict, List, Any
from sqlalchemy.orm import Session
from app.models.alcohol import Alcohol
from app.core.config import settings
from app.services.alcohol_service import AlcoholService


class CalculationService:
    """Service for hydration calculation business logic."""
    
    def __init__(self, db: Session):
        self.db = db
        self.alcohol_service = AlcoholService(db)
    
    def calculate(
        self,
        weight: float,
        gender: str,
        alcohol: Alcohol,
        volume_ml: float,
        drink_count: float,
        time_elapsed: float = 0,
        hydration_level: str = "normal"
    ) -> Dict[str, Any]:
        """
        Calculate hydration needs based on alcohol consumption.
        
        Returns a dictionary with calculation results.
        """
        
        # Validate inputs
        self._validate_calculation_inputs(weight, gender, volume_ml, drink_count, time_elapsed, hydration_level)
        
        # Calculate total pure alcohol consumed
        total_alcohol_ml = volume_ml * drink_count * (alcohol.alcohol_percentage / 100)
        total_alcohol_grams = total_alcohol_ml * settings.ALCOHOL_DENSITY
        
        # Calculate Blood Alcohol Concentration (Widmark formula)
        r = settings.WIDMARK_MALE if gender == "male" else settings.WIDMARK_FEMALE
        weight_grams = weight * 1000
        bac = (total_alcohol_grams / (weight_grams * r)) * 100
        
        # Subtract alcohol metabolized over time
        bac = max(0, bac - (settings.METABOLISM_RATE * time_elapsed))
        
        # Calculate water needed
        base_water_ml = total_alcohol_ml * settings.WATER_PER_ALCOHOL_ML
        
        # Hydration factor adjustment
        hydration_factor = 1.0
        if hydration_level == "dehydrated":
            hydration_factor = 1.5
        elif hydration_level == "wellHydrated":
            hydration_factor = 0.7
        
        # Time adjustment
        time_factor = 1.0
        if time_elapsed > 0:
            time_factor = max(0.3, 1 - (time_elapsed / 12) * 0.5)
        
        water_needed_ml = base_water_ml * hydration_factor * time_factor
        
        # Additional water for body weight
        maintenance_water = weight * 0.33  # 33ml per kg
        water_needed_ml = max(water_needed_ml, maintenance_water * 0.3)
        
        # Cap at 4L
        water_needed_ml = min(water_needed_ml, 4000)
        
        # Calculate glasses
        glasses_needed = math.ceil(water_needed_ml / settings.GLASS_SIZE)
        
        # Time to hydrate
        time_to_hydrate_minutes = math.ceil((water_needed_ml / settings.HYDRATION_RATE) * 60)
        
        # Status message based on BAC
        status_text, status_class = self._get_status_info(bac)
        
        # Generate tips
        tips = self._generate_tips(bac, water_needed_ml, time_elapsed, drink_count, hydration_level)
        
        return {
            "water_needed_ml": water_needed_ml,
            "glasses_needed": glasses_needed,
            "time_to_hydrate_minutes": time_to_hydrate_minutes,
            "bac": bac,
            "status_text": status_text,
            "status_class": status_class,
            "tips": tips,
            "total_alcohol_ml": total_alcohol_ml,
            "total_alcohol_grams": total_alcohol_grams
        }
    
    def _validate_calculation_inputs(
        self,
        weight: float,
        gender: str,
        volume_ml: float,
        drink_count: float,
        time_elapsed: float,
        hydration_level: str
    ) -> None:
        """Validate calculation inputs."""
        
        if weight < 20 or weight > 300:
            raise ValueError("Peso debe estar entre 20-300 kg")
        
        if gender not in ["male", "female"]:
            raise ValueError("Género inválido")
        
        if volume_ml < 50 or volume_ml > 2000:
            raise ValueError("Volumen debe estar entre 50-2000 ml")
        
        if drink_count < 0.5 or drink_count > 50:
            raise ValueError("Número de bebidas debe estar entre 0.5-50")
        
        if time_elapsed < 0 or time_elapsed > 24:
            raise ValueError("Tiempo debe estar entre 0-24 horas")
        
        if hydration_level not in ["normal", "dehydrated", "wellHydrated"]:
            raise ValueError("Nivel de hidratación inválido")
    
    def _get_status_info(self, bac: float) -> tuple:
        """Get status text and class based on BAC."""
        
        if bac >= 0.15:
            return (
                "⚠️ Alto nivel de alcohol. ¡Hidrátate inmediatamente!",
                "status-danger"
            )
        elif bac >= 0.08:
            return (
                "⚠️ Nivel significativo. Bebe agua con urgencia.",
                "status-danger"
            )
        elif bac >= 0.05:
            return (
                "⚠️ Nivel moderado. Necesitas hidratarte.",
                "status-moderate"
            )
        elif bac >= 0.02:
            return (
                "✅ Nivel bajo. Mantente hidratado.",
                "status-safe"
            )
        else:
            return (
                "✅ Nivel muy bajo. Sigue hidratándote bien.",
                "status-safe"
            )
    
    def _generate_tips(
        self,
        bac: float,
        water_needed_ml: float,
        time_elapsed: float,
        drink_count: float,
        hydration_level: str
    ) -> List[str]:
        """Generate hydration tips."""
        
        tips = []
        
        if bac > 0.05:
            tips.append("🕐 Espera al menos 1 hora antes de conducir por cada bebida estándar consumida.")
        
        if water_needed_ml > 1000:
            tips.append("💧 Bebe el agua de forma gradual, no toda de una vez. Tu cuerpo la absorberá mejor.")
        
        if time_elapsed < 2 and drink_count > 2:
            tips.append("⏰ Has consumido alcohol recientemente. Tómate tu tiempo para hidratarte.")
        
        tips.append("🥤 Los electrolitos (como en bebidas deportivas) pueden ayudar a una mejor hidratación.")
        
        if hydration_level == "dehydrated":
            tips.append("⚠️ Partías deshidratado. Aumenta tu consumo de agua en las próximas horas.")
        
        return tips
