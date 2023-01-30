
from flask import Flask

app = Flask(__name__ )
app.config.from_prefixed_env()
from bookstore import views, admin_views, api_views
app.config["PERMANENT_SESSION_LIFETIME"] = app.config["PERMANENT_SESSION_LIFETIME"] * 60
app.config["MAX_CONTENT_LENGTH"] = app.config['MAX_CONTENT_LENGTH'] * 1024 * 1024

print(f"It is a {app.config['ENV']} mode.")

# Generate requirements.txt
# pip freeze > requirements.txt

# Install requirements.txt
# pip install -r requirements.txt --use-pep517


