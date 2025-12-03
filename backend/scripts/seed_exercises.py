from app.database import SessionLocal
from app.models.muscle import Muscle
from app.models.exercise import Exercise
from app.models.exercise_secondary_muscle import ExerciseSecondaryMuscle

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


def seed_exercises():
    db = SessionLocal()
    try:
        muscles_by_name = {m.name: m for m in db.query(Muscle).all()}

        for data in EXERCISES:
            name = data["name"]
            primary_name = data["primary_muscle"]
            secondary_names = data["secondary_muscles"]

            # 1) Récupérer / créer le muscle principal
            primary_muscle = muscles_by_name.get(primary_name)
            if not primary_muscle:
                primary_muscle = Muscle(name=primary_name)
                db.add(primary_muscle)
                db.flush()
                muscles_by_name[primary_name] = primary_muscle

            # 2) Récupérer / créer l'exercice
            exercise = db.query(Exercise).filter(Exercise.name == name).first()
            if not exercise:
                exercise = Exercise(
                    name=name,
                    primary_muscle=primary_muscle.id,
                )
                db.add(exercise)
                db.flush()

            # 3) Gérer les muscles secondaires
            for sec_name in secondary_names:
                sec_muscle = muscles_by_name.get(sec_name)
                if not sec_muscle:
                    sec_muscle = Muscle(name=sec_name)
                    db.add(sec_muscle)
                    db.flush()
                    muscles_by_name[sec_name] = sec_muscle

                # Vérifier si la relation existe déjà
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
        print("✅ Exercises + secondary muscles seeded")
    except Exception as e:
        db.rollback()
        print("❌ Error seeding exercises:", e)
    finally:
        db.close()


if __name__ == "__main__":
    seed_exercises()
