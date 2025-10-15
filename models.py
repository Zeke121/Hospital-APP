from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

# Initialize the SQLAlchemy object.
db = SQLAlchemy()

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(10))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(120))
    address = db.Column(db.Text)
    weight = db.Column(db.Float)  # Weight in kg
    disease = db.Column(db.String(100))
    status = db.Column(db.String(20), default='Active')  # Active, Recovered, Deceased
    date_registered = db.Column(db.DateTime, default=datetime.utcnow)
    profile_picture = db.Column(db.String(200))
    # Relationships
    appointments = db.relationship('Appointment', backref='patient', lazy=True, cascade="all, delete-orphan")
    records = db.relationship('MedicalRecord', backref='patient', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Patient {self.name}>'

class Doctor(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    # Authentication fields
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    # Profile fields
    name = db.Column(db.String(100), nullable=False)
    specialization = db.Column(db.String(50))
    phone = db.Column(db.String(20))
    hospital = db.Column(db.String(100))
    experience_years = db.Column(db.Integer, default=0)
    total_patients = db.Column(db.Integer, default=0)
    total_reviews = db.Column(db.Integer, default=0)
    profile_picture = db.Column(db.String(200))
    bio = db.Column(db.Text)
    # Relationships
    appointments = db.relationship('Appointment', backref='doctor', lazy=True)
    availability = db.relationship('DoctorAvailability', backref='doctor', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Doctor {self.name}>'

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(20), nullable=False)
    time = db.Column(db.String(20), nullable=False)
    diagnosis = db.Column(db.Text)
    status = db.Column(db.String(20), default='Pending')  # Pending, Accepted, Rejected, Completed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    # Foreign Keys
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    # Relationships
    prescriptions = db.relationship('Prescription', backref='appointment', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Appointment {self.id} on {self.date}>'

class Prescription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    medication = db.Column(db.String(100), nullable=False)
    dosage = db.Column(db.String(100), nullable=False)
    notes = db.Column(db.Text)
    # Foreign Key
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointment.id'), nullable=False)

    def __repr__(self):
        return f'<Prescription {self.medication}>'

class MedicalRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(200), nullable=False)
    # Foreign Key
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)

    def __repr__(self):
        return f'<MedicalRecord {self.filename}>'
    
class DoctorAvailability(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # We will store the day of the week as an integer: Monday=0, Tuesday=1, ..., Sunday=6
    day_of_week = db.Column(db.Integer, nullable=False) 
    # Foreign key to link this availability to a specific doctor
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)

    def __repr__(self):
        # A little helper to make the day human-readable for debugging
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        return f'<Available on {days[self.day_of_week]}>'

# New models for enhanced features
class Operation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='Scheduled')  # Scheduled, In Progress, Completed
    cost = db.Column(db.Float)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Operation {self.name} for {self.patient.name}>'

class Income(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    source = db.Column(db.String(100))  # Appointment, Operation, etc.
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'))
    date = db.Column(db.DateTime, default=datetime.utcnow)
    description = db.Column(db.Text)

    def __repr__(self):
        return f'<Income ${self.amount} from {self.source}>'

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('doctor.id'))
    receiver_id = db.Column(db.Integer, db.ForeignKey('doctor.id'))
    subject = db.Column(db.String(200))
    content = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Message from {self.sender.name if self.sender else "System"}>'

class Medication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    dosage = db.Column(db.String(50))
    description = db.Column(db.Text)
    stock_quantity = db.Column(db.Integer, default=0)
    unit_price = db.Column(db.Float)
    expiry_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Medication {self.name}>'

class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(200), nullable=False)
    original_filename = db.Column(db.String(200), nullable=False)
    file_type = db.Column(db.String(50))
    file_size = db.Column(db.Integer)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'))
    description = db.Column(db.Text)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Document {self.original_filename}>'