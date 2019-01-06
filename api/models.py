from api import dbase, generate_password_hash
from flask_login import UserMixin

class Admin(dbase.Model, UserMixin):
   __tablename__ = 'admin'
   id = dbase.Column(dbase.Integer, primary_key = True)
   username = dbase.Column(dbase.String(50), nullable = False)
   password = dbase.Column(dbase.String(256), nullable = False)

   def __init__(self, username, password):
      self.username = username
      self.password = generate_password_hash(password, method='sha256')

class CompanyTime(dbase.Model):
   __tablename__ = 'companytime'
   company_time_id = dbase.Column(dbase.Integer, primary_key = True)
   morning_time_in = dbase.Column(dbase.Time)
   morning_time_out = dbase.Column(dbase.Time)
   afternoon_time_in = dbase.Column(dbase.Time)
   afternoon_time_out = dbase.Column(dbase.Time)

   def __init__(self, morning_time_in, morning_time_out, afternoon_time_in, afternoon_time_out):
      self.morning_time_in = morning_time_in
      self.morning_time_out = morning_time_out
      self.afternoon_time_in = afternoon_time_in
      self.afternoon_time_out = afternoon_time_out

class Employee(dbase.Model):
   __tablename__ = 'employee'
   employee_id = dbase.Column(dbase.Integer, primary_key = True)
   firstname = dbase.Column(dbase.String(50))
   middlename = dbase.Column(dbase.String(50))
   lastname = dbase.Column(dbase.String(50))
   birthday = dbase.Column(dbase.DATE)
   gender = dbase.Column(dbase.String(6))
   status = dbase.Column(dbase.String(20))
   nationality = dbase.Column(dbase.String(30))
   address = dbase.Column(dbase.String(100))
   code = dbase.Column(dbase.String(20), unique = True)
   position = dbase.Column(dbase.String(30))
   email = dbase.Column(dbase.String(50))
   contact_number = dbase.Column(dbase.String(11))
   employee_status = dbase.Column(dbase.Integer)
   department = dbase.Column(dbase.String(50))

   def __init__(self, firstname, middlename, department, contact_number, email, lastname, birthday, gender, address, code, position, employee_status, nationality, status):
      self.firstname = firstname
      self.middlename = middlename
      self.lastname = lastname
      self.birthday = birthday
      self.gender = gender
      self.address = address
      self.code = code
      self.position = position
      self.employee_status = employee_status
      self.nationality = nationality
      self.status = status
      self.email = email
      self.contact_number = contact_number
      self.department = department

class Attendance(dbase.Model):
   __tablename__ = 'attendance'
   attendance_id = dbase.Column(dbase.Integer, primary_key = True)
   employee_id = dbase.Column(dbase.Integer, dbase.ForeignKey('employee.employee_id'))
   attendance_date = dbase.Column(dbase.Date)
   morning_time_in = dbase.Column(dbase.Time)
   morning_time_out = dbase.Column(dbase.Time)
   morning_attendance_status = dbase.Column(dbase.Integer)
   morning_remarks = dbase.Column(dbase.String(50))
   afternoon_time_in = dbase.Column(dbase.Time)
   afternoon_time_out = dbase.Column(dbase.Time)
   afternoon_attendance_status = dbase.Column(dbase.Integer)
   afternoon_remarks = dbase.Column(dbase.String(50))

   def __init__(self, employee_id,  attendance_date,  morning_attendance_status, afternoon_attendance_status, morning_remarks, afternoon_remarks):
      self.employee_id = employee_id
      self.attendance_date = attendance_date
      self.morning_attendance_status = morning_attendance_status
      self.afternoon_attendance_status = afternoon_attendance_status

class Logs(dbase.Model):
   __tablename__ = 'logs'
   log_id = dbase.Column(dbase.Integer, primary_key = True)
   log_details = dbase.Column(dbase.String(100))
   log_date = dbase.Column(dbase.DateTime)

   def __init__(self, log_details, log_date):
      self.log_details = log_details
      self.log_date = log_date

class Overtimelist(dbase.Model):
   __tablename__ = 'overtimelist'
   overtime_id = dbase.Column(dbase.Integer, primary_key = True)
   overtimer_code = dbase.Column(dbase.String(20))
   overtime_status = dbase.Column(dbase.Integer)
   overtime_request_date = dbase.Column(dbase.Date)
   time_in = dbase.Column(dbase.DateTime)
   time_out = dbase.Column(dbase.DateTime)
   time_status = dbase.Column(dbase.Integer)

   def __init__(self, overtimer_code, overtime_status):
      self.overtimer_code = overtimer_code
      self.overtime_status = overtime_status
