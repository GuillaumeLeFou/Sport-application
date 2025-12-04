CREATE TABLE "User" (
  "id" serial PRIMARY KEY,
  "username" varchar,
  "password" varchar,
  "firstname" varchar,
  "lastname" varchar,
  "age" integer,
  "weight" float,
  "height" float
);

CREATE TABLE "Exercise" (
  "id" serial PRIMARY KEY,
  "name" varchar,
  "primary_muscle" int
);

CREATE TABLE "Muscle" (
  "id" serial PRIMARY KEY,
  "name" varchar
);

CREATE TABLE "ExerciseSecondaryMuscle" (
  "id" serial PRIMARY KEY,
  "exercise_id" int,
  "muscle_id" int
);

CREATE TABLE "Routine" (
  "id" serial PRIMARY KEY,
  "user_id" integer,
  "name" varchar,
  "description" varchar
);

CREATE TABLE "RoutineExercise" (
  "id" serial PRIMARY KEY,
  "routine_id" integer,
  "exercise_id" integer,
  "position" int,
  "target_sets" int,
  "target_reps" int,
  "target_weight" float
);

CREATE TABLE "WorkoutSession" (
  "id" serial PRIMARY KEY,
  "user_id" integer,
  "routine_id" integer,
  "performed_at" timestamptz
);

CREATE TABLE "WorkoutSet" (
  "id" serial PRIMARY KEY,
  "session_id" integer,
  "exercise_id" integer,
  "set_number" int,
  "weight" float,
  "reps" int
);

ALTER TABLE "Exercise" ADD FOREIGN KEY ("primary_muscle") REFERENCES "Muscle" ("id");

ALTER TABLE "ExerciseSecondaryMuscle" ADD FOREIGN KEY ("exercise_id") REFERENCES "Exercise" ("id");

ALTER TABLE "ExerciseSecondaryMuscle" ADD FOREIGN KEY ("muscle_id") REFERENCES "Muscle" ("id");

ALTER TABLE "Routine" ADD FOREIGN KEY ("user_id") REFERENCES "User" ("id");

ALTER TABLE "RoutineExercise" ADD FOREIGN KEY ("routine_id") REFERENCES "Routine" ("id");

ALTER TABLE "RoutineExercise" ADD FOREIGN KEY ("exercise_id") REFERENCES "Exercise" ("id");

ALTER TABLE "WorkoutSession" ADD FOREIGN KEY ("user_id") REFERENCES "User" ("id");

ALTER TABLE "WorkoutSession" ADD FOREIGN KEY ("routine_id") REFERENCES "Routine" ("id");

ALTER TABLE "WorkoutSet" ADD FOREIGN KEY ("session_id") REFERENCES "WorkoutSession" ("id");

ALTER TABLE "WorkoutSet" ADD FOREIGN KEY ("exercise_id") REFERENCES "Exercise" ("id");
