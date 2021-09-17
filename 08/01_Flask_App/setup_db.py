import sqlite3
from sqlite3 import Error
from werkzeug.security import generate_password_hash, check_password_hash


def create_tables(conn):
    cur = conn.cursor()
    try:
        sql_users = """ 
            CREATE TABLE users(
                id INTEGER PRIMARY KEY,
                username TEXT NOT NULL,
                email TEXT NOT NULL,
                passwordhash VARCHAR(120) NOT NULL,
                role TEXT,
                UNIQUE(username),
                UNIQUE(email)
            )
        """
        sql_exercises = """ 
            CREATE TABLE exercises(
                userid INTEGER,
                exercise_id INTEGER PRIMARY KEY,
                exercise_name TEXT NOT NULL,
                category TEXT NOT NULL,
                body_part TEXT NOT NULL,
                global_exercise INTEGER NOT NULL,
                FOREIGN KEY(userid) REFERENCES users(id)
            )
        """
        sql_workouts = """ 
            CREATE TABLE workouts(
                workout_id INTEGER,
                userid INTEGER,
                title TEXT,
                exercise_id INTEGER,
                exercise TEXT NOT NULL,
                sets INTEGER,
                reps INTEGER,
                weight REAL,
                date TEXT NOT NULL,
                FOREIGN KEY(exercise) REFERENCES exercise(exercise_name),
                FOREIGN KEY(userid) REFERENCES users(id),
                FOREIGN KEY(exercise_id) REFERENCES exercise(exercise_id)
            )
        """
        cur.execute(sql_users)
        cur.execute(sql_exercises)
        cur.execute(sql_workouts)
        conn.commit()
    except sqlite3.Error as e:
        print(e)
    else:
        print("table created")
    finally:
        cur.close()


def dummy_workouts(conn):
    cur = conn.cursor()
    try:
        sql = """ INSERT INTO workouts(workout_id, userid, title, exercise_id, exercise, sets, reps, weight, date) VALUES 
        (1, 1, "Chest Day", (SELECT exercise_id FROM exercises WHERE exercise_name = "Bench Press"), "Bench Press", 3, 3, 80, "2021-04-19"),
        (1, 1, "Chest Day", (SELECT exercise_id FROM exercises WHERE exercise_name = "Dumbbell Press"), "Dumbbell Press", 3, 3, 80, "2021-04-19"),
        (2, 2, "Back Day", (SELECT exercise_id FROM exercises WHERE exercise_name = "Deadlift"), "Deadlift", 3, 3, 80, "2021-04-19"),
        (2, 2, "Back Day", (SELECT exercise_id FROM exercises WHERE exercise_name = "Barbell Row"), "Barbell Row", 3, 3, 20, "2021-04-19"),
        (2, 2, "Back Day", (SELECT exercise_id FROM exercises WHERE exercise_name = "Pull Up"), "Pull Up", 3, 3, 0, "2021-04-19"),
        (3, 3, "Leg Day", (SELECT exercise_id FROM exercises WHERE exercise_name = "Squats"), "Squats", 3, 3, 90, "2021-04-19"),
        (3, 3, "Leg Day", (SELECT exercise_id FROM exercises WHERE exercise_name = "Bulgarian Split Squats"), "Bulgarian Split Squats", 3, 3, 16, "2021-04-19"),
        (3, 3, "Leg Day", (SELECT exercise_id FROM exercises WHERE exercise_name = "Leg Raises"), "Leg Raises", 3, 3, 87.5, "2021-04-19"),
        (4, 3, "Chest Day", (SELECT exercise_id FROM exercises WHERE exercise_name = "Dumbbell Press"), "Dumbbell Press", 3, 3, 80, "2021-04-20"),
        (4, 3, "Chest Day", (SELECT exercise_id FROM exercises WHERE exercise_name = "Cable Crossover"), "Cable Crossover", 3, 3, 80, "2021-04-20"),
        (4, 3, "Chest Day", (SELECT exercise_id FROM exercises WHERE exercise_name = "Incline Bench Press"), "Incline Bench Press", 3, 3, 80, "2021-04-20"),
        (5, 1, "Shoulders", (SELECT exercise_id FROM exercises WHERE exercise_name = "Lateral Raise"), "Lateral Raise", 5, 5, 15, "2021-04-21"),
        (5, 1, "Shoulders", (SELECT exercise_id FROM exercises WHERE exercise_name = "Seated Overhead Press"), "Seated Overhead Press", 3, 3, 50, "2021-04-21"),
        (6, 3, "Legs", (SELECT exercise_id FROM exercises WHERE exercise_name = "Squats"), "Squats", 5, 5, 90, "2021-04-21"),
        (6, 3, "Legs", (SELECT exercise_id FROM exercises WHERE exercise_name = "Bulgarian Split Squats"), "Bulgarian Split Squats", 3, 10, 16, "2021-04-21"),
        (6, 3, "Legs", (SELECT exercise_id FROM exercises WHERE exercise_name = "Lying Leg Curls"), "Lying Leg Curls", 4, 8, 80, "2021-04-21"),
        (6, 3, "Legs", (SELECT exercise_id FROM exercises WHERE exercise_name = "Leg Extensions"), "Leg Extensions", 4, 8, 80, "2021-04-21"),
        (7, 1, "Back Workout", (SELECT exercise_id FROM exercises WHERE exercise_name = "Pull Up"), "Pull Up", 5, 5, 140, "2021-04-25"),
        (7, 1, "Back Workout", (SELECT exercise_id FROM exercises WHERE exercise_name = "Deadlift"), "Deadlift", 3, 4, 50, "2021-04-25"),
        (7, 1, "Back Workout", (SELECT exercise_id FROM exercises WHERE exercise_name = "Bent Over Rows"), "Bent Over Rows", 3, 4, 50, "2021-04-25"),
        (7, 1, "Back Workout", (SELECT exercise_id FROM exercises WHERE exercise_name = "T Bar Row"), "T Bar Row", 3, 4, 50, "2021-04-25"),
        (8, 1, "Push", (SELECT exercise_id FROM exercises WHERE exercise_name = "Bench Press"), "Bench Press", 5, 5, 90, "2021-04-26"),
        (8, 1, "Push", (SELECT exercise_id FROM exercises WHERE exercise_name = "Dumbbell Press"), "Dumbbell Press", 3, 4, 25, "2021-04-26"),
        (8, 1, "Push", (SELECT exercise_id FROM exercises WHERE exercise_name = "Cable Crossover"), "Cable Crossover", 3, 4, 50, "2021-04-26"),
        (8, 1, "Push", (SELECT exercise_id FROM exercises WHERE exercise_name = "Chest Dip"), "Chest Dip", 3, 4, 24, "2021-04-26"),
        (9, 1, "Pull", (SELECT exercise_id FROM exercises WHERE exercise_name = "Barbell Row"), "Barbell Row", 5, 5, 60, "2021-04-27"),
        (9, 1, "Pull", (SELECT exercise_id FROM exercises WHERE exercise_name = "Bicep Curl"), "Bicep Curl", 3, 4, 20, "2021-04-27"),
        (9, 1, "Pull", (SELECT exercise_id FROM exercises WHERE exercise_name = "Concentration Curl"), "Concentration Curl", 4, 4, 14, "2021-04-27"),
        (9, 1, "Pull", (SELECT exercise_id FROM exercises WHERE exercise_name = "Skullcrusher"), "Skullcrusher", 3, 4, 40, "2021-04-27"),

        (10, 3, "Legs", (SELECT exercise_id FROM exercises WHERE exercise_name = "Squats"), "Squats", 5, 5, 90, "2021-04-21"),
        (10, 3, "Legs", (SELECT exercise_id FROM exercises WHERE exercise_name = "Bulgarian Split Squats"), "Bulgarian Split Squats", 3, 10, 16, "2021-04-21"),
        (10, 3, "Legs", (SELECT exercise_id FROM exercises WHERE exercise_name = "Lying Leg Curls"), "Lying Leg Curls", 4, 8, 80, "2021-04-21"),
        (10, 3, "Legs", (SELECT exercise_id FROM exercises WHERE exercise_name = "Leg Extensions"), "Leg Extensions", 4, 8, 80, "2021-04-21"),
        (11, 2, "Back Workout", (SELECT exercise_id FROM exercises WHERE exercise_name = "Pull Up"), "Pull Up", 5, 5, 140, "2021-04-25"),
        (11, 2, "Back Workout", (SELECT exercise_id FROM exercises WHERE exercise_name = "Deadlift"), "Deadlift", 3, 4, 50, "2021-04-25"),
        (11, 2, "Back Workout", (SELECT exercise_id FROM exercises WHERE exercise_name = "Bent Over Rows"), "Bent Over Rows", 3, 4, 50, "2021-04-25"),
        (11, 2, "Back Workout", (SELECT exercise_id FROM exercises WHERE exercise_name = "T Bar Row"), "T Bar Row", 3, 4, 50, "2021-04-25"),
        (12, 2, "Push", (SELECT exercise_id FROM exercises WHERE exercise_name = "Bench Press"), "Bench Press", 5, 5, 90, "2021-04-26"),
        (12, 2, "Push", (SELECT exercise_id FROM exercises WHERE exercise_name = "Dumbbell Press"), "Dumbbell Press", 3, 4, 25, "2021-04-26"),
        (12, 2, "Push", (SELECT exercise_id FROM exercises WHERE exercise_name = "Cable Crossover"), "Cable Crossover", 3, 4, 50, "2021-04-26"),
        (12, 2, "Push", (SELECT exercise_id FROM exercises WHERE exercise_name = "Chest Dip"), "Chest Dip", 3, 4, 24, "2021-04-26"),
        (13, 2, "Pull", (SELECT exercise_id FROM exercises WHERE exercise_name = "Barbell Row"), "Barbell Row", 5, 5, 60, "2021-04-27"),
        (13, 2, "Pull", (SELECT exercise_id FROM exercises WHERE exercise_name = "Bicep Curl"), "Bicep Curl", 3, 4, 20, "2021-04-27"),
        (13, 2, "Pull", (SELECT exercise_id FROM exercises WHERE exercise_name = "Concentration Curl"), "Concentration Curl", 4, 4, 14, "2021-04-27"),
        (13, 2, "Pull", (SELECT exercise_id FROM exercises WHERE exercise_name = "Skullcrusher"), "Skullcrusher", 3, 4, 40, "2021-04-27"),

        (14, 3, "Legs", (SELECT exercise_id FROM exercises WHERE exercise_name = "Squats"), "Squats", 5, 5, 90, "2021-04-21"),
        (14, 3, "Legs", (SELECT exercise_id FROM exercises WHERE exercise_name = "Bulgarian Split Squats"), "Bulgarian Split Squats", 3, 10, 16, "2021-04-21"),
        (14, 3, "Legs", (SELECT exercise_id FROM exercises WHERE exercise_name = "Lying Leg Curls"), "Lying Leg Curls", 4, 8, 80, "2021-04-21"),
        (14, 3, "Legs", (SELECT exercise_id FROM exercises WHERE exercise_name = "Leg Extensions"), "Leg Extensions", 4, 8, 80, "2021-04-21"),
        (15, 3, "Back Workout", (SELECT exercise_id FROM exercises WHERE exercise_name = "Pull Up"), "Pull Up", 5, 5, 140, "2021-04-25"),
        (15, 3, "Back Workout", (SELECT exercise_id FROM exercises WHERE exercise_name = "Deadlift"), "Deadlift", 3, 4, 50, "2021-04-25"),
        (15, 3, "Back Workout", (SELECT exercise_id FROM exercises WHERE exercise_name = "Bent Over Rows"), "Bent Over Rows", 3, 4, 50, "2021-04-25"),
        (15, 3, "Back Workout", (SELECT exercise_id FROM exercises WHERE exercise_name = "T Bar Row"), "T Bar Row", 3, 4, 50, "2021-04-25"),
        (16, 3, "Push", (SELECT exercise_id FROM exercises WHERE exercise_name = "Bench Press"), "Bench Press", 5, 5, 90, "2021-04-26"),
        (16, 3, "Push", (SELECT exercise_id FROM exercises WHERE exercise_name = "Dumbbell Press"), "Dumbbell Press", 3, 4, 25, "2021-04-26"),
        (16, 3, "Push", (SELECT exercise_id FROM exercises WHERE exercise_name = "Cable Crossover"), "Cable Crossover", 3, 4, 50, "2021-04-26"),
        (16, 3, "Push", (SELECT exercise_id FROM exercises WHERE exercise_name = "Chest Dip"), "Chest Dip", 3, 4, 24, "2021-04-26"),
        (17, 3, "Pull", (SELECT exercise_id FROM exercises WHERE exercise_name = "Barbell Row"), "Barbell Row", 5, 5, 60, "2021-04-27"),
        (17, 3, "Pull", (SELECT exercise_id FROM exercises WHERE exercise_name = "Bicep Curl"), "Bicep Curl", 3, 4, 20, "2021-04-27"),
        (17, 3, "Pull", (SELECT exercise_id FROM exercises WHERE exercise_name = "Concentration Curl"), "Concentration Curl", 4, 4, 14, "2021-04-27"),
        (17, 3, "Pull", (SELECT exercise_id FROM exercises WHERE exercise_name = "Skullcrusher"), "Skullcrusher", 3, 4, 40, "2021-04-27"),

        (18, 3, "Legs", (SELECT exercise_id FROM exercises WHERE exercise_name = "Squats"), "Squats", 5, 5, 90, "2021-04-11"),
        (18, 3, "Legs", (SELECT exercise_id FROM exercises WHERE exercise_name = "Bulgarian Split Squats"), "Bulgarian Split Squats", 3, 10, 16, "2021-04-11"),
        (18, 3, "Legs", (SELECT exercise_id FROM exercises WHERE exercise_name = "Lying Leg Curls"), "Lying Leg Curls", 4, 8, 80, "2021-04-11"),
        (18, 3, "Legs", (SELECT exercise_id FROM exercises WHERE exercise_name = "Leg Extensions"), "Leg Extensions", 4, 8, 80, "2021-04-11"),
        (19, 3, "Legs", (SELECT exercise_id FROM exercises WHERE exercise_name = "Squats"), "Squats", 5, 5, 80, "2021-04-09"),
        (20, 3, "Legs", (SELECT exercise_id FROM exercises WHERE exercise_name = "Squats"), "Squats", 5, 5, 60, "2021-04-08"),

        (21, 1, "Legs", (SELECT exercise_id FROM exercises WHERE exercise_name = "Squats"), "Squats", 5, 5, 90, "2021-04-11"),
        (21, 1, "Legs", (SELECT exercise_id FROM exercises WHERE exercise_name = "Bulgarian Split Squats"), "Bulgarian Split Squats", 3, 10, 16, "2021-04-11"),
        (21, 1, "Legs", (SELECT exercise_id FROM exercises WHERE exercise_name = "Lying Leg Curls"), "Lying Leg Curls", 4, 8, 80, "2021-04-11"),
        (21, 1, "Legs", (SELECT exercise_id FROM exercises WHERE exercise_name = "Leg Extensions"), "Leg Extensions", 4, 8, 80, "2021-04-11"),
        (22, 1, "Legs", (SELECT exercise_id FROM exercises WHERE exercise_name = "Squats"), "Squats", 5, 5, 80, "2021-04-09"),
        (23, 1, "Legs", (SELECT exercise_id FROM exercises WHERE exercise_name = "Squats"), "Squats", 5, 5, 60, "2021-04-08"),

        (24, 2, "Legs", (SELECT exercise_id FROM exercises WHERE exercise_name = "Squats"), "Squats", 5, 5, 90, "2021-04-11"),
        (24, 2, "Legs", (SELECT exercise_id FROM exercises WHERE exercise_name = "Bulgarian Split Squats"), "Bulgarian Split Squats", 3, 10, 16, "2021-04-11"),
        (24, 2, "Legs", (SELECT exercise_id FROM exercises WHERE exercise_name = "Lying Leg Curls"), "Lying Leg Curls", 4, 8, 80, "2021-04-11"),
        (24, 2, "Legs", (SELECT exercise_id FROM exercises WHERE exercise_name = "Leg Extensions"), "Leg Extensions", 4, 8, 80, "2021-04-11"),
        (25, 2, "Legs", (SELECT exercise_id FROM exercises WHERE exercise_name = "Squats"), "Squats", 5, 5, 80, "2021-04-09"),
        (26, 2, "Legs", (SELECT exercise_id FROM exercises WHERE exercise_name = "Squats"), "Squats", 5, 5, 60, "2021-04-08")
        """
        cur.execute(sql,)
        conn.commit()
    except sqlite3.Error as err:
        print("Error: {}".format(err))
    finally:
        cur.close()


def default_exercises(conn):
    cur = conn.cursor()
    try:
        sql = """ INSERT INTO exercises(userid, exercise_name, category, body_part, global_exercise) VALUES 
        (3, "Concentration Curl", "Dumbbell", "Arms", 1),
        (3, "Incline Curl", "Dumbbell", "Arms", 1),
        (3, "Bicep Curl", "Dumbbell", "Arms", 1),
        (3, "Tricep Extension", "Cable", "Arms", 1),
        (3, "Skullcrusher", "Barbell", "Arms", 1),
        (3, "Tricep Pushdown", "Cable", "Arms", 1),

        (3,	"Deadlift",	"Barbell", "Back", 1),
        (3,	"Bent Over Rows", "Barbell", "Back", 1),
        (3, "Barbell Row", "Barbell", "Back", 1),
        (3, "Lat Pulldown", "Cable", "Back", 1),
        (3, "Seated Row", "Machine", "Back", 1),
        (3, "T Bar Row", "Barbell", "Back", 1),
        (3, "Pull Up", "Bodyweight", "Back", 1),

        (3,	"Sit Up", "Bodyweight", "Core", 1),
        (3, "Ab Wheel", "Bodyweight", "Core", 1),
        (3, "Cable Crunch", "Cable", "Core", 1),
        (3, "Leg Raises", "Bodyweight", "Core", 1),
        (3, "Decline Crunch", "Bodyweight", "Core", 1),

        (3, "Bench Press", "Barbell", "Chest", 1),
        (3,	"Dumbbell Press", "Dumbbell" ,"Chest", 1),
        (3,	"Push ups",	"Bodyweight", "Chest", 1),
        (3, "Chest Dip", "Bodyweight", "Chest", 1),
        (3, "Cable Crossover", "Cable", "Chest", 1),
        (3, "Incline Bench Press", "Barbell", "Chest", 1),
        (3, "Pec Dec", "Machine", "Chest", 1),

        (3,	"Squats", "Barbell", "Legs", 1),
        (3,	"Bulgarian Split Squats" ,"Dumbbell", "Legs", 1),
        (3, "Lying Leg Curls", "Machine", "Legs", 1),
        (3, "Leg Extensions", "Machine", "Legs", 1),
        (3, "Box Jump", "Other", "Legs", 1),
        (3, "Calf Press", "Machine", "Legs", 1),

        (3, "Arnold Press", "Dumbbell", "Shoulders", 1),
        (3, "Military Press", "Barbell", "Shoulders", 1),
        (3, "Seated Overhead Press", "Dumbbell", "Shoulders", 1),
        (3, "Face Pull", "Cable", "Shoulders", 1),
        (3, "Lateral Raise", "Dumbbell", "Shoulders", 1),
        (3, "Z Press", "Barbell", "Shoulders", 1),
        (3, "Push Press", "Barbell", "Shoulders", 1),

        (3, "Stretching", "Other", "Other", 1),

        (3,	"Clean & Jerk",	"Barbell", "Olympic", 1),
        (3,	"Snatch", "Barbell", "Olympic", 1),
        (3, "Clean", "Barbell", "Olympic", 1),
        (3, "Deadlift High Pull", "Barbell", "Olympic", 1),
        (3, "Hang Clean", "Barbell", "Olympic", 1),

        (3, "Burpee", "Bodyweight", "Full Body", 1),
        (3, "Muscle Up", "Bodyweight", "Full Body", 1),
        (3, "Squat Row", "Other", "Full Body", 1),
        (3, "Thruster", "Barbell", "Full Body", 1),

        (3, "Climbing", "Other", "Cardio", 1),
        (3, "Cycling", "Other", "Cardio", 1),
        (3, "Hiking", "Other", "Cardio", 1),
        (3, "Jump Rope", "Other", "Cardio", 1),
        (3, "Rowing", "Other", "Cardio", 1)
        """
        cur.execute(sql,)
        conn.commit()
    except sqlite3.Error as err:
        print("Error: {}".format(err))
    finally:
        cur.close()

def add_user(conn, username, email, hash, role="default"):
    """Add user. Returns the new user id"""
    cur = conn.cursor()
    try:
        sql = ("INSERT INTO users (username, email, passwordhash, role) VALUES (?,?,?,?)")
        cur.execute(sql, (username, email, hash, role))
        conn.commit()
    except sqlite3.Error as err:
        print("Error: {}".format(err))
        return -1
    else:
        print("User {} created with id {}.".format(username, cur.lastrowid))
        return cur.lastrowid
    finally:
        cur.close()


if __name__ == "__main__":
    try:
        conn = sqlite3.connect("database.db")
        cur = conn.cursor()
    except sqlite3.Error as err:
        print(err)
    else:
        create_tables(conn)
        add_user(conn, "user1", "user1@user.com" ,generate_password_hash("demo"))
        add_user(conn, "user2", "user2@user.com" ,generate_password_hash("demo"))
        add_user(conn, "admin", "admin@user.com" ,generate_password_hash("admin"), "admin")
        default_exercises(conn)
        dummy_workouts(conn)

        conn.close()
