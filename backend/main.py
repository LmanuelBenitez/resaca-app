from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import math

app = FastAPI(title="Hydration Calculator API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Constants
ALCOHOL_DENSITY = 0.789  # g/mL
WATER_PER_ALCOHOL_ML = 4  # mL of water per mL of pure alcohol
MAX_SAFE_BAC = 0.05  # 0.05% BAC legal limit
GLASS_SIZE = 250  # mL
HYDRATION_RATE = 250  # mL per hour


# Drink presets
DRINK_PRESETS = {
    "beer": {"alcohol": 5, "label": "Cerveza"},
    "wine": {"alcohol": 12, "label": "Vino"},
    "spirit": {"alcohol": 40, "label": "Licor"},
    "cocktail": {"alcohol": 15, "label": "Cóctel"},
    "custom": {"alcohol": None, "label": "Personalizado"}
}

class HydrationRequest(BaseModel):
    weight: float
    gender: str  # "male" or "female"
    drink_type: str
    custom_alcohol: Optional[float] = None
    drink_volume: float
    drink_count: float
    time_elapsed: float
    hydration_level: str  # "normal", "dehydrated", "wellHydrated"

class HydrationResponse(BaseModel):
    water_needed_ml: float
    glasses_needed: int
    time_to_hydrate_minutes: int
    bac: float
    status_text: str
    status_class: str
    tips: List[str]
    total_alcohol_ml: float
    total_alcohol_grams: float

@app.get("/")
def root():
    return {"message": "Hydration Calculator API", "status": "running"}

@app.get("/drink-types")
def get_drink_types():
    """Get available drink types with their alcohol percentages"""
    return {
        "drink_types": [
            {"id": "beer", "label": "Cerveza", "alcohol": 5},
            {"id": "wine", "label": "Vino", "alcohol": 12},
            {"id": "spirit", "label": "Licor", "alcohol": 40},
            {"id": "cocktail", "label": "Cóctel", "alcohol": 15},
            {"id": "custom", "label": "Personalizado", "alcohol": None}
        ]
    }

@app.post("/calculate", response_model=HydrationResponse)
def calculate_hydration(request: HydrationRequest):
    """Calculate hydration needs based on alcohol consumption"""
    
    # Validate inputs
    if request.weight < 20 or request.weight > 300:
        raise HTTPException(status_code=400, detail="Peso debe estar entre 20-300 kg")
    
    if request.gender not in ["male", "female"]:
        raise HTTPException(status_code=400, detail="Género inválido")
    
    # Get alcohol percentage
    if request.drink_type == "custom":
        if request.custom_alcohol is None:
            raise HTTPException(status_code=400, detail="Porcentaje de alcohol requerido para tipo personalizado")
        alcohol_percent = request.custom_alcohol
        if alcohol_percent < 0.5 or alcohol_percent > 100:
            raise HTTPException(status_code=400, detail="Porcentaje de alcohol debe estar entre 0.5-100%")
    else:
        if request.drink_type not in DRINK_PRESETS:
            raise HTTPException(status_code=400, detail="Tipo de bebida inválido")
        alcohol_percent = DRINK_PRESETS[request.drink_type]["alcohol"]
    
    if request.drink_volume < 50 or request.drink_volume > 2000:
        raise HTTPException(status_code=400, detail="Volumen debe estar entre 50-2000 ml")
    
    if request.drink_count < 0.5 or request.drink_count > 50:
        raise HTTPException(status_code=400, detail="Número de bebidas debe estar entre 0.5-50")
    
    if request.time_elapsed < 0 or request.time_elapsed > 24:
        raise HTTPException(status_code=400, detail="Tiempo debe estar entre 0-24 horas")
    
    if request.hydration_level not in ["normal", "dehydrated", "wellHydrated"]:
        raise HTTPException(status_code=400, detail="Nivel de hidratación inválido")
    
    # Calculate total pure alcohol consumed
    total_alcohol_ml = (request.drink_volume * request.drink_count) * (alcohol_percent / 100)
    total_alcohol_grams = total_alcohol_ml * ALCOHOL_DENSITY
    
    # Calculate Blood Alcohol Concentration (Widmark formula)
    r = 0.68 if request.gender == "male" else 0.55
    weight_grams = request.weight * 1000
    bac = (total_alcohol_grams / (weight_grams * r)) * 100
    
    # Subtract alcohol metabolized over time
    metabolism_rate = 0.015  # % BAC per hour
    bac = max(0, bac - (metabolism_rate * request.time_elapsed))
    
    # Calculate water needed
    base_water_ml = total_alcohol_ml * WATER_PER_ALCOHOL_ML
    
    # Hydration factor adjustment
    hydration_factor = 1.0
    if request.hydration_level == "dehydrated":
        hydration_factor = 1.5
    elif request.hydration_level == "wellHydrated":
        hydration_factor = 0.7
    
    # Time adjustment
    time_factor = 1.0
    if request.time_elapsed > 0:
        time_factor = max(0.3, 1 - (request.time_elapsed / 12) * 0.5)
    
    water_needed_ml = base_water_ml * hydration_factor * time_factor
    
    # Additional water for body weight
    maintenance_water = request.weight * 0.33  # 33ml per kg
    water_needed_ml = max(water_needed_ml, maintenance_water * 0.3)
    
    # Cap at 4L
    water_needed_ml = min(water_needed_ml, 4000)
    
    # Calculate glasses
    glasses_needed = math.ceil(water_needed_ml / GLASS_SIZE)
    
    # Time to hydrate
    time_to_hydrate_minutes = math.ceil((water_needed_ml / HYDRATION_RATE) * 60)
    
    # Status message based on BAC
    if bac >= 0.15:
        status_text = "⚠️ Alto nivel de alcohol. ¡Hidrátate inmediatamente!"
        status_class = "status-danger"
    elif bac >= 0.08:
        status_text = "⚠️ Nivel significativo. Bebe agua con urgencia."
        status_class = "status-danger"
    elif bac >= 0.05:
        status_text = "⚠️ Nivel moderado. Necesitas hidratarte."
        status_class = "status-moderate"
    elif bac >= 0.02:
        status_text = "✅ Nivel bajo. Mantente hidratado."
        status_class = "status-safe"
    else:
        status_text = "✅ Nivel muy bajo. Sigue hidratándote bien."
        status_class = "status-safe"
    
    # Tips
    tips = []
    if bac > 0.05:
        tips.append("🕐 Espera al menos 1 hora antes de conducir por cada bebida estándar consumida.")
    if water_needed_ml > 1000:
        tips.append("💧 Bebe el agua de forma gradual, no toda de una vez. Tu cuerpo la absorberá mejor.")
    if request.time_elapsed < 2 and request.drink_count > 2:
        tips.append("⏰ Has consumido alcohol recientemente. Tómate tu tiempo para hidratarte.")
    tips.append("🥤 Los electrolitos (como en bebidas deportivas) pueden ayudar a una mejor hidratación.")
    if request.hydration_level == "dehydrated":
        tips.append("⚠️ Partías deshidratado. Aumenta tu consumo de agua en las próximas horas.")
    
    return HydrationResponse(
        water_needed_ml=water_needed_ml,
        glasses_needed=glasses_needed,
        time_to_hydrate_minutes=time_to_hydrate_minutes,
        bac=bac,
        status_text=status_text,
        status_class=status_class,
        tips=tips,
        total_alcohol_ml=total_alcohol_ml,
        total_alcohol_grams=total_alcohol_grams
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
