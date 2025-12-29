from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.routers.user import router as user_router
from app.routers.routine import router as routine_router
from app.routers.routine_exercise import router as routine_exercise_router
from app.routers.workout_session import router as workout_session_router
from app.routers.workout_set import router as workout_set_router
from app.routers.auth import router as auth_router
from app.routers.body_stats import router as body_stats_router
from app.routers.dashboard_stats import router as dashboard_stats_router
from app.database import SessionLocal
from app.models.muscle import Muscle
from app.models.exercise import Exercise
from app.models.exercise_secondary_muscle import ExerciseSecondaryMuscle
from app.models.bodyStats import BodyStats
from app.models.dashboardStats import DashboardStats
from fastapi.middleware.cors import CORSMiddleware

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

EXERCISES = [
    {
        "name": "Bench Press",
        "primary_muscle": "Chest",
        "secondary_muscles": ["Triceps", "Shoulders"],
    },
    {
        "name": "Lat Pulldown",
        "primary_muscle": "Back",
        "secondary_muscles": ["Biceps", "Shoulders"],
    },
    {
        "name": "Lateral Raises",
        "primary_muscle": "Shoulders",
        "secondary_muscles": ["Traps"],
    },
    {
        "name": "Hammer Curls", 
        "primary_muscle": "Biceps",
        "secondary_muscles": ["Forearms"],
    },
    {
        "name": "Tricep Cable Pushdown",
        "primary_muscle": "Triceps",
        "secondary_muscles": ["Shoulders"],
    },
    {
        "name": "Leg Press Machine",
        "primary_muscle": "Quadriceps",
        "secondary_muscles": ["Glutes", "Hamstrings"],
    },
]

@asynccontextmanager
async def lifespan(app: FastAPI):
    db = SessionLocal()
    try:
        # ------------ Seed MUSCLES ------------
        muscles_by_name: dict[str, Muscle] = {
            str(m.name): m for m in db.query(Muscle).all()
        }

        for name in MUSCLES:
            if name not in muscles_by_name:
                muscle = Muscle(name=name)
                db.add(muscle)
                db.flush()  # pour avoir muscle.id
                muscles_by_name[name] = muscle

        # ------------ Seed EXERCISES + secondary muscles ------------
        for data in EXERCISES:
            name = data["name"]
            primary_name = data["primary_muscle"]
            secondary_names = data["secondary_muscles"]

            # Muscle principal
            primary_muscle = muscles_by_name.get(primary_name)
            if not primary_muscle:
                primary_muscle = Muscle(name=primary_name)
                db.add(primary_muscle)
                db.flush()
                muscles_by_name[primary_name] = primary_muscle

            # Exercice
            exercise = db.query(Exercise).filter(Exercise.name == name).first()
            if not exercise:
                exercise = Exercise(
                    name=name,
                    primary_muscle=primary_muscle.id,
                )
                db.add(exercise)
                db.flush()  # pour avoir exercise.id

            # Muscles secondaires
            for sec_name in secondary_names:
                sec_muscle = muscles_by_name.get(sec_name)
                if not sec_muscle:
                    sec_muscle = Muscle(name=sec_name)
                    db.add(sec_muscle)
                    db.flush()
                    muscles_by_name[sec_name] = sec_muscle

                # Vérifie si la relation existe déjà
                exists = (
                    db.query(ExerciseSecondaryMuscle)
                    .filter(
                        ExerciseSecondaryMuscle.exercise_id == exercise.id,
                        ExerciseSecondaryMuscle.muscle_id == sec_muscle.id,
                    )
                    .first()
                )

                if not exists:
                    db.add(
                        ExerciseSecondaryMuscle(
                            exercise_id=exercise.id,
                            muscle_id=sec_muscle.id,
                        )
                    )

        db.commit()
        print("✅ Muscles + exercises seeded on startup.")
    except Exception as e:
        db.rollback()
        print("❌ Error seeding data:", e)
    finally:
        db.close()

    # --------- API running ---------
    yield

    print("🛑 API shutting down...")


app = FastAPI(lifespan=lifespan)
app = FastAPI()
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,      # en dev tu peux mettre ["*"] si tu veux
    allow_credentials=True,
    allow_methods=["*"],        # autorise GET, POST, etc.
    allow_headers=["*"],        # autorise tous les headers (Content-Type, Authorization, ...)
)

app.include_router(user_router)
app.include_router(routine_router)
app.include_router(routine_exercise_router)
app.include_router(workout_session_router)
app.include_router(workout_set_router)
app.include_router(auth_router)
app.include_router(body_stats_router)
app.include_router(dashboard_stats_router)


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/")
def root():
    return {"message": "Sport API backend is running 🚀"}

