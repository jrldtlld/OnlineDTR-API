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
   address = dbase.Column(dbase.String(100))
   code = dbase.Column(dbase.String(20))
   position = dbase.Column(dbase.String(30))
   employee_status = dbase.Column(dbase.Integer)

   def __init__(self, firstname, middlename, lastname, birthday, gender, address, code, position, employee_status):
      self.firstname = firstname
      self.middlename = middlename
      self.lastname = lastname
      self.birthday = birthday
      self.birthday = birthday
      self.gender = gender
      self.address = address
      self.code = code
      self.position = position
      self.employee_status = employee_status

class Attendance(dbase.Model):
   __tablename__ = 'attendance'
   attendance_id = dbase.Column(dbase.Integer, primary_key = True)
   employee_id = dbase.Column(dbase.Integer, dbase.ForeignKey('employee.employee_id'))
   morning_time_in = dbase.Column(dbase.Time)
   morning_time_out = dbase.Column(dbase.Time)
   morning_attendance_status = dbase.Column(dbase.Integer)
   afternoon_time_in = dbase.Column(dbase.Time)
   afternoon_time_out = dbase.Column(dbase.Time)
   afternoon_attendance_status = dbase.Column(dbase.Integer)
   
   def __init__(self, employee_id, morning_time_in, morning_time_out, morning_attendance_status, afternoon_time_in, afternoon_time_out, afternoon_attendance_status):
      self.employee_id = employee_id
      self.morning_time_in = morning_time_in
      self.morning_time_out = morning_time_out
      self.morning_attendance_status = morning_attendance_status
      self.afternoon_time_in = afternoon_time_in
      self.afternoon_time_out = afternoon_time_out
      self.afternoon_attendance_status = afternoon_attendance_status

class Logs(dbase.Model):
   __tablename__ = 'logs'
   log_id = dbase.Column(dbase.Integer, primary_key = True)
   log_details = dbase.Column(dbase.String(100))
   log_date = dbase.Column(dbase.DateTime)

   def __init__(self, log_details, log_date):
      self.log_details = log_details
      self.log_date = log_date
