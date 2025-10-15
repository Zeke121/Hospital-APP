import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory, jsonify
from werkzeug.utils import secure_filename
from models import (db, Patient, Doctor, Appointment, Prescription, MedicalRecord, 
                   DoctorAvailability, Operation, Income, Message, Medication, Document)
# Imports for authentication
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_bcrypt import Bcrypt

# --- APP and EXTENSION INITIALIZATION ---
app = Flask(__name__)
# Configurations
app.config['SECRET_KEY'] = 'a_very_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hospital.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

# Initialize extensions
db.init_app(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


# --- AUTHENTICATION SETUP ---
@login_manager.user_loader
def load_user(user_id):
    return Doctor.query.get(int(user_id))


# --- HELPER FUNCTION ---
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


# --- DATABASE CREATION AND SEEDING ---
with app.app_context():
    db.create_all()
    if not Doctor.query.first():
        # Create default admin doctor
        hashed_password = bcrypt.generate_password_hash('password').decode('utf-8')
        admin_doctor = Doctor(
            name='Dr. Antonio Murray', 
            email='admin@hospital.com', 
            password=hashed_password, 
            specialization='System Admin',
            hospital='Mbezi Beach Hospital',
            experience_years=10,
            total_patients=1500,
            total_reviews=850,
            phone='+255-123-456-789'
        )
        
        # Create sample doctors
        best_doctor = Doctor(
            name='Dr. Jackline Swai',
            email='jackline@hospital.com',
            password=hashed_password,
            specialization='Endocrinologist',
            hospital='Mbezi Beach Hospital',
            experience_years=8,
            total_patients=2598,
            total_reviews=1537,
            phone='+255-987-654-321'
        )
        
        # Create sample patients
        patients_data = [
            {'name': 'Daniel Smith', 'age': 45, 'gender': 'Male', 'phone': '152-660-5591', 'weight': 75, 'disease': 'Diabetes'},
            {'name': 'Dora Herrera', 'age': 32, 'gender': 'Female', 'phone': '152-660-5592', 'weight': 54, 'disease': 'Flu'},
            {'name': 'Albert Diaz', 'age': 67, 'gender': 'Male', 'phone': '152-660-5593', 'weight': 82, 'disease': 'Cancer'},
            {'name': 'Edith Lyons', 'age': 29, 'gender': 'Female', 'phone': '152-660-5594', 'weight': 49, 'disease': 'Liver Disease'},
            {'name': 'Martha Fletcher', 'age': 55, 'gender': 'Female', 'phone': '152-660-5595', 'weight': 68, 'disease': 'Lung Disease'},
            {'name': 'Glenn Stanley', 'age': 41, 'gender': 'Male', 'phone': '152-660-5596', 'weight': 75, 'disease': 'Cancer'},
            {'name': 'Johanna Blake', 'age': 38, 'gender': 'Female', 'phone': '152-660-5597', 'weight': 54, 'disease': 'Diabetes'},
            {'name': 'Dustin Ramsey', 'age': 26, 'gender': 'Male', 'phone': '152-660-5598', 'weight': 49, 'disease': 'Liver Disease'},
            {'name': 'Evelyn Thomas', 'age': 63, 'gender': 'Female', 'phone': '152-660-5599', 'weight': 71, 'disease': 'Stroke'},
            {'name': 'Mamie Mack', 'age': 52, 'gender': 'Female', 'phone': '152-660-5600', 'weight': 65, 'disease': 'Hypertension'}
        ]
        
        # Add doctors
        db.session.add(admin_doctor)
        db.session.add(best_doctor)
        db.session.commit()
        
        # Add patients
        for patient_data in patients_data:
            patient = Patient(**patient_data)
            db.session.add(patient)
        
        db.session.commit()
        
        # Create some sample appointments with different statuses
        appointments_data = [
            {'patient_id': 1, 'doctor_id': 1, 'date': '2024-01-04', 'time': '10:00', 'diagnosis': 'Routine checkup', 'status': 'Accepted'},
            {'patient_id': 2, 'doctor_id': 2, 'date': '2024-01-05', 'time': '14:30', 'diagnosis': 'Flu symptoms', 'status': 'Pending'},
            {'patient_id': 3, 'doctor_id': 1, 'date': '2024-01-06', 'time': '09:15', 'diagnosis': 'Cancer treatment', 'status': 'Pending'},
            {'patient_id': 4, 'doctor_id': 2, 'date': '2024-01-07', 'time': '11:45', 'diagnosis': 'Liver function test', 'status': 'Pending'},
            {'patient_id': 5, 'doctor_id': 1, 'date': '2024-01-08', 'time': '16:20', 'diagnosis': 'Respiratory issues', 'status': 'Pending'}
        ]
        
        for apt_data in appointments_data:
            appointment = Appointment(**apt_data)
            db.session.add(appointment)
        
        # Create sample income records
        income_data = [
            {'amount': 150.0, 'source': 'Appointment', 'patient_id': 1, 'doctor_id': 1, 'description': 'Consultation fee'},
            {'amount': 200.0, 'source': 'Appointment', 'patient_id': 2, 'doctor_id': 2, 'description': 'Specialist consultation'},
            {'amount': 5000.0, 'source': 'Operation', 'patient_id': 3, 'doctor_id': 1, 'description': 'Surgery procedure'},
            {'amount': 120.0, 'source': 'Appointment', 'patient_id': 4, 'doctor_id': 2, 'description': 'Follow-up visit'},
            {'amount': 150.0, 'source': 'Appointment', 'patient_id': 5, 'doctor_id': 1, 'description': 'Diagnostic consultation'}
        ]
        
        for income_record in income_data:
            income = Income(**income_record)
            db.session.add(income)
        
        # Create some sample medications
        medications_data = [
            {'name': 'Metformin', 'dosage': '500mg', 'description': 'Diabetes medication', 'stock_quantity': 100, 'unit_price': 15.50},
            {'name': 'Amoxicillin', 'dosage': '250mg', 'description': 'Antibiotic', 'stock_quantity': 75, 'unit_price': 8.25},
            {'name': 'Lisinopril', 'dosage': '10mg', 'description': 'Blood pressure medication', 'stock_quantity': 50, 'unit_price': 12.75},
            {'name': 'Paracetamol', 'dosage': '500mg', 'description': 'Pain reliever', 'stock_quantity': 200, 'unit_price': 3.50}
        ]
        
        for med_data in medications_data:
            medication = Medication(**med_data)
            db.session.add(medication)
        
        db.session.commit()
        print("Database seeded with sample data!")
        print("Default admin account created with email 'admin@hospital.com' and password 'password'")


# --- MAIN APPLICATION ROUTES ---

@app.route('/')
def welcome():
    return render_template('welcome.html')

@app.route('/dashboard')
@login_required
def dashboard():
    # Dashboard statistics
    total_patients = Patient.query.count()
    total_doctors = Doctor.query.count()
    total_operations = Operation.query.count()
    total_income = db.session.query(db.func.sum(Income.amount)).scalar() or 0
    
    # Recent data
    recent_patients = Patient.query.order_by(Patient.date_registered.desc()).limit(5).all()
    appointment_requests = Appointment.query.filter_by(status='Pending').order_by(Appointment.created_at.desc()).limit(5).all()
    best_doctor = Doctor.query.order_by(Doctor.total_reviews.desc()).first()
    
    # Patient status data for chart (mock data for now)
    patient_status_data = [
        {'month': 'Jan', 'recovered': 120, 'deaths': 5},
        {'month': 'Feb', 'recovered': 135, 'deaths': 3},
        {'month': 'Mar', 'recovered': 98, 'deaths': 7},
        {'month': 'Apr', 'recovered': 145, 'deaths': 4},
        {'month': 'May', 'recovered': 167, 'deaths': 6},
        {'month': 'Jun', 'recovered': 134, 'deaths': 2},
        {'month': 'Jul', 'recovered': 135, 'deaths': 8},
        {'month': 'Aug', 'recovered': 156, 'deaths': 5},
        {'month': 'Sep', 'recovered': 142, 'deaths': 3},
        {'month': 'Oct', 'recovered': 178, 'deaths': 7},
        {'month': 'Nov', 'recovered': 165, 'deaths': 4},
        {'month': 'Dec', 'recovered': 189, 'deaths': 6}
    ]
    
    return render_template('index.html', 
                         total_patients=total_patients,
                         total_doctors=total_doctors,
                         total_operations=total_operations,
                         total_income=total_income,
                         recent_patients=recent_patients,
                         appointment_requests=appointment_requests,
                         best_doctor=best_doctor,
                         patient_status_data=patient_status_data)

@app.route('/add_patient', methods=['POST'])
@login_required
def add_patient():
    name = request.form['name']
    age = request.form.get('age')
    gender = request.form['gender']
    phone = request.form.get('phone')
    email = request.form.get('email')
    weight = request.form.get('weight')
    disease = request.form.get('disease')
    
    new_patient = Patient(
        name=name, 
        age=int(age) if age else None,
        gender=gender,
        phone=phone,
        email=email,
        weight=float(weight) if weight else None,
        disease=disease
    )
    db.session.add(new_patient)
    db.session.commit()
    flash('Patient successfully registered!', 'success')
    return redirect(url_for('patients'))

@app.route('/delete_patient/<int:patient_id>')
@login_required
def delete_patient(patient_id):
    patient_to_delete = Patient.query.get_or_404(patient_id)
    db.session.delete(patient_to_delete)
    db.session.commit()
    flash('Patient and their appointments/records deleted.', 'danger')
    return redirect(url_for('patients'))

@app.route('/add_appointment', methods=['POST'])
@login_required
def add_appointment():
    patient_id = request.form['patient_id']
    doctor_id = request.form['doctor_id']
    date = request.form['date']
    time = request.form['time']
    diagnosis = request.form['diagnosis']
    new_appointment = Appointment(
        patient_id=patient_id, 
        doctor_id=doctor_id, 
        date=date,
        time=time, 
        diagnosis=diagnosis,
        status='Pending'
    )
    db.session.add(new_appointment)
    db.session.commit()
    flash('Appointment successfully booked!', 'success')
    return redirect(url_for('dashboard'))

@app.route('/update_appointment_status/<int:appointment_id>/<status>')
@login_required
def update_appointment_status(appointment_id, status):
    appointment = Appointment.query.get_or_404(appointment_id)
    appointment.status = status
    db.session.commit()
    flash(f'Appointment {status.lower()}!', 'success')
    return redirect(url_for('dashboard'))

@app.route('/add_prescription', methods=['POST'])
@login_required
def add_prescription():
    appointment_id = request.form['appointment_id']
    medication = request.form['medication']
    dosage = request.form['dosage']
    notes = request.form['notes']
    new_prescription = Prescription(appointment_id=appointment_id, medication=medication, dosage=dosage, notes=notes)
    db.session.add(new_prescription)
    db.session.commit()
    flash('Prescription successfully added!', 'success')
    return redirect(url_for('dashboard'))

@app.route('/upload_record', methods=['POST'])
@login_required
def upload_record():
    if 'file' not in request.files:
        flash('No file part', 'warning')
        return redirect(url_for('dashboard'))
    file = request.files['file']
    patient_id = request.form['patient_id']
    if file.filename == '':
        flash('No selected file', 'warning')
        return redirect(url_for('dashboard'))
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file.path)
        new_record = MedicalRecord(filename=filename, patient_id=patient_id)
        db.session.add(new_record)
        db.session.commit()
        flash('File successfully uploaded!', 'success')
        return redirect(url_for('dashboard'))
    else:
        flash('File type not allowed', 'danger')
        return redirect(url_for('dashboard'))

@app.route('/uploads/<filename>')
def get_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


# --- AUTHENTICATION AND AVAILABILITY ROUTES ---

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        doctor = Doctor.query.filter_by(email=email).first()
        if doctor and bcrypt.check_password_hash(doctor.password, password):
            login_user(doctor)
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Login Unsuccessful. Please check email and password.', 'danger')
    return render_template('login.html')

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('welcome'))

@app.route("/availability", methods=['GET', 'POST'])
@login_required
def manage_availability():
    days_of_week = {0: "Monday", 1: "Tuesday", 2: "Wednesday", 3: "Thursday", 4: "Friday", 5: "Saturday", 6: "Sunday"}
    if request.method == 'POST':
        selected_days = request.form.getlist('days')
        DoctorAvailability.query.filter_by(doctor_id=current_user.id).delete()
        for day in selected_days:
            new_availability = DoctorAvailability(day_of_week=int(day), doctor_id=current_user.id)
            db.session.add(new_availability)
        db.session.commit()
        flash('Your availability has been updated!', 'success')
        return redirect(url_for('manage_availability'))
    availability_records = DoctorAvailability.query.filter_by(doctor_id=current_user.id).all()
    current_availability = [record.day_of_week for record in availability_records]
    return render_template('manage_availability.html', days=days_of_week, current_availability=current_availability)


# --- API ROUTE FOR DYNAMIC DATA ---

@app.route('/doctors')
@login_required
def doctors():
    all_doctors = Doctor.query.all()
    return render_template('doctors.html', doctors=all_doctors)

@app.route('/patients')
@login_required
def patients():
    all_patients = Patient.query.order_by(Patient.date_registered.desc()).all()
    return render_template('patients.html', patients=all_patients)

@app.route('/messages')
@login_required
def messages():
    # Get messages where current user is either sender or receiver
    received_messages = Message.query.filter_by(receiver_id=current_user.id).order_by(Message.created_at.desc()).all()
    sent_messages = Message.query.filter_by(sender_id=current_user.id).order_by(Message.created_at.desc()).all()
    all_doctors = Doctor.query.filter(Doctor.id != current_user.id).all()
    return render_template('messages.html', 
                         received_messages=received_messages, 
                         sent_messages=sent_messages,
                         all_doctors=all_doctors)

@app.route('/send_message', methods=['POST'])
@login_required
def send_message():
    receiver_id = request.form['receiver_id']
    subject = request.form['subject']
    content = request.form['content']
    
    new_message = Message(
        sender_id=current_user.id,
        receiver_id=receiver_id,
        subject=subject,
        content=content
    )
    db.session.add(new_message)
    db.session.commit()
    flash('Message sent successfully!', 'success')
    return redirect(url_for('messages'))

@app.route('/medications')
@login_required
def medications():
    all_medications = Medication.query.order_by(Medication.name).all()
    return render_template('medications.html', medications=all_medications)

@app.route('/add_medication', methods=['POST'])
@login_required
def add_medication():
    name = request.form['name']
    dosage = request.form['dosage']
    description = request.form['description']
    stock_quantity = int(request.form['stock_quantity']) if request.form['stock_quantity'] else 0
    unit_price = float(request.form['unit_price']) if request.form['unit_price'] else 0.0
    
    new_medication = Medication(
        name=name,
        dosage=dosage,
        description=description,
        stock_quantity=stock_quantity,
        unit_price=unit_price
    )
    db.session.add(new_medication)
    db.session.commit()
    flash('Medication added successfully!', 'success')
    return redirect(url_for('medications'))

@app.route('/edit_medication/<int:medication_id>', methods=['POST'])
@login_required
def edit_medication(medication_id):
    medication = Medication.query.get_or_404(medication_id)
    medication.name = request.form['name']
    medication.dosage = request.form['dosage']
    medication.description = request.form['description']
    medication.stock_quantity = int(request.form['stock_quantity']) if request.form['stock_quantity'] else 0
    medication.unit_price = float(request.form['unit_price']) if request.form['unit_price'] else 0.0
    db.session.commit()
    flash('Medication updated successfully!', 'success')
    return redirect(url_for('medications'))

@app.route('/update_medication_stock/<int:medication_id>', methods=['POST'])
@login_required
def update_medication_stock(medication_id):
    medication = Medication.query.get_or_404(medication_id)
    new_stock = int(request.form['stock_quantity'])
    medication.stock_quantity = new_stock
    db.session.commit()
    flash('Stock updated successfully!', 'success')
    return redirect(url_for('medications'))

@app.route('/delete_medication/<int:medication_id>')
@login_required
def delete_medication(medication_id):
    medication = Medication.query.get_or_404(medication_id)
    db.session.delete(medication)
    db.session.commit()
    flash('Medication deleted successfully!', 'success')
    return redirect(url_for('medications'))

@app.route('/doctor_profile/<int:doctor_id>')
@login_required
def doctor_profile(doctor_id):
    doctor = Doctor.query.get_or_404(doctor_id)
    # Get doctor's recent appointments
    recent_appointments = Appointment.query.filter_by(doctor_id=doctor_id).order_by(Appointment.created_at.desc()).limit(5).all()
    # Get doctor's availability
    availability = DoctorAvailability.query.filter_by(doctor_id=doctor_id).all()
    return jsonify({
        'id': doctor.id,
        'name': doctor.name,
        'email': doctor.email,
        'specialization': doctor.specialization,
        'hospital': doctor.hospital,
        'experience_years': doctor.experience_years,
        'total_patients': doctor.total_patients,
        'total_reviews': doctor.total_reviews,
        'phone': doctor.phone,
        'bio': doctor.bio,
        'recent_appointments': [{
            'id': apt.id,
            'patient_name': apt.patient.name,
            'date': apt.date,
            'time': apt.time,
            'status': apt.status
        } for apt in recent_appointments],
        'availability': [record.day_of_week for record in availability]
    })

@app.route('/send_message_to_doctor', methods=['POST'])
@login_required
def send_message_to_doctor():
    receiver_id = request.form['receiver_id']
    subject = request.form['subject']
    content = request.form['content']
    
    new_message = Message(
        sender_id=current_user.id,
        receiver_id=receiver_id,
        subject=subject,
        content=content
    )
    db.session.add(new_message)
    db.session.commit()
    flash('Message sent successfully!', 'success')
    return redirect(url_for('messages'))

@app.route('/patient_profile/<int:patient_id>')
@login_required
def patient_profile(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    # Get patient's appointments
    appointments = Appointment.query.filter_by(patient_id=patient_id).order_by(Appointment.created_at.desc()).all()
    # Get patient's medical records
    records = MedicalRecord.query.filter_by(patient_id=patient_id).order_by(MedicalRecord.id.desc()).all()
    # Get patient's prescriptions
    prescriptions = []
    for apt in appointments:
        for pres in apt.prescriptions:
            prescriptions.append(pres)
    
    return jsonify({
        'id': patient.id,
        'name': patient.name,
        'age': patient.age,
        'gender': patient.gender,
        'phone': patient.phone,
        'email': patient.email,
        'address': patient.address,
        'weight': patient.weight,
        'disease': patient.disease,
        'status': patient.status,
        'date_registered': patient.date_registered.strftime('%d %b %Y') if patient.date_registered else None,
        'appointments': [{
            'id': apt.id,
            'doctor_name': apt.doctor.name,
            'date': apt.date,
            'time': apt.time,
            'diagnosis': apt.diagnosis,
            'status': apt.status,
            'created_at': apt.created_at.strftime('%d %b %Y') if apt.created_at else None
        } for apt in appointments],
        'records': [{
            'id': record.id,
            'filename': record.filename
        } for record in records],
        'prescriptions': [{
            'id': pres.id,
            'medication': pres.medication,
            'dosage': pres.dosage,
            'notes': pres.notes,
            'appointment_date': pres.appointment.date
        } for pres in prescriptions]
    })

@app.route('/edit_patient/<int:patient_id>', methods=['POST'])
@login_required
def edit_patient(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    patient.name = request.form['name']
    patient.age = int(request.form['age']) if request.form['age'] else None
    patient.gender = request.form['gender']
    patient.phone = request.form['phone']
    patient.email = request.form['email']
    patient.address = request.form.get('address')
    patient.weight = float(request.form['weight']) if request.form['weight'] else None
    patient.disease = request.form['disease']
    patient.status = request.form['status']
    db.session.commit()
    flash('Patient updated successfully!', 'success')
    return redirect(url_for('patients'))

@app.route('/documents')
@login_required
def documents():
    all_documents = Document.query.order_by(Document.uploaded_at.desc()).all()
    return render_template('documents.html', documents=all_documents)

@app.route('/upload_document', methods=['POST'])
@login_required
def upload_document():
    if 'file' not in request.files:
        flash('No file selected', 'warning')
        return redirect(url_for('documents'))
    
    file = request.files['file']
    if file.filename == '':
        flash('No file selected', 'warning')
        return redirect(url_for('documents'))
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        new_document = Document(
            filename=filename,
            original_filename=file.filename,
            file_type=file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else 'unknown',
            file_size=os.path.getsize(file_path),
            doctor_id=current_user.id,
            description=request.form.get('description', '')
        )
        db.session.add(new_document)
        db.session.commit()
        flash('Document uploaded successfully!', 'success')
    else:
        flash('File type not allowed', 'danger')
    
    return redirect(url_for('documents'))

@app.route('/settings')
@login_required
def settings():
    return render_template('settings.html')

@app.route('/api/doctors_by_date')
def doctors_by_date():
    date_str = request.args.get('date')
    if not date_str:
        return jsonify([])
    try:
        selected_date = datetime.strptime(date_str, '%Y-%m-%d')
        day_of_week = selected_date.weekday()
        available_doctors = Doctor.query.join(DoctorAvailability).filter(DoctorAvailability.day_of_week == day_of_week).all()
        doctor_list = [{'id': doc.id, 'name': doc.name, 'specialization': doc.specialization} for doc in available_doctors]
        return jsonify(doctor_list)
    except ValueError:
        return jsonify({'error': 'Invalid date format'}), 400


# --- MAIN EXECUTION BLOCK ---
if __name__ == '__main__':
   app.run(debug=True, host='127.0.0.1', port=5000)
 
    
   # --- app.run(host='192.168.113.198', port=5000, debug=True) ---