from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.debug = True
dbase = SQLAlchemy(app)


from models import *
from app import *
