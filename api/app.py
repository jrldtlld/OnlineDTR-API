from api import server, request, jsonify, check_password_hash
from models import Admin, Employee, dbase
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
   admin = Admin.query.filter_by(username = data['username']).first()
   if not admin:
      return jsonify({'message': 'Invalid username or password'})
   else:
      if check_password_hash(admin.password, data['password']):
         login_user(admin, remember=True)
         return jsonify({'message': 'Login Successfully!'})
      else:
         return jsonify({'message': 'Invalid username or password'})

@server.route('/employee-list', methods=['GET'])
def employee_list():
   employee_from_db = Employee.query.filter_by(employee_status = 1).all()
   data = []
   if employee_from_db:
      for i in employee_from_db:
         employee = {}
         employee['firstname'] = i.firstname
         employee['middlename'] = i.middlename
         employee['lastname'] = i.lastname
         employee['birthday'] = i.birthday
         employee['address'] = i.address
         employee['gender'] = i.gender
         employee['code'] = i.code
         employee['position'] = i.position
         data.append(employee)
         return jsonify({'employee': data})
   else:
      return jsonify({'employee': data})

@server.route('/add-employee', methods=['GET', 'POST'])
def employee_add():
   data = request.get_json()
   try:
      new_employee = Employee(firstname=data['firstname'], middlename=data['middlename'], lastname=data['lastname'],
                              address=data['address'], gender=data['gender'], code=data['code'], birthday = data['birthday'], position=data['[position'], employee_status=1)
   except:
      return jsonify({'message': 'There was an error adding'})
   dbase.session.add(new_employee)
   dbase.session.commit()
   return jsonify({'message': 'Employee was added Successfully!'})
