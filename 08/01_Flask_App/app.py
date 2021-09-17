from flask import Flask, g, session, request, flash, abort
from db_queries import *
from setup_db import add_user
import sqlite3
from sqlite3 import Error
from werkzeug.security import generate_password_hash, check_password_hash
import json


app = Flask(__name__)

app.secret_key = 'SECRET_KEY'
app.config.update(SESSION_COOKIE_SAMESITE="Lax")

DATABASE = './database.db'


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# validates login: checks username and password match
def valid_login(username, password):
    conn = get_db()
    # first need to check that username exists:
    if not check_if_username_is_taken(conn, username):
        return False
    hash = get_hash_from_username(conn, username)
    if hash != None:
        # hash returns (hashvalue,) so need to select hash[0] for the value itself
        return check_password_hash(hash[0], password)
    return False

# Checks if logged in user is same as the user session. Can compare ID's and usernames
def check_correct_user(arg):
    return True if session.get("username") == arg or str(session.get("id")) == arg else False

# ROUTES:
@app.route("/resource/session", methods=["GET", "POST", "DELETE"])
def sessionHandler():
    conn = get_db()
    # POST: create session
    if request.method == "POST":
        user = json.loads(request.data)
        if user["username"] == "" or user["password"] == "":
            return json.dumps(False)    
        if valid_login(user["username"], user["password"]):
            # fetch the user from the db, and put in session
            user = get_user_by_name(conn, user["username"])
            session["username"] = user["username"]
            session["role"] = user["role"]
            session["id"] = user["id"]
            return json.dumps(user)

    # GET: get session
    elif request.method == "GET":
        if session.get("username"):
            return json.dumps(get_user_by_name(conn, session["username"]))
        return json.dumps(False)
    
    # DELETE: pop session
    elif request.method == "DELETE":
        if session.get("username"):
            session.pop("username")
            session.pop("role")
            session.pop("id")
            return json.dumps(True)
        return json.dumps(False)
    
    # Return false if something went wrong
    return json.dumps(False)


@app.route("/user", methods=["POST"])
def register():
    user = json.loads(request.data)
    conn = get_db()
    # Checking for empty usernames/pw or too short usernames:
    if user["username"] == "" or user["email"] == "" or user["password"] == "" or len(user["username"])<3:
        return json.dumps(False)

    # if username is taken, return false
    if check_if_username_is_taken(conn, user["username"]):
        return json.dumps("username taken")
    # check if email is taken
    if check_if_email_is_taken(conn, user["email"]):
        return json.dumps("email taken")

    # If username-field is filled out, and the name is not taken:
    # Create hash and add user to db
    hash = generate_password_hash(user["password"])
    id = add_user(conn, user["username"], user["email"], hash)
    if id == -1:
        return json.dumps(False)

    # fetch the registered user and put username, role and id into session
    user = get_user_by_name(conn, user["username"])
    session["username"] = user["username"]
    session["role"] = user["role"]
    session["id"] = user["id"]
    return json.dumps(user)

@app.route("/user/<id>", methods=["DELETE"])
def deleteUser(id):
    if check_correct_user(id):
        delete_user(get_db(), id)
        # Log out after deleting account:
        session.pop("username")
        session.pop("role")
        session.pop("id")
        return json.dumps(True)
    return json.dumps(False)


# load workouts and save workout
@app.route("/resource/<username>/workouts", methods=["GET", "POST"])
def loadWorkouts(username):
    conn = get_db()
    if check_correct_user(username):

        # GET: get all workouts for user
        if request.method == "GET":
            workouts = load_workouts_for_user(conn, session["id"])
            return json.dumps(workouts)

        # POST: Save a workout to workouts:
        if request.method == "POST":
            workout = json.loads(request.data)
            # Find the next free workout ID:
            workout_id = find_next_workout_id(conn)
            for exercise in workout:
                # Adds each exercise in the saved workout to the table workouts. Each exercise has same title, date and workout_id
                add_exercise_to_workouts(conn, workout_id, session["id"], exercise["title"], exercise["exercise_name"], exercise["sets"], exercise["reps"], exercise["weight"], exercise["date"])
            return json.dumps(True)
    return json.dumps(False)


# delete workout from workouts
@app.route("/resource/workouts/<workout_id>", methods=["DELETE"])
def delWorkout(workout_id):
    if session.get("username"):
        # DELETE: Delete a workout:
        if request.method == "DELETE":
            # delete current logged in user's id and workout id
            delete_workout(get_db(), session["id"], workout_id)
            return json.dumps(True)
    return json.dumps(False)



@app.route("/resource/globalexercises", methods=["GET"])
def globalExercises():
    """ Returns list of all global exercises (for an admin user)"""
    if session.get("username"):
        conn = get_db()
        exercises = get_all_global_exercises(conn)
        return json.dumps(exercises)
    return json.dumps(False)


@app.route("/resource/<username>/exercises", methods=["GET", "POST"])
def exercises(username):
    """GET request returns all exercises for a user. POST request adds exercise to user"""
    if check_correct_user(username):
        conn = get_db()

        if request.method == "POST":
            user = get_user_by_name(conn, username)
            exercise = json.loads(request.data)
            last_id = create_exercise(conn, user, exercise)
            # return the ID for the exercise that was created
            return json.dumps(last_id)

        if request.method == "GET":
            user = get_user_by_name(conn, username)
            exercises = load_exercises_for_userid(conn, user["id"])
            return json.dumps(exercises)
    return json.dumps(False)


@app.route("/resource/exercise/<exercise_id>", methods=["DELETE", "PUT"])
def exercise(exercise_id):
    """Returns true if exercise was successfully edited/removed"""
    # Check that a user is logged in
    if session.get("username"):
        conn = get_db()

        # Delete a single exercise:
        if request.method == "DELETE":
            exercise = json.loads(request.data)
            delete_exercise(conn, exercise)
            return json.dumps(True)

        # Edit single exercise:
        if request.method == "PUT":
            exercise = json.loads(request.data)
            edit_existing_exercise(conn, exercise, exercise_id)
            return json.dumps(True)

    return json.dumps(False)


# Accesses the workouts table to find every record of an exercise
@app.route("/resource/<username>/workouts/exercise/<exercise_id>", methods=["GET"])
def exerciseHistory(username, exercise_id):
    """Returns workout history"""
    if check_correct_user(username):
        conn = get_db()
        user = get_user_by_name(conn, username)
        history = get_exercise_history(conn, exercise_id, user["id"])
        return json.dumps(history)
    return json.dumps(False)


@app.route("/")
def index():
    return app.send_static_file("index.html")


if __name__ == "__main__":
    app.run(debug=True)
