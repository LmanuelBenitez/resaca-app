# backend/seed.py
from app.core.database import SessionLocal
from app.models.alcohol import Alcohol

def seed_alcohols():
    """Insertar tipos de alcohol predefinidos."""
    db = SessionLocal()
    
    try:
        # Verificar si ya hay datos
        count = db.query(Alcohol).count()
        if count > 0:
            print(f"⚠️ Ya hay {count} tipos de alcohol en la base de datos")
            return
        
        # Tipos de alcohol predefinidos
        alcohols = [
            {"name": "Cerveza", "alcohol_percentage": 5.0, "serving_size": 330.0},
            {"name": "Vino", "alcohol_percentage": 12.0, "serving_size": 150.0},
            {"name": "Whisky", "alcohol_percentage": 40.0, "serving_size": 50.0},
            {"name": "Vodka", "alcohol_percentage": 40.0, "serving_size": 50.0},
            {"name": "Ron", "alcohol_percentage": 40.0, "serving_size": 50.0},
            {"name": "Tequila", "alcohol_percentage": 38.0, "serving_size": 50.0},
        ]
        
        for data in alcohols:
            alcohol = Alcohol(**data)
            db.add(alcohol)
        
        db.commit()
        print(f"✅ {len(alcohols)} tipos de alcohol agregados")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error al insertar datos: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_alcohols()