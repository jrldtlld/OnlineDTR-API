from api import dbase, generate_password_hash
from flask_login import UserMixin

class Admin(dbase, UserMixin):
   __tablename__ = 'admin'
   admin_id = dbase.Column(dbase.Integer, primary_key = True)
   username = dbase.Column(dbase.String(50), nullable = False)
   password = dbase.Column(dbase.String(256), nullable = False)

   def __init__(self, username, password):
      self.username = username
      self.password = generate_password_hash(password, method='sha256')

class CompanyTime(dbase):
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

class Employee(dbase):
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

   def __init__(self, firstname, middlename, lastname, birthday, gender, address, code, position):
      self.firstname = firstname
      self.middlename = middlename
      self.lastname = lastname
      self.birthday = birthday
      self.birthday = birthday
      self.gender = gender
      self.address = address
      self.code = code
      self.position = position

class Attendance(dbase):
   __tablename__ = 'attendance'


