from flask import Flask
from flask_sqlalchemy import SQLAlchemy

DEBUG = 'True'
SECRET_KEY = 'random'
UPLOAD_FOLDER = "./app/static/uploads"

app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = "r@nd0m"
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://admin:admin@localhost/profiles"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True # added just to suppress a warning

db = SQLAlchemy(app)
from app import views