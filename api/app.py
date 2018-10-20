from api import server, request, jsonify, check_password_hash
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


@server.route('/create-admin', methods=['GET'])
def create_admin():
   admin = Admin('admin', 'admin')
   dbase.session.add(admin)
   dbase.session.commit()
   return jsonify({'message':'Admin created successfully'})

@server.route('/login', methods=['GET', 'POST'])
def login():
   data = request.get_json()
   admin = Admin.query.filter_by(usernname = data['username']).first()
   if not admin:
      return jsonify({'message': 'Invalid username or password'})
   else:
      if check_password_hash(admin.password, data['password']):
         login_user(admin, remember=True)
         return jsonify({'message', 'Log-in Successful!'})
      else:
         return jsonify({'message', 'Invalid username or password'})
