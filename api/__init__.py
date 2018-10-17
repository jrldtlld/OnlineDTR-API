from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.debug = True
dbase = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEM_TRACK_MODIFICATIONS'] = False
app.secret_key = os.urandom(24)
 
from models import *
from app import *

dbase.create_all()
