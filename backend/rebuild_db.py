from sqlalchemy import text
from app.database import engine, Base

# ⚠️ très important : importer TOUS tes models ici
from app.models.user import User
from app.models.muscle import Muscle
from app.models.exercise import Exercise
from app.models.exercise_secondary_muscle import ExerciseSecondaryMuscle
from app.models.routine import Routine
from app.models.routine_exercise import RoutineExercise
from app.models.workout_session import WorkoutSession
from app.models.workout_set import WorkoutSet

if __name__ == "__main__":
    print("⚠️ Reset complet du schema 'public'...")

    with engine.connect() as conn:
        conn.execute(text("DROP SCHEMA public CASCADE;"))
        conn.execute(text("CREATE SCHEMA public;"))
        conn.commit()

    print("🔁 Recréation des tables à partir des models SQLAlchemy...")
    Base.metadata.create_all(bind=engine)
    print("✅ Base de données rebuild avec succès.")
