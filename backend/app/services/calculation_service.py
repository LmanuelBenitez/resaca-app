import math
from typing import Dict, Any, Literal
from sqlalchemy.orm import Session
from app.models.alcohol import Alcohol
from app.core.config import settings


class CalculationService:
    """Service for hydration calculation business logic."""

    def __init__(self, db: Session):
        self.db = db

    def calculate(
        self,
        alcohol_type: str,
        volume_ml: float,
        weight_kg: float,
        gender: Literal["male", "female"]
    ) -> Dict[str, Any]:
        """
        Calculate hydration needs based on alcohol consumption.

        Returns a dictionary with calculation results matching the frontend schema.
        """
        # Validar entradas
        self._validate_inputs(alcohol_type, volume_ml, weight_kg, gender)

        # Obtener el alcohol de la base de datos
        alcohol = self.db.query(Alcohol).filter(Alcohol.name.ilike(alcohol_type)).first()
        if not alcohol:
            raise ValueError(f"Tipo de alcohol no encontrado: {alcohol_type}")

        # Calcular gramos de alcohol puro
        alcohol_ml = volume_ml * (alcohol.alcohol_percentage / 100)
        grams = alcohol_ml * settings.ALCOHOL_DENSITY

        # Calcular BAC (Widmark formula)
        r = settings.WIDMARK_MALE if gender == "male" else settings.WIDMARK_FEMALE
        bac = grams / (weight_kg * r)

        # Calcular agua recomendada
        water_ml = bac * 5000
        glasses = water_ml / settings.GLASS_SIZE

        # Determinar nivel de hidratación
        if bac < 0.05:
            hydration_level = "Bajo"
        elif bac < 0.08:
            hydration_level = "Moderado"
        else:
            hydration_level = "Alto"

        return {
            "grams": grams,
            "bac": bac,
            "water_ml": water_ml,
            "glasses": glasses,
            "hydration_level": hydration_level
        }

    def _validate_inputs(
        self,
        alcohol_type: str,
        volume_ml: float,
        weight_kg: float,
        gender: str
    ) -> None:
        """Validar entradas del cálculo."""
        if weight_kg < 20 or weight_kg > 300:
            raise ValueError("El peso debe estar entre 20 y 300 kg")

        if gender not in ["male", "female"]:
            raise ValueError("El género debe ser 'male' o 'female'")

        if volume_ml < 50 or volume_ml > 5000:
            raise ValueError("El volumen debe estar entre 50 y 5000 ml")

        if not alcohol_type or len(alcohol_type) < 2:
            raise ValueError("El tipo de alcohol es requerido")