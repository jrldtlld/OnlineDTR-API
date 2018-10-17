from api import server
from models import *
from flask_login import LoginManager, login_user

login_manager = LoginManager()
login_manager.init_app(server)


@login_manager.user_loader
def load_user(user_id):
  return Admin.query.get(int(user_id))

@server.route('/', methods=['GET'])
def index():
   return 'hello deployed!'
