from api import app  
from models import *
from flask_login import LoginManager, login_user

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
  return Admin.query.get(int(user_id))

@app.route('/', methods=['GET'])
def index():
   return 'hello deployed!'
