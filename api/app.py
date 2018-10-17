from api import app
from flask_login import LoginManager, login_user

@app.route('/', methods=['GET'])
def index():
   return 'hello deployed!'