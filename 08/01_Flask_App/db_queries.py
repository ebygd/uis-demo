import sqlite3
from sqlite3 import Error
from werkzeug.security import generate_password_hash, check_password_hash



def get_hash_from_username(conn, username):
    """Return the hash for a user, to check password match"""
    cur = conn.cursor()
    try:
        sql = """SELECT passwordhash FROM users WHERE username = ?"""
        cur.execute(sql, (username,))
        return cur.fetchone()
    except sqlite3.Error as err:
        print("Error: {}".format(err))
    finally:
        cur.close()


def get_user_by_name(conn, username):
    """Get user details by name."""
    cur = conn.cursor()
    try:
        sql = ("SELECT id, username, email, role FROM users WHERE username = ?")
        cur.execute(sql, (username,))
        for row in cur:
            (id, name, email, role) = row
            return {
                "id": id,
                "username": name,
                "email": email,
                "role": role
            }
        else:
            # user does not exist
            return {
                "username": username,
                # før: userid: None, endrer til id: pass på bugs!
                "id": None,
                "role": None
            }
    except sqlite3.Error as err:
        print("Error: {}".format(err))
    finally:
        cur.close()


def load_exercises_for_userid(conn, userid):
    """Load all exercises a user has in their db"""
    cur = conn.cursor()
    try:        
        sql = (""" SELECT * FROM exercises WHERE userid = ? OR global_exercise = 1 """)
        cur.execute(sql, (userid, ))
        exercises = []
        for row in cur:
            (userid, exercise_id, exercise_name, category, body_part, global_exercise) = row
            exercises.append({
                "userid": userid,
                "exercise_id": exercise_id,
                "exercise_name": exercise_name,
                "category": category,
                "body_part": body_part,
                "global_exercise": global_exercise,
            })
        return exercises
    except sqlite3.Error as err:
        print("Error: {}".format(err))
    finally:
        cur.close()


def check_if_username_is_taken(conn, username):
    """Returns true if a given username already exists in db / is taken"""
    cur = conn.cursor()
    try:
        sql = """ SELECT COUNT(*) FROM users where username = ? """
        cur.execute(sql, (username,))
        for row in cur:
            # if value is >= 1, there is already a record of the username
            if row[0] >= 1:
                return True

        return False 
    except sqlite3.Error as err:
        print("Error: {}".format(err))
    finally:
        cur.close()

def check_if_email_is_taken(conn, email):
    """Returns true if a given email already exists in db / is taken"""
    cur = conn.cursor()
    try:
        sql = """ SELECT COUNT(*) FROM users where email = ? """
        cur.execute(sql, (email,))
        for row in cur:
            if row[0] >= 1:
                return True

        return False 
    except sqlite3.Error as err:
        print("Error: {}".format(err))
    finally:
        cur.close()


def load_workouts_for_user(conn, userid):
    """Returns a list of all workouts for the user"""
    cur = conn.cursor()
    try:
        # grab every workout_id there is for a user, and add to list (ordered by date, and if 2 equal, then the newest/highest workout_id)
        sql = """SELECT DISTINCT workout_id FROM workouts WHERE userid=? ORDER BY date DESC, workout_id DESC"""
        cur.execute(sql, (userid,))
        workouts = []
        ids = []
        for row in cur:
            ids.append(row[0])
        sql = """SELECT * FROM workouts WHERE userid=? AND workout_id=?"""
        # for each ID, log the workout belonging to that ID
        for id in ids:    
            cur.execute(sql, (userid, id,))
            workouts.append(cur.fetchall())
        return workouts
    except sqlite3.Error as err:
        print("Error: {}".format(err))
    finally:
        cur.close()


def add_exercise_to_workouts(conn, workout_id, userid, title, ex_name, sets, reps, weight, date):
    """Save exercise to workouts"""
    cur = conn.cursor()
    try:
        # insret each exercise into workouts, also need to grab exercise_id for that exercise (and for correct user if two users has same name for an exercise)
        sql = """INSERT INTO workouts (workout_id, userid, title, exercise_id ,exercise, sets, reps, weight, date) VALUES 
        (?,?,?, (SELECT exercise_id FROM exercises WHERE exercise_name = ? AND userid = ? OR exercise_name = ? AND global_exercise=1) ,?,?,?,?,?)"""
        cur.execute(sql, (workout_id, userid, title, ex_name, userid,ex_name, ex_name, sets, reps, weight, date,))
        conn.commit()
        
    except sqlite3.Error as err:
        print("Error: {}".format(err))
    finally:
        cur.close()


def find_next_workout_id(conn):
    """Find the next free workout id"""
    cur = conn.cursor()
    try:
        sql = """SELECT MAX(workout_id) FROM workouts"""
        cur.execute(sql,)
        next_index = cur.fetchone()
        # increase next workout id:
        return next_index[0]+1
    except sqlite3.Error as err:
        print("Error: {}".format(err))
    finally:
        cur.close()


def delete_workout(conn, userid, workout_id ):
    """ Delete a workout from a user's workouts """
    cur = conn.cursor()
    try:
        sql = """ DELETE FROM workouts WHERE userid = ? AND workout_id = ?"""
        cur.execute(sql, (userid, workout_id))
        conn.commit()
    except sqlite3.Error as err:
        print("Error: {}".format(err))
    finally:
        cur.close()


def create_exercise(conn, user, exercise):
    """Create an exercise, returns the new exercise' ID"""
    cur = conn.cursor()
    try:
        sql = """ INSERT INTO exercises(userid, exercise_name, category, body_part, global_exercise) VALUES(?,?,?,?,?) """
        cur.execute(sql, (user["id"], exercise["exercise_name"], exercise["category"], exercise["body_part"], exercise["global"] ))
        conn.commit()
        return cur.lastrowid
    except sqlite3.Error as err:
        print("Error: {}".format(err))
    finally:
        cur.close()


def delete_exercise(conn, exercise):
    """Delete an exercise"""
    cur = conn.cursor()
    try:
        sql = """ DELETE FROM exercises WHERE userid = ? AND exercise_id = ? """
        cur.execute(sql, (exercise["userid"], exercise["exercise_id"] ))
        conn.commit()
    except sqlite3.Error as err:
        print("Error: {}".format(err))
    finally:
        cur.close()


def edit_existing_exercise(conn, exercise, exercise_id):
    """Find an existing exercise for a user, and replace it with the new"""
    cur = conn.cursor()
    try:
        sql = """UPDATE exercises SET exercise_name = ?, category = ?, body_part = ? WHERE exercise_id = ?"""
        cur.execute(sql, (exercise["newName"], exercise["newCategory"], exercise["newBodyPart"], exercise_id,))
        conn.commit()
    except sqlite3.Error as err:
        print("Error: {}".format(err))
    finally:
        cur.close()


def get_all_global_exercises(conn):
    """Only loads global exercises"""
    cur = conn.cursor()
    try:
        sql = (""" SELECT * FROM exercises WHERE  global_exercise = 1 """)
        cur.execute(sql)
        exercises = []
        for row in cur:
            (userid, exercise_id, exercise_name, category, body_part, global_exercise) = row
            exercises.append({
                "userid": userid,
                "exercise_id": exercise_id,
                "exercise_name": exercise_name,
                "category": category,
                "body_part": body_part,
                "global_exercise": global_exercise,
            })
        return exercises
    except sqlite3.Error as err:
        print("Error: {}".format(err))
    finally:
        cur.close()


def get_exercise_history(conn, exercise_id, userid):
    """Returns a list of all the times an exercise has been done"""
    cur = conn.cursor()
    try:
        sql = (""" SELECT title, exercise, sets, reps, weight, date FROM workouts WHERE  userid = ? AND exercise_id = ? ORDER BY date DESC """)
        cur.execute(sql, (userid, exercise_id))
        history = []
        for row in cur:
            (title, exercise, sets, reps, weight, date) = row
            history.append({
                "title": title,
                "exercise": exercise,
                "sets": sets,
                "reps": reps,
                "weight": weight,
                "date": date,
            })
        return history
    except sqlite3.Error as err:
        print("Error: {}".format(err))
    finally:
        cur.close()

def delete_user(conn, id):
    """Fully delete a user along with all records of him/her ever existing"""
    cur = conn.cursor()
    try:
        sql = """ DELETE FROM workouts WHERE userid= ?"""
        cur.execute (sql, (id, ))
        
        sql2 = """ DELETE FROM exercises WHERE userid = ?"""
        cur.execute(sql2, (id, ))

        sql3 = """ DELETE FROM users WHERE id = ?"""
        cur.execute (sql3, (id, ))

        conn.commit()
    except sqlite3.Error as err:
        print("Error: {}".format(err))
    finally:
        cur.close()


