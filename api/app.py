from api import server, request, jsonify, check_password_hash
from models import Admin, Employee, dbase, Overtimelist
from flask_login import LoginManager, login_user

login_manager = LoginManager()
login_manager.init_app(server)


@login_manager.user_loader
def load_user(user_id):
  return Admin.query.get(int(user_id))

@server.route('/', methods=['GET'])
def index():
   return 'hello deployed!'

server.route('/check/code/<string:emp_code>', methods=['GET'])
def check_code(emp_code):
   employee = Employee.query.filter_by(code = emp_code).first()
   if employee:
      return jsonify({'data':'True'})
   else:
      return jsonify({'data': 'False'})



@server.route('/create-admin', methods=['GET'])
def create_admin():
   admin = Admin('admin', 'admin')
   dbase.session.add(admin)
   dbase.session.commit()
   return jsonify({'message':'Admin created successfully'})

@server.route('/login', methods=['GET', 'POST'])
def login():
   data = request.get_json()
   print data
   admin = Admin.query.filter_by(username = data['username']).first()
   if not admin:
      return jsonify({'message': 'Invalid username or password'})
   else:
      if check_password_hash(admin.password, data['password']):
         login_user(admin, remember=True)
         return jsonify({'message': 'Login Successfully!'})
      else:
         return jsonify({'message': 'Invalid username or password'})

@server.route('/employee/all', methods=['GET'])
def employee_all():
   employee_from_db = Employee.query.filter_by(employee_status=1).all()
   data = []
   if employee_from_db:
      for i in employee_from_db:
         employee = {}
         employee['firstname'] = i.firstname
         employee['middlename'] = i.middlename
         employee['lastname'] = i.lastname
         employee['birthday'] = str(i.birthday)
         employee['address'] = i.address
         employee['status'] = i.status
         employee['nationality'] = i.nationality
         employee['gender'] = i.gender
         employee['code'] = i.code
         employee['position'] = i.position
         employee['contact_number'] = i.contact_number
         employee['email'] = i.email
         data.append(employee)
      return jsonify({'employee': data})
   else:
      return jsonify({'employee': data})

@server.route('/add/employee', methods=['GET', 'POST'])
def employee_add():
   data = request.get_json()
   check_avail = Employee.query.filter_by(code = data['code']).first()
   if not check_avail:
      new_employee = Employee(firstname=data['firstname'], middlename=data['middlename'],
       lastname=data['lastname'], address=data['address'], gender=data['gender'], code=data['code'],
       birthday = data['birthday'], position=data['position'], employee_status=1, nationality=data['nationality'], status=data['status'],
       email=data['email'], contact_number=data['contact_number'])
      dbase.session.add(new_employee)
      dbase.session.commit()
      return jsonify({'message': 'Employee was added Successfully!'})
   else:
      return jsonify({'message': 'The code is not available employee already exist.'})

@server.route('/edit/employee/<string:emp_code>', methods=['GET', 'POST'])
def employee_edit(emp_code):
   data = request.get_json()
   employee_to_edit = Employee.query.filter_by(code = emp_code).first()
   try:
      employee_to_edit.firstname = data['firstname']
      employee_to_edit.middlename = data['middlename']
      employee_to_edit.lastname = data['lastname']
      employee_to_edit.address = data['address']
      employee_to_edit.gender = data['gender']
      employee_to_edit.code = data['code']
      employee_to_edit.birthday = data['birthday']
      employee_to_edit.position = data['position']
      employee_to_edit.nationality = data['nationality']
      employee_to_edit.status = data['status']
      employee_to_edit.email = data['email']
      employee_to_edit.contact_number = data['contact_number']
      dbase.session.commit()
      return jsonify({'message': 'Information was edited Successfully!'})
   except:
      return jsonify({'message': 'The code is not available!'})
   


@server.route('/remove/employee/<string:emp_code>', methods=['GET', 'POST'])
def remove_employee(emp_code):
   employee_remove = Employee.query.filter_by(code = emp_code).first()
   try:
      employee_remove.employee_status = 0
      dbase.session.commit()
   except:
      return jsonify({'message': 'There was an error request failed!'})
   return jsonify({'message': 'Employee was deactivated!'})


@server.route('/activate/employee/<string:emp_code>', methods=['GET', 'POST'])
def activate_employee(emp_code):
   employee_remove = Employee.query.filter_by(code = emp_code).first()
   try:
      employee_remove.employee_status = 1
      dbase.session.commit()
   except:
      return jsonify({'message': 'There was an error request failed!'})
   return jsonify({'message': 'Employee was activated!'})

@server.route('/delete/employee/<string:emp_code>', methods=['GET', 'POST'])
def delete_employee(emp_code):
   employee_delete = Employee.query.filter_by(code = emp_code).first()
   try:
      dbase.session.delete(employee_delete)
      dbase.session.commit()
   except:
      return jsonify({'message': 'There was an error request failed!'})
   return jsonify({'message': 'Employee was Deleted!'})

@server.route('/employee/deactivated', methods=['GET', 'POST'])
def view_deactivated():
   deactivated_list = Employee.query.filter_by(employee_status = 0).all()
   data = []
   if deactivated_list:
      for i in deactivated_list:
         employee = {}
         employee['firstname'] = i.firstname
         employee['middlename'] = i.middlename
         employee['lastname'] = i.lastname
         employee['birthday'] = str(i.birthday)
         employee['address'] = i.address
         employee['status'] = i.status
         employee['nationality'] = i.nationality
         employee['gender'] = i.gender
         employee['code'] = i.code
         employee['position'] = i.position
         employee['contact_number'] = i.contact_number
         employee['email'] = i.email
         data.append(employee)
         return jsonify({'employee': data})
   else:
      return jsonify({'employee': data})
   
@server.route('/request/overtime/<string:emp_code>', methods=['POST'])
def request_overtime(emp_code):
   try:
      overtime_obj = Overtimelist(overtimer_code = emp_code, overtime_status = 0)
   except:
      return jsonify({'message': 'There was an error request failed!'})
   dbase.session.add(overtime_obj)
   dbase.session.commit()

@server.route('/view/employee/<string:emp_code>', methods=['GET'])
def view_one(emp_code):
   employee_from_db = Employee.query.filter(Employee.employee_status == 1 & Employee.code == emp_code).first()
   data = []
   if employee_from_db:
      for i in employee_from_db:
         employee = {}
         employee['firstname'] = i.firstname
         employee['middlename'] = i.middlename
         employee['lastname'] = i.lastname
         employee['birthday'] = str(i.birthday)
         employee['address'] = i.address
         employee['status'] = i.status
         employee['nationality'] = i.nationality
         employee['gender'] = i.gender
         employee['code'] = i.code
         employee['position'] = i.position
         employee['contact_number'] = i.contact_number
         employee['email'] = i.email
         data.append(employee)
      return jsonify({'employee': data})
   else:
      return jsonify({'employee': data})
