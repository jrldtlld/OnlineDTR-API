from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash


server = Flask(__name__)
dbase = SQLAlchemy(server)

server.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
server.secret_key = os.urandom(24)
server.debug = True
 
from models import *
from app import *

dbase.create_all()
