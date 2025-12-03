from app.database import SessionLocal
from app.models.muscle import Muscle

MUSCLES = [
    "Chest",
    "Back",
    "Shoulders",
    "Biceps",
    "Triceps",
    "Quadriceps",
    "Hamstrings",
    "Glutes",
    "Calves",
    "Abs",
    "Forearms",
    "Traps",
    "Lower back",
]

def seed_muscles():
    db = SessionLocal()
    try:
        for name in MUSCLES:
            exists = db.query(Muscle).filter(Muscle.name == name).first()
            if not exists:
                db.add(Muscle(name=name))
        db.commit()
        print("✅ Muscles seeded")
    except Exception as e:
        db.rollback()
        print("❌ Error seeding muscles:", e)
    finally:
        db.close()

if __name__ == "__main__":
    seed_muscles()