# models.py

from sqlalchemy import Boolean, Column, Float, Integer, String, Text, Date, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    UserID = Column(String, primary_key=True)
    Username = Column(String, unique=True, nullable=False)
    Password = Column(String, nullable=False)
    Role = Column(String, nullable=False) 
    IsActive = Column(Boolean, default=False)
    IsAuthenticated = Column(Boolean, default=False)
    IsAnonymous = Column(Boolean, default=False)  
    
    def __init__(self, user_id, username, password, role):
        self.UserID = user_id
        self.Username = username
        self.Password = password
        self.Role = role
    def get_id(self):
        return str(self.UserID)  

    @property
    def is_authenticated(self):
        return self.IsAuthenticated

    @property
    def is_active(self):
        return self.IsActive

    @property
    def is_anonymous(self):
        return self.IsAnonymous

    def __repr__(self):
        return f"<User(Username={self.Username}, Role={self.Role})>"
    def to_dict(self):
        return {
            'UserID': self.UserID,
            'Username': self.Username,
            'Password': self.Password,
            'Role': self.Role
        }

class Patient(Base):
  __tablename__ = 'patients'

  PatientID = Column(String, ForeignKey('users.UserID'), primary_key=True)
  Name = Column(String)
  DateOfBirth = Column(Date)
  Gender = Column(String)
  PhoneNumber = Column(Integer, unique=True)

  appointments = relationship("Appointment", backref='patient')
  prescriptions = relationship("Prescription", backref='patient')
  billings = relationship("Billing", backref='patient')
  def __init__(self, patient_id, name, date_of_birth, gender, phone_number):
    self.PatientID = patient_id  
    self.Name = name
    self.DateOfBirth = date_of_birth
    self.Gender = gender
    self.PhoneNumber = phone_number
  def to_dict(self):
    return {
        'PatientID': self.PatientID,
        'Name': self.Name,
        'DateOfBirth': self.DateOfBirth.strftime('%Y-%m-%d'),
        'Gender': self.Gender,
        'PhoneNumber': self.PhoneNumber
    }
class Doctor(Base):
  __tablename__ = 'doctors'

  DoctorID = Column(String, ForeignKey('users.UserID'), primary_key=True)  
  Name = Column(String)
  Specialization = Column(String)
  PhoneNumber = Column(Integer, unique=True)
  DepartmentID = Column(Integer, ForeignKey('departments.DepartmentID'))

  appointments = relationship("Appointment", backref='doctor')
  prescriptions = relationship("Prescription", backref='doctor')

  def __init__(self, doctor_id, name, specialization, phone_number, department_id):
      self.DoctorID = doctor_id  
      self.Name = name
      self.Specialization = specialization
      self.PhoneNumber = phone_number
      self.DepartmentID = department_id
class Nurse(Base):
    __tablename__ = 'nurses'

    NurseID = Column(String, primary_key=True)
    Name = Column(String)
    PhoneNumber = Column(Integer, unique=True)
    DepartmentID = Column(Integer, ForeignKey('departments.DepartmentID'))
    
class Department(Base):
    __tablename__ = 'departments'

    DepartmentID = Column(Integer, primary_key=True)
    DepartmentName = Column(String)

    doctors = relationship("Doctor", backref='department')
    nurses = relationship("Nurse", backref='department')

class Appointment(Base):
    __tablename__ = 'appointments'

    AppointmentID = Column(Integer, primary_key=True)
    PatientID = Column(String, ForeignKey('patients.PatientID'))
    DoctorID = Column(String, ForeignKey('doctors.DoctorID'))
    AppointmentDateTime = Column(Date)
    Purpose = Column(String)
class Prescription(Base):
    __tablename__ = 'prescriptions'

    PrescriptionID = Column(Integer, primary_key=True)
    PatientID = Column(String, ForeignKey('patients.PatientID'))
    DoctorID = Column(String, ForeignKey('doctors.DoctorID'))
    Medication = Column(String)
    Dosage = Column(String)
    Frequency = Column(String)
    Refills = Column(Integer)
    Instructions = Column(Text)
    
    def __init__(self, patient_id, doctor_id, medication, dosage, frequency, refills, instructions):
        self.PatientID = patient_id  
        self.DoctorID = doctor_id
        self.Medication = medication
        self.Dosage = dosage
        self.Frequency = frequency
        self.Refills = refills
        self.Instructions = instructions
    
class Billing(Base):
    __tablename__ = 'billings'

    BillingID = Column(Integer, primary_key=True)
    PatientID = Column(String, ForeignKey('patients.PatientID'))
    TotalCost = Column(Float)  
    PaymentStatus = Column(String)
    DateOfBilling = Column(Date)