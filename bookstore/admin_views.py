import jwt
from bookstore import app
from flask import render_template
from flask_bcrypt import Bcrypt
from flask import Flask, render_template, request, redirect, make_response, jsonify, flash, session, url_for
from .models import User, Book, Review
from functools import wraps
from datetime import datetime, timedelta

bcrypt = Bcrypt(app)

@app.route("/admin/dashboard")
def admin_dashboard():
    return render_template("admin/dashboard.html")


@app.route("/admin/profile")
def admin_profile():
    return "Admin Profile"

# ---------------------------------------------------------------------------------------------------------------------
# User functions
# Login

# Home

@app.route("/")
def index():
    if not session.get("username"):
        return render_template("public/book/login.html")
    else:
        return render_template("public/book/base.html")


@app.route("/register", methods=["POST"])
def register():
    row_affected = 0
    post = request.form
    username = request.form["username"].strip()
    password = request.form["password"]
    if username and password:

        hashed_password = bcrypt.generate_password_hash(password)
        print(hashed_password)
        row_affected = User.add_user(username, hashed_password)
        print("row_affected", row_affected)
        return f"The user {username} is added successfully."
    else:
        return "problems on username/password"

@app.route("/logout", methods=["GET"])
def logout():
    if "username" in session:
        del session["username"]
    if "token" in session:
        del session["token"]
    return render_template("public/book/base.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    message = None
    if request.method == "POST": 
        username = request.form["username"].strip()
        password = request.form["password"]
        if username and password:
            user = User.find_user(username)
            token = None
            if user:
                # print("user", len(user), user[0])
                hashed_password = user[0].user_password
                print("hashed password", len(user), hashed_password)
                if bcrypt.check_password_hash(hashed_password, password):
                    session["username"] = username                    
                    token = jwt.encode({
                        "user": username,
                        "expiration": str(datetime.utcnow() + timedelta(seconds=300))
                    },
                        app.config["SECRET_KEY"], algorithm="HS256"
                    )
                    print(f"{username} is logged with token {token}")
                    session["token"] = token
                    return render_template("public/book/base.html")
                    # return jsonify({"token": token})
                    # return jsonify({"token": token})
                else:
                    message = f"The useranme/password is not matched."
                    flash(message)
                    return render_template("public/book/login.html")
                    # return make_response("Unable to verify", 403, {"WWW-Authenicate": "Basic realm: Authentication Failed!" })
            else:
                # no such user
                message = f"The useranme/password is not matched."
                flash(message)
                return render_template("public/book/base.html")

        else:
            message = f"The useranme/password cannot be blank."
            flash(message)
            return render_template("public/book/base.html")
    else:
        # GET method to load login page
        return render_template("public/book/login.html")

# Depreciated but keep it for future reference

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
        # return func(*args, **kwargs)

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

# # Public
# @app.route ("/public")
# def public():
#     return "For public"

# # Auth
# @app.route("/auth")
# @token_required
# def auth():
#     return "JWT is verified. Welcome to your dashboard."