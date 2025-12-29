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
from app.models.bodyStats import BodyStats
from app.models.dashboardStats import DashboardStats

if __name__ == "__main__":
    print("⚠️ Complete reset of the database in progress...")

    with engine.connect() as conn:
        conn.execute(text("DROP SCHEMA public CASCADE;"))
        conn.execute(text("CREATE SCHEMA public;"))
        conn.commit()
    Base.metadata.create_all(bind=engine)
    print("✅ Data base rebuilt with success.")