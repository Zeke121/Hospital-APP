# 🏥 Modern Hospital Management System

A comprehensive hospital management system built with Flask, featuring a modern dashboard interface that matches professional healthcare software standards.

## ✨ Features

### 🎯 Dashboard Overview
- **Real-time Statistics**: Track new patients, doctors, operations, and income
- **Interactive Charts**: Patient status visualization with recovered/death tracking
- **Best Doctor Profile**: Highlight top-performing doctors with statistics
- **Appointment Management**: Accept/reject appointment requests with one-click actions
- **Recent Patients Table**: Quick access to patient information and status

### 👥 User Management
- **Doctor Authentication**: Secure login system with bcrypt password hashing
- **User Profiles**: Complete doctor profiles with experience, patient count, and reviews
- **Role-based Access**: Different access levels for different user types

### 🏥 Patient Management
- **Patient Registration**: Complete patient profiles with demographics and medical history
- **Medical Records**: File upload and management system
- **Appointment Scheduling**: Dynamic doctor availability based on schedules
- **Status Tracking**: Monitor patient status (Active, Recovered, Deceased)

### 📊 Advanced Features
- **Object-Relational Mapping**: Full SQLAlchemy ORM implementation
- **Database Relationships**: Proper foreign key relationships between all entities
- **Income Tracking**: Monitor revenue from appointments and operations
- **Medication Management**: Track medication inventory and prescriptions
- **Document Management**: Secure file upload and retrieval system
- **Message System**: Internal communication between doctors

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- Virtual environment (recommended)

### Installation

1. **Clone or navigate to the project directory**
   ```bash
   cd hospital-system
   ```

2. **Activate the virtual environment**
   ```bash
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies** (if not already installed)
   ```bash
   pip install flask flask-sqlalchemy flask-login flask-bcrypt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Access the application**
   - Open your browser and go to: `http://192.168.113.198:5000`
   - Or access from any device on the same network using this IP
   - Login with default credentials:
     - **Email**: `admin@hospital.com`
     - **Password**: `password`

## 🎨 Modern Interface

The system features a professional, modern interface with:

- **Clean Dashboard Layout**: Intuitive sidebar navigation and organized content areas
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices
- **Professional Color Scheme**: Blue and white theme matching healthcare standards
- **Interactive Elements**: Hover effects, smooth transitions, and modern UI components
- **Data Visualization**: Chart.js integration for patient status tracking
- **Real-time Updates**: Dynamic content loading and status updates

## 🗄️ Database Schema

### Core Models
- **Patient**: Complete patient information with medical history
- **Doctor**: Doctor profiles with authentication and statistics
- **Appointment**: Appointment scheduling with status tracking
- **Prescription**: Medication management and tracking
- **MedicalRecord**: Document and file management
- **Operation**: Surgical procedure tracking
- **Income**: Revenue and financial tracking
- **Message**: Internal communication system
- **Medication**: Inventory management
- **Document**: File storage and management

### Key Features
- **Foreign Key Relationships**: Proper database relationships
- **Data Integrity**: Constraints and validations
- **Scalable Design**: Support for multiple hospitals and departments
- **Audit Trail**: Timestamps and user tracking

## 🔧 Configuration

### Environment Variables
- `SECRET_KEY`: Flask secret key for sessions
- `SQLALCHEMY_DATABASE_URI`: Database connection string
- `UPLOAD_FOLDER`: Directory for file uploads

### Default Configuration
- **Database**: SQLite (development)
- **Upload Folder**: `uploads/`
- **Allowed File Types**: txt, pdf, png, jpg, jpeg, gif

## 📱 Usage Guide

### For Administrators
1. **Login** with admin credentials
2. **View Dashboard** for system overview
3. **Manage Patients** - Add, edit, or remove patient records
4. **Schedule Appointments** - Book appointments with available doctors
5. **Track Operations** - Monitor surgical procedures and outcomes
6. **Review Income** - Analyze revenue and financial metrics

### For Doctors
1. **Login** with doctor credentials
2. **View Appointments** - Check scheduled appointments
3. **Manage Availability** - Set working days and hours
4. **Add Prescriptions** - Prescribe medications to patients
5. **Upload Records** - Add medical documents and reports

## 🛠️ Development

### Project Structure
```
hospital-system/
├── app.py                 # Main Flask application
├── models.py             # Database models and ORM
├── templates/            # HTML templates
│   ├── base.html         # Base template
│   ├── index.html        # Dashboard template
│   └── login.html        # Login template
├── static/               # Static files
│   └── css/
│       └── dashboard.css # Dashboard styling
├── uploads/              # File upload directory
├── instance/             # Database files
└── venv/                 # Virtual environment
```

### Adding New Features
1. **Models**: Add new database models in `models.py`
2. **Routes**: Add new routes in `app.py`
3. **Templates**: Create new HTML templates in `templates/`
4. **Styling**: Add CSS in `static/css/`

### Database Migrations
When modifying models, delete the existing database to recreate with new schema:
```bash
# Windows
Remove-Item instance\hospital.db -Force

# Linux/Mac
rm instance/hospital.db
```

## 🔒 Security Features

- **Password Hashing**: Bcrypt encryption for all passwords
- **Session Management**: Secure Flask-Login implementation
- **File Upload Security**: Restricted file types and secure filenames
- **Input Validation**: Form validation and sanitization
- **SQL Injection Protection**: SQLAlchemy ORM prevents SQL injection

## 📊 Sample Data

The system comes pre-loaded with sample data including:
- **2 Doctors**: Admin and specialist doctors
- **10 Patients**: Diverse patient profiles with various conditions
- **5 Appointments**: Sample appointment requests
- **4 Medications**: Common medications with inventory
- **Income Records**: Sample revenue data

## 🌟 Key Improvements

This enhanced version includes:
- ✅ Modern dashboard matching professional healthcare software
- ✅ Complete object-relational mapping with SQLAlchemy
- ✅ Enhanced patient and doctor models with additional fields
- ✅ Interactive charts and data visualization
- ✅ Appointment request management with accept/reject functionality
- ✅ Professional styling with responsive design
- ✅ Comprehensive database schema with proper relationships
- ✅ Real-time statistics and metrics
- ✅ User profile management with notifications
- ✅ File upload and document management

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🆘 Support

For support or questions:
1. Check the documentation above
2. Review the code comments
3. Test with the provided sample data
4. Ensure all dependencies are installed correctly

---

## 🌐 Network Access

The application is configured to run on IP address `192.168.113.198:5000`, which means:

- **Local Access**: Visit `http://192.168.113.198:5000` on the same computer
- **Network Access**: Any device on the same network can access the application using the same URL
- **Mobile Access**: You can access the dashboard from phones/tablets on the same WiFi network
- **Multi-User**: Multiple users can access the system simultaneously

### Firewall Note
If you can't access from other devices, you may need to:
1. Allow Python through Windows Firewall
2. Ensure port 5000 is not blocked
3. Check that other devices are on the same network

---

**🎉 Enjoy using your modern hospital management system!**
