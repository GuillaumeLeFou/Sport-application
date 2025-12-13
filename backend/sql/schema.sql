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

-- 1) PR par exercice (max weight + best estimated 1RM)
CREATE TABLE "ExercisePR" (
  "id" serial PRIMARY KEY,
  "user_id" integer NOT NULL,
  "exercise_id" integer NOT NULL,

  "pr_type" varchar NOT NULL,         -- 'max_weight' | 'best_1rm_est'
  "pr_value" float NOT NULL,

  "achieved_at" timestamptz NOT NULL,
  "session_id" integer,
  "set_id" integer,

  "created_at" timestamptz DEFAULT now()
);

-- 1 PR par type / user / exercise
CREATE UNIQUE INDEX "idx_exercise_pr_unique"
ON "ExercisePR" ("user_id", "exercise_id", "pr_type");

CREATE INDEX "idx_exercise_pr_user"
ON "ExercisePR" ("user_id");

CREATE INDEX "idx_exercise_pr_exercise"
ON "ExercisePR" ("exercise_id");


-- 2) Stats agrégées par exercice et période (jour/semaine/mois)
-- Pour afficher des graphs rapidement (volume, max weight, 1RM, sets, reps…)
CREATE TABLE "ExerciseStats" (
  "id" serial PRIMARY KEY,

  "user_id" integer NOT NULL,
  "exercise_id" integer NOT NULL,

  "period_type" varchar NOT NULL,     -- 'day' | 'week' | 'month'
  "period_start" date NOT NULL,
  "period_end" date NOT NULL,

  "total_sets" int NOT NULL DEFAULT 0,
  "total_reps" int NOT NULL DEFAULT 0,
  "total_volume" float NOT NULL DEFAULT 0,  -- sum(weight * reps)

  "max_weight" float,
  "best_1rm_est" float,

  "avg_weight" float,
  "avg_reps" float,

  "updated_at" timestamptz DEFAULT now()
);

CREATE UNIQUE INDEX "idx_exercise_stats_unique"
ON "ExerciseStats" ("user_id", "exercise_id", "period_type", "period_start", "period_end");

CREATE INDEX "idx_exercise_stats_user_period"
ON "ExerciseStats" ("user_id", "period_type", "period_start");


-- 3) Dashboard stats (Top 8) - global par période
-- 1 ligne = toutes les cartes du dashboard
CREATE TABLE "DashboardStats" (
  "id" serial PRIMARY KEY,

  "user_id" integer NOT NULL,

  "period_type" varchar NOT NULL,     -- 'week' | 'month' | 'all'
  "period_start" date NOT NULL,
  "period_end" date NOT NULL,
  "total_volume" float NOT NULL DEFAULT 0,   -- 1) volume période
  "total_sessions" int NOT NULL DEFAULT 0,   -- 2) nb séances
  "current_streak" int NOT NULL DEFAULT 0,   -- 3) streak (ex: semaines)
  "pr_count" int NOT NULL DEFAULT 0,         -- 4) nb PR sur période

  "key_exercise_id" integer,                 -- 5) exo clé (bench/squat…)
  "key_exercise_1rm" float,                  -- 5) e1RM actuel sur période

  "top_muscle_id" integer,                   -- 6) muscle le plus travaillé
  "top_muscle_volume" float,                 -- 6) volume associé

  "body_weight" float,                       -- 7) poids actuel
  "body_weight_delta" float,                 -- 7) delta vs période précédente

  "goal_value" float,                        -- 8) objectif (ex: 80 kg)
  "goal_current" float,                      -- 8) valeur actuelle
  "goal_progress_percent" float,             -- 8) %

  "updated_at" timestamptz DEFAULT now()
);

CREATE UNIQUE INDEX "idx_dashboard_stats_unique"
ON "DashboardStats" ("user_id", "period_type", "period_start", "period_end");

CREATE INDEX "idx_dashboard_stats_user"
ON "DashboardStats" ("user_id");

CREATE TABLE "BodyStats" (
  "id" serial PRIMARY KEY,
  "user_id" integer NOT NULL,

  "measured_at" date NOT NULL,
  "body_weight" float NOT NULL,

  "notes" varchar,
  "created_at" timestamptz DEFAULT now()
);

CREATE UNIQUE INDEX "idx_body_stats_unique"
ON "BodyStats" ("user_id", "measured_at");

CREATE INDEX "idx_body_stats_user_date"
ON "BodyStats" ("user_id", "measured_at");


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

ALTER TABLE "ExercisePR" ADD FOREIGN KEY ("user_id") REFERENCES "User" ("id");
ALTER TABLE "ExercisePR" ADD FOREIGN KEY ("exercise_id") REFERENCES "Exercise" ("id");
ALTER TABLE "ExercisePR" ADD FOREIGN KEY ("session_id") REFERENCES "WorkoutSession" ("id");
ALTER TABLE "ExercisePR" ADD FOREIGN KEY ("set_id") REFERENCES "WorkoutSet" ("id");

ALTER TABLE "ExerciseStats" ADD FOREIGN KEY ("user_id") REFERENCES "User" ("id");
ALTER TABLE "ExerciseStats" ADD FOREIGN KEY ("exercise_id") REFERENCES "Exercise" ("id");

ALTER TABLE "DashboardStats" ADD FOREIGN KEY ("user_id") REFERENCES "User" ("id");
ALTER TABLE "DashboardStats" ADD FOREIGN KEY ("key_exercise_id") REFERENCES "Exercise" ("id");
ALTER TABLE "DashboardStats" ADD FOREIGN KEY ("top_muscle_id") REFERENCES "Muscle" ("id");

ALTER TABLE "BodyStats" ADD FOREIGN KEY ("user_id") REFERENCES "User" ("id");
