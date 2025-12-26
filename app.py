print("hello, world")

"""
TODO
1. home:           display home page
2. info:           display info page
3. tester:         cycle through 255 grayscale values
4. register:       register for an account
5. login:          Log user in (already made)
6. logout:         log user out (already made)
7. save_preset:    save grayscale value to database for logged-in user
8. saves:          display user saved grayscale values
9. delete_preset:  delete grayscale value from database for logged-in user
"""

"""
Helpful commands:
flask run --port=5001
ctrl c to stop flask
"""

import os # used for python to interact with operating system such as getting file paths and creating folders but is not needed in this program
import sqlite3
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required 

# Configure application
app = Flask(__name__) # create Flask application instance
app.secret_key = "os.urandom(24)" # secret key is so that sessions are secure. Flask uses this to encrypt session data. If someone modifies your cookies, flask will know because the signature won't match and so it will reject the session. os.random(24) is common convention and generates a random 24-byte string each time the app starts. 24 is chosen because it falls halfway within the recommended range of 16-32 bytes for secret keys and is sufficiently secure for most applications.
app.config["DEBUG"] = True # enable debug mode so that we get detailed error messages in the browser and automatic reloading of the server when code changes. This should be disabled in production for security reasons.

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False # session will not be permanent and will expire when the browser is closed
app.config["SESSION_TYPE"] = "filesystem" # store session data on the filesystem instead of in cookies
Session(app) # apply the session configuration to the Flask app

@app.route("/")
def home():
    """1. Display the home page of OLED Vertical Banding Tester"""

    return render_template("home.html")



@app.route("/home", methods=["GET", "POST"])
def home_tab():
    """1. Display the home page of OLED Vertical Banding Tester"""

    if request.method == "POST":

        # you need to redirect user back to homepage or you will get 500 internal server error.
        return redirect("/")

    else:
        return render_template("home.html")



@app.route("/info", methods=["GET", "POST"])
def info():
    """2. Display the info page of OLED Vertical Banding Tester"""

    if request.method == "POST":

        # you need to redirect user back to homepage or you will get 500 internal server error.
        return redirect("/")

    else:
        return render_template("info.html")



@app.route("/tester")
def tester():
    """3. Display the tester page of OLED Vertical Banding Tester"""

    # set brightness level from query parameter (the saved preset that is clicked on in saves.html) or default to 0 if not provided
    level = request.args.get("level", default=0, type=int)

    # render tester.html with fullscreen and start_level variables
    return render_template(
        "tester.html",
        fullscreen=True,
        start_level=level
    )
    


@app.route("/register", methods=["GET", "POST"])
def register():
    """4. Register user"""

    session.clear() # Forget any user_id

    if request.method == "POST":

        # open database
        connection = sqlite3.connect("database.db") # connect to the SQLite database file
        connection.row_factory = sqlite3.Row   # so rows behave like dicts (CS50-style)
        db = connection.cursor() # create a cursor object to interact with the database

        # get form values
        username = request.form.get("username")
        password = request.form.get("password")
        confirm_password = request.form.get("confirmation")

        # validation
        if not username:
            connection.close()
            return apology("Sorry, username field cannot be blank.", 400)
        if not password:
            connection.close()
            return apology("Sorry, password field cannot be blank.", 400)
        if not confirm_password:
            connection.close()
            return apology("Sorry, confirm password field cannot be blank.", 400)
        if confirm_password != password:
            connection.close()
            return apology("Sorry, passwords do not match.", 400)

        # checking if username exists from database
        db.execute("SELECT * FROM users WHERE username = ?", (username,))
        existing = db.fetchone() # fetch one row
        if existing is not None:
            connection.close()
            return apology("Sorry, username already taken.", 400)

        # hash password
        password_hash = generate_password_hash(password)

        # insert user into database
        db.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, password_hash))
        connection.commit()

        # get new user
        db.execute("SELECT * FROM users WHERE username = ?", (username,))
        row = db.fetchone()

        # close the connection before redirecting
        connection.close()

        # log user in
        session["user_id"] = row["id"]

        # redirect to login page
        return redirect("/login")

    else:
        return render_template("register.html")



@app.route("/login", methods=["GET", "POST"])
def login():
    """5. Log user in (already made)"""

    # Forget any user_id
    session.clear()

    if request.method == "POST":

        # open database
        # conn is common convention for connection variable name
        conn = sqlite3.connect("database.db") # connect to the SQLite database file
        conn.row_factory = sqlite3.Row # we need this so rows behave like dicts (CS50-style)
        db = conn.cursor() # create a cursor object to interact with the database

        # validation
        if not request.form.get("username"):
            return apology("must provide username", 403)
        if not request.form.get("password"):
            return apology("must provide password", 403)

        # query database for username
        db.execute("SELECT * FROM users WHERE username = ?", (request.form.get("username"),))
        row = db.fetchone()  # fetch one row

        # close database before returning
        conn.close()

        # ensure username exists and password is correct
        if row is None or not check_password_hash(row["password_hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = row["id"]

        # Redirect user to home page
        return redirect("/")
    
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")



@app.route("/logout")
def logout():
    """6. Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")



@app.route("/save_preset", methods=["POST"])
@login_required # to ensure only logged-in users can save presets since presets are tied to user accounts.
def save_preset():
    """7. Save a grayscale preset to the database for the logged-in user"""

    # Get JSON data from request. We need to use request.get_json() because the data is sent as JSON from the frontend. We need json module to parse the JSON data. 
    data = request.get_json()
    level = data.get("level")

    # Validate level
    if level is None:
        return {"error": "No level provided"}, 400

    # Get user_id from session
    user_id = session["user_id"]

    # open database
    # conn is common convention for connection variable name
    conn = sqlite3.connect("database.db") # connect to the SQLite database file
    conn.row_factory = sqlite3.Row # we need this so rows behave like dicts (CS50-style)
    db = conn.cursor() # create a cursor object to interact with the database

    # Check if there is a duplicate preset
    db.execute(
        "SELECT 1 FROM presets WHERE user_id = ? AND r = ?",
        (user_id, level)
    )
    duplicate = db.fetchone() # fetch one row

    # If duplicate exists, return "Preset already saved." message
    if duplicate:
        conn.close()
        return jsonify({
            "status": "duplicate",
            "message": "Preset already saved."
        })

    # Insert preset into database
    # Use 3 quotation marks if you you want to do a multi-line string
    db.execute("""
        INSERT INTO presets (user_id, r, g, b) 
        VALUES (?, ?, ?, ?)
    """, (user_id, level, level, level)) 

    # Commit changes and close connection
    conn.commit()
    conn.close()

    # Return success response "Preset saved!" message
    return {"status": "success", "message": "Preset saved!", "saved_level": level} 



@app.route("/saves")
@login_required # to ensure only logged-in users can save presets since presets are tied to user accounts.
def saves():
    """8. Display the saves page of OLED Vertical Banding Tester"""

    # get user_id from session
    user_id = session["user_id"]

    # open database
    # conn is common convention for connection variable name
    conn = sqlite3.connect("database.db") # connect to the SQLite database file
    conn.row_factory = sqlite3.Row # we need this so rows behave like dicts (CS50-style)
    db = conn.cursor() # create a cursor object to interact with the database

    # query presets for the user
    db.execute("SELECT * FROM presets WHERE user_id = ?", (user_id,))
    presets = db.fetchall()

    # close connection
    conn.close()

    # render saves.html with presets
    return render_template("saves.html", presets=presets)



@app.route("/delete_preset/<int:preset_id>", methods=["POST"])
@login_required
def delete_preset(preset_id):
    """9. Delete a grayscale preset from the database for the logged-in user"""

    # Get user_id from session
    user_id = session["user_id"]

    # open database
    # conn is common convention for connection variable name
    conn = sqlite3.connect("database.db") # connect to the SQLite database file
    # we don't need conn.row_factory = sqlite3.Row here because we only need it for SELECTing rows and reading columns by name rather than INSERT / UPDATE / DELETE
    db = conn.cursor() # create a cursor object to interact with the database

    # Delete preset from database
    db.execute(
        "DELETE FROM presets WHERE id = ? AND user_id = ?",
        (preset_id, user_id),
    )

    # Commit changes and close connection
    conn.commit()
    conn.close()

    # Flash message and redirect to saves page
    flash("Preset deleted.")
    return redirect("/saves")



# Ensure responses aren't cached so that users always receive the most recent data e.g., after logging in or out.
@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response



# Run the app
if __name__ == "__main__":
    app.run(debug=True) # Start the Flask development server only when running this file directly
