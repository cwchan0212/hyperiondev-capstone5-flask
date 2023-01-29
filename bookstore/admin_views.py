# Views for admin function
import jwt
from bookstore import app
from flask import render_template
from flask_bcrypt import Bcrypt
from flask import Flask, render_template, request, redirect, make_response, jsonify, flash, session, url_for
from .models import User, Book, Review
from functools import wraps
from datetime import datetime, timedelta
bcrypt = Bcrypt(app)
# =====================================================================================================================
# User functions
# ---------------------------------------------------------------------------------------------------------------------
# 
# Route to index page
@app.route("/")
def index():
    return render_template("public/book/base.html")
# ---------------------------------------------------------------------------------------------------------------------
# 
# Route to register page
# Depreciated: used for adding user admin and boss
@app.route("/register", methods=["POST"])
def register():
    row_affected = 0
    username = request.form["username"].strip()
    password = request.form["password"]
    if username and password:
        hashed_password = bcrypt.generate_password_hash(password)
        row_affected = User.add_user(username, hashed_password)
        return f"The user {username} is added successfully."
    else:
        return "problems on username/password"
# ---------------------------------------------------------------------------------------------------------------------
# 
# Route to logout page
@app.route("/logout", methods=["GET"])
def logout():
    # If username session exists, delete username session
    if "username" in session:
        del session["username"]
    # If a token session exists, delete the token session
    if "token" in session:
        del session["token"]
    return render_template("public/book/base.html")
# ---------------------------------------------------------------------------------------------------------------------
# Check login status
def is_logged():
    status = False
    if "username" in session and "token" in session:
        status = True
    return status
# ---------------------------------------------------------------------------------------------------------------------
# Route to login page
@app.route("/login", methods=["GET", "POST"])
def login():
    message = None
    # POST method to load the login page
    if request.method == "POST": 
        username = request.form["username"].strip()
        password = request.form["password"]
        # if username and password exist, check the existence of username and correctness of the password
        if username and password:
            user = User.find_user(username)
            token = None
            # If the username is found, check the correctness of the password
            if user:
                hashed_password = user[0].user_password
                # If the passwords are matched, store the username in the session
                if bcrypt.check_password_hash(hashed_password, password):
                    session["username"] = username
                    user = User.login_time(username)
                    # Create a token from JWT                    
                    token = jwt.encode({
                        "user": username,
                        "expiration": str(datetime.utcnow() + timedelta(seconds=300))
                    },
                        app.config["SECRET_KEY"], algorithm="HS256"
                    )
                    # Store token session
                    session["token"] = token
                    return render_template("public/book/base.html")
                # If the username/password is not matched, flash a message to notify the user
                else:
                    message = f"The username/password is not matched."
                    flash(message)
                    return render_template("public/book/login.html")
            # If no username is matched, flash a message to notify the user
            else:                
                message = f"The username/password is not matched."
                flash(message)
                return render_template("public/book/base.html")
        # If the username/password is blank, flash a message to notify the user
        else:
            message = f"The username/password cannot be blank."
            flash(message)
            return render_template("public/book/base.html")
    # GET method to load login page
    else:        
        return render_template("public/book/login.html")
# ---------------------------------------------------------------------------------------------------------------------
# JWT
# Depreciated but keep it for future reference
# token_required decorated
def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        # token = request.args.get("token")
        token = request.headers.get("Authorization")        
        if not token:
            return jsonify({"Alert": "token is missing."}), 403
        try:
            payload = jwt.decode(token, app.config["SECRET_KEY"])
        except:
            return jsonify({"Alert": "Invalid token."}), 403
    return decorated
# ---------------------------------------------------------------------------------------------------------------------
# login_required decorated
def login_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return redirect(url_for("login"))
        try:
            payload = jwt.decode(token, app.config["SECRET_KEY"])
        except:
            return redirect(url_for("login"))
        return func(*args, **kwargs)
    return decorated