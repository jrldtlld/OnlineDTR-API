from api import server, request, jsonify, check_password_hash
from models import *
from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url
from sqlalchemy import and_, desc, extract
from flask_login import LoginManager, login_user
import datetime as dt
import pyqrcode
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

@server.route('/create-time', methods=['GET'])
def create_time():
   new_time = CompanyTime('09:00','12:00', '13:00', '17:00')
   dbase.session.add(new_time)
   dbase.session.commit()
   return jsonify({'message':'Time created successfully'})

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
      #logs here
         details = "Logged in"
         new_log = Logs(log_date=dt.datetime.now(), log_details=details)
         dbase.session.add(new_log)
         dbase.session.commit()
      #End log
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
         employee['department'] = i.department
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
       email=data['email'], contact_number=data['contact_number'], department=data['department'])
      dbase.session.add(new_employee)
      dbase.session.commit()
      #logs here
      details = "Added employee " + data['firstname'] + " " + data['lastname']
      new_log = Logs(log_date=dt.datetime.now(), log_details=details)
      dbase.session.add(new_log)
      dbase.session.commit()
      #End log
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
      employee_to_edit.department = data['department']
      #logs here
      details = "Edited information of " + employee_to_edit.firstname + " " + employee_to_edit.lastname
      new_log = Logs(log_date=dt.datetime.now(), log_details=details)
      dbase.session.add(new_log)
      dbase.session.commit()
      #End log
      return jsonify({'message': 'Information was edited Successfully!'})
   except:
      return jsonify({'message': 'The code is not available!'})
   


@server.route('/remove/employee/<string:emp_code>', methods=['GET', 'POST'])
def remove_employee(emp_code):
   employee_remove = Employee.query.filter_by(code = emp_code).first()
   try:
      #logs here
      details = "Deactivated/Removed " + employee_remove.firstname + " " + employee_remove.lastname
      new_log = Logs(log_date=dt.datetime.now(), log_details=details)
      dbase.session.add(new_log)
      dbase.session.commit()
      #End log
      employee_remove.employee_status = 0
      dbase.session.commit()
   except:
      return jsonify({'message': 'There was an error request failed!'})
   return jsonify({'message': 'Employee was deactivated!'})


@server.route('/activate/employee/<string:emp_code>', methods=['GET', 'POST'])
def activate_employee(emp_code):
   employee_remove = Employee.query.filter_by(code = emp_code).first()
   try:
      #logs here
      details = "Activated " + employee_remove.firstname + " " + employee_remove.lastname
      new_log = Logs(log_date=dt.datetime.now(), log_details=details)
      dbase.session.add(new_log)
      dbase.session.commit()
      #End log
      employee_remove.employee_status = 1
      dbase.session.commit()
   except:
      return jsonify({'message': 'There was an error request failed!'})
   return jsonify({'message': 'Employee was activated!'})

@server.route('/delete/employee/<string:emp_code>', methods=['GET', 'POST'])
def delete_employee(emp_code):
   employee_delete = Employee.query.filter_by(code = emp_code).first()
   try:
      #logs here
      details = "Permanently removed " + employee_delete.firstname + " " + employee_delete.lastname
      new_log = Logs(log_date=dt.datetime.now(), log_details=details)
      dbase.session.add(new_log)
      dbase.session.commit()
      #End log
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
         employee['department'] = i.department
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
   employee_from_db = Employee.query.filter((Employee.employee_status == 1) & (Employee.code == emp_code)).first()
   data = []
   if employee_from_db:
      employee = {}
      employee['firstname'] = employee_from_db.firstname
      employee['middlename'] = employee_from_db.middlename
      employee['lastname'] = employee_from_db.lastname
      employee['birthday'] = str(employee_from_db.birthday)
      employee['address'] = employee_from_db.address
      employee['status'] = employee_from_db.status
      employee['nationality'] = employee_from_db.nationality
      employee['gender'] = employee_from_db.gender
      employee['code'] = employee_from_db.code
      employee['position'] = employee_from_db.position
      employee['contact_number'] = employee_from_db.contact_number
      employee['email'] = employee_from_db.email
      employee['department'] = employee_from_db.department
      data.append(employee)
      return jsonify({'employee': data})
   else:
      return jsonify({'employee': data})

@server.route('/edit/time', methods=['POST'])
def edit_time():
   data = request.get_json()
   to_edit = CompanyTime.query.filter_by(company_time_id = 1).first()
   if to_edit:
      to_edit.morning_time_in = dt.datetime.strptime(data['morning_time_in'], "%H:%M:%S")
      to_edit.morning_time_out = dt.datetime.strptime(data['morning_time_out'], "%H:%M:%S")
      to_edit.afternoon_time_in = dt.datetime.strptime(data['afternoon_time_in'], "%H:%M:%S")
      to_edit.afternoon_time_out = dt.datetime.strptime(data['afternoon_time_out'], "%H:%M:%S")
      dbase.session.commit()
      #logs here
      details = "Edited time In/Out."
      new_log = Logs(log_date = dt.datetime.now(), log_details = details )
      dbase.session.add(new_log)
      dbase.session.commit()
      #End log
      return jsonify({'message':'Time changed successfully!'})
   return jsonify({'message': 'Operation failed!'})

@server.route('/permanent/remove/<string:emp_code>', methods=['GET'])
def permanent_remove(emp_code):
   to_del = Employee.query.filter_by(code = emp_code).first()
   if to_del:
      #logs here
      details = "Permanently removed " + to_del.firstname + " " + to_del.lastname
      new_log = Logs(log_date=dt.datetime.now(), log_details=details)
      dbase.session.add(new_log)
      dbase.session.commit()
      #End log
      dbase.session.delete(to_del)
      dbase.session.commit()
      return jsonify({'message': 'Employee removed permanently!'})
   return jsonify({'message': 'Operation failed!'})


def to_min(str_time):
   y, m, d = str_time.split(":")
   total = (int(y) * 60) + int(m) + int(d)/60
   return total

@server.route('/logging/<string:emp_code>', methods=['GET', 'POST'])
def logging(emp_code):
   #query time for logging in
   time_set = CompanyTime.query.filter_by(company_time_id = 1).first()
   morning_in = time_set.morning_time_in.strftime("%H:%M:%S")
   get_morning_in = to_min(morning_in)
   morning_out = time_set.morning_time_out.strftime("%H:%M:%S")
   get_morning_out = to_min(morning_out)
   afternoon_in = time_set.afternoon_time_in.strftime("%H:%M:%S")
   get_afternoon_in = to_min(afternoon_in)
   afternoon_out = time_set.afternoon_time_out.strftime("%H:%M:%S")
   get_afternoon_out = to_min(afternoon_out)
   print get_afternoon_out
   print "\n"
   print get_afternoon_in
   print "\n"
   print get_morning_in
   print "\n"
   print get_morning_out
   print "\n"
   current_time = dt.datetime.now().strftime("%H:%M:%S")
   get_time = to_min(current_time)
   print get_time
   print "\n"
   emp_to_log = Employee.query.filter(and_(Employee.code == emp_code, Employee.employee_status == 1)).first()
   current_date = dt.datetime.now().strftime("%m-%d-%Y")
   print current_date
   print "\n"
   #check if employee is active
   if not emp_to_log:
      return jsonify({'message': 'user not found'})
   #check if employee is got logged for current date
   logging_check = Attendance.query.filter(and_(Attendance.employee_code == emp_code, Attendance.attendance_date == current_date)).first()
   #if not logged yet for this day
   if not logging_check:
      new_logging = Attendance(employee_code=emp_code, attendance_date=current_date, morning_attendance_status=0, afternoon_attendance_status=0,
      morning_remarks = 'Absent', afternoon_remarks = 'Absent')
      dbase.session.add(new_logging)
      dbase.session.commit()
      to_log = Attendance.query.filter(and_(Attendance.employee_code == emp_code, Attendance.attendance_date == current_date)).first()
      if get_time <= get_morning_in:
         if to_log.morning_attendance_status == 0:
            to_log.morning_time_in = dt.datetime.now().strftime("%H:%M:%")
            to_log.morning_attendance_status = 1
            to_log.morning_remarks = 'On Time'
            dbase.session.commit()
            return jsonify({'message': 'Morning time-in Success!'})
      elif get_time > get_morning_in and get_time <= get_morning_out:
         if to_log.morning_attendance_status == 0:
            to_log.morning_time_in = dt.datetime.now().strftime("%H:%M:%S")
            to_log.morning_attendance_status = 1
            to_log.morning_remarks = 'Late'
            dbase.session.commit()
            return jsonify({'message': 'Morning time-in Success!'})
         else:
            return jsonify({'message': 'Please time-out later!'})
      elif get_time > get_morning_out and get_time <= get_afternoon_in:
         if to_log.morning_attendance_status == 0:
            if to_log.afternoon_attendance_status == 0:
               to_log.afternoon_time_in = dt.datetime.now().strftime("%H:%M:%S")
               to_log.afternoon_attendance_status = 1
               to_log.afternoon_remarks = 'On Time'
               dbase.session.commit()
               return jsonify({'message': 'Afternoon time-in Success'})
            elif to_log.afternoon_attendance_status == 1:
               return jsonify({'message': 'Please time-out later!'})
         elif to_log.morning_attendance_status == 2:
            to_log.afternoon_time_in = dt.datetime.now().strftime("%H:%M:%S")
            to_log.afternoon_attendance_status = 1
            to_log.afternoon_remarks = 'On Time'
            dbase.session.commit()
            return jsonify({'message': 'Time-in Success!'})
         else:
            to_log.morning_time_out = dt.datetime.now().strftime("%H:%M:%S")
            to_log.morning_attendance_status = 2
            dbase.session.commit()
            return jsonify({'message': 'Time-out Success!'})
      elif get_time > get_afternoon_in and get_time <= get_afternoon_out:
            if to_log.afternoon_attendance_status == 0:
               to_log.afternoon_time_in = dt.datetime.now().strftime("%H:%M:%S")
               to_log.afternoon_attendance_status = 1
               to_log.afternoon_remarks = 'Late'
               dbase.session.commit()
               return jsonify({'message': 'Afternoon Time-in Success!'})
            else:
               to_log.afternoon_out = dt.datetime.now().strftime("%H:%M:%S")
               to_log.afternoon_attendance_status = 2
               dbase.session.commit()
               return jsonify({'message': 'Afternoon Time-out Success!'})
   else:
      if get_time <= get_morning_in:
         if logging_check.morning_attendance_status == 0:
            logging_check.morning_time_in = dt.datetime.now().strftime("%H:%M:%S")
            logging_check.morning_attendance_status = 1
            logging_check.morning_remarks = 'On Time'
            dbase.session.commit()
            return jsonify({'message': 'Time-in Success!'})
      elif get_time > get_morning_in and get_time < get_morning_out:
         if logging_check.morning_attendance_status == 0:
            logging_check.morning_time_in = dt.datetime.now().strftime("%H:%M:%S")
            logging_check.morning_attendance_status = 1
            logging_check.morning_remarks = 'Late'
            dbase.session.commit()
            return jsonify({'message': 'Time-in Success!'})
         else:
            return jsonify({'message': 'Please time-out later!'})
      elif get_time >= get_morning_out and get_time <= get_afternoon_in:
         if logging_check.morning_attendance_status == 0 and logging_check.afternoon_attendance_status == 0:
            logging_check.afternoon_time_in = dt.datetime.now().strftime("%H:%M:%S")
            logging_check.afternoon_attendance_status = 1
            logging_check.afternoon_remarks = 'On Time'
            dbase.session.commit()
            return jsonify({'message': 'Afternoon time-in Success'})
         elif logging_check.morning_attendance_status == 2:
            logging_check.afternoon_time_in = dt.datetime.now().strftime("%H:%M:%S")
            logging_check.afternoon_attendance_status = 1
            logging_check.afternoon_remarks = 'On Time'
            dbase.session.commit()
            return jsonify({'message': 'Afternoon Time-in Success!'})
         if  logging_check.afternoon_attendance_status == 0:
            logging_check.morning_time_out = dt.datetime.now().strftime("%H:%M:%S")
            logging_check.morning_attendance_status = 2
            logging_check.afternoon_time_in = dt.datetime.now().strftime("%H:%M:%S")
            logging_check.afternoon_attendance_status = 1
            logging_check.afternoon_remarks = 'On Time'
            dbase.session.commit()
            return jsonify({'message': 'Afternoon Time-in Success!'})
         else:
            return jsonify({'message': 'Cannot time-out yet!'})
      elif get_time > get_afternoon_in and get_time <= get_afternoon_out:
         if logging_check.morning_attendance_status == 1:
            logging_check.morning_time_out = dt.datetime.now().strftime("%H:%M:%S")
            logging_check.morning_attendance_status = 2
         if logging_check.afternoon_attendance_status == 0:
            logging_check.afternoon_time_in = dt.datetime.now().strftime("%H:%M:%S")
            logging_check.afternoon_attendance_status = 1
            logging_check.afternoon_remarks = 'Late'
            dbase.session.commit()
            return jsonify({'message': 'Time-in Success!'})
         else:
            logging_check.afternoon_time_out = dt.datetime.now().strftime("%H:%M:%S")
            logging_check.afternoon_attendance_status = 2
            dbase.session.commit()
            return jsonify({'message': 'Time-out Success!'})
      else:
         return jsonify({'message': 'Failed!'})

@server.route('/get_logs', methods=['GET'])
def get_logs():
   log = Logs.query.all()
   logs = []
   if log:
      for i in log:
         log_data = {}
         log_data['logdetails'] = i.log_details
         log_data['logdate'] = str(i.log_date)
         logs.append(log_data)
      return jsonify({'adminlogs': logs})
   else:
      return jsonify({'adminlogs': logs})

@server.route('/summary/<string:dates>', methods=['GET','POST'])
def summary(dates):
   data = request.get_json()
   dates = dt.datetime.strptime(dates, "%Y-%m-%d")
   if data['emp_id'] == "":
      summary = Attendance.query.filter(and_((extract('year', Attendance.attendance_date) == (dates.strftime("%Y"))),\
         (extract('month', Attendance.attendance_date) == (dates.strftime("%m"))))).order_by(Attendance.attendance_date.desc()).all()
      employees = []
      if not summary:
         return jsonify({'Employee': employees})
      for employee in summary:
         employee_data = {}
         name = Employee.query.filter_by(code=employee.employee_code).first()
         employee_data['name'] = name.firstname + " " + name.middlename + " " + name.lastname
         employee_data['date'] = employee.attendance_date
         employee_data['morning_remarks'] = employee.morning_remarks
         employee_data['afternoon_remarks'] = employee.afternoon_remarks
         if employee.morning_time_in is None:
            employee_data['morning_time_in'] = "None"
         else:
            employee_data['morning_time_in'] = str(employee.morning_time_in.strftime("%H:%M:%S"))
         if employee.morning_time_out is None:
            employee_data['morning_time_out'] = "None"
         else:
            employee_data['morning_time_out'] = str(employee.morning_time_out.strftime("%H:%M:%S"))
         if employee.afternoon_time_in is None:
            employee_data['afternoon_time_in'] = "None"
         else:
            employee_data['afternoon_time_in'] = str(employee.afternoon_time_in.strftime("%H:%M:%S"))
         if employee.afternoon_time_out is None:
            employee_data['afternoon_time_out'] = "None"
         else:
            employee_data['afternoon_time_out'] = str(employee.afternoon_time_out.strftime("%H:%M:%S"))
         employees.append(employee_data)
      return jsonify({'Employee': employees})
   else:
      summary = Attendance.query.filter(and_(Attendance.employee_code == data['emp_id'],\
       (extract('year', Attendance.attendance_date) == (dates.strftime("%Y"))),\
         (extract('month', Attendance.attendance_date) == (dates.strftime("%m"))))).order_by(Attendance.attendance_date.desc()).all()
      employees = []
      if not summary:
         return jsonify({'Employee': employees})
      for employee in summary:
         employee_data = {}
         name = Employee.query.filter_by(code=employee.employee_code).first()
         employee_data['name'] = name.firstname + " " + name.middlename + " " + name.lastname
         employee_data['date'] = employee.attendance_date
         employee_data['morning_remarks'] = employee.morning_remarks
         employee_data['afternoon_remarks'] = employee.afternoon_remarks
         if employee.morning_time_in is None:
            employee_data['morning_time_in'] = "None"
         else:
            employee_data['morning_time_in'] = str(employee.morning_time_in.strftime("%H:%M:%S")) 
         if employee.morning_time_out is None:
            employee_data['morning_time_out'] = "None"
         else:
            employee_data['morning_time_out'] = str(employee.morning_time_out.strftime("%H:%M:%S"))
         if employee.afternoon_time_in is None:
            employee_data['afternoon_time_in'] = "None"
         else:
            employee_data['afternoon_time_in'] = str(employee.afternoon_time_in.strftime("%H:%M:%S"))
         if employee.afternoon_time_out is None:
            employee_data['afternoon_time_out'] = "None"
         else:
            employee_data['afternoon_time_out'] = str(employee.afternoon_time_out.strftime("%H:%M:%S"))
         employees.append(employee_data)
      return jsonify({'Employee': employees})

@server.route('/generate/qr/<string:emp_code>', methods=['GET'])
def gen_qr(emp_code):
   qr = pyqrcode.create(emp_code)
   qr.png(emp_code+'.png', scale=6)
   with open(code+'.png', "rb") as f:
      image = f.read()
      print image
      pass
