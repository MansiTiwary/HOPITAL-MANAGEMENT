# from flask import Flask, render_template
# from flask_sqlalchemy import SQLAlchemy
# from datetime import datetime

# app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///healthfusion.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db = SQLAlchemy(app)


# # ---------------- MODELS ------------------

# class Department(db.Model):
#     __tablename__ = 'departments'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), unique=True, nullable=False)
#     description = db.Column(db.Text, nullable=True)

#     # Relationship to User (doctors)
#     doctors = db.relationship(
#         "User",
#         back_populates="department",
#         foreign_keys="User.department_id"
#     )


# class User(db.Model):
#     __tablename__ = 'users'
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(150), unique=True, nullable=False)
#     email = db.Column(db.String(150), unique=True, nullable=False)
#     password = db.Column(db.String(200), nullable=False)
#     role = db.Column(db.String(50), nullable=False)
#     contact = db.Column(db.String(30))
#     is_active = db.Column(db.Boolean, default=True, nullable=False)
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)

#     department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=True)

#     # Explicitly specify which foreign key this relationship uses
#     department = db.relationship(
#         "Department",
#         back_populates="doctors",
#         foreign_keys=[department_id]
#     )

#     # Relationship to appointments
#     appointments = db.relationship(
#         "Appointment",
#         back_populates="user",
#         cascade="all, delete-orphan"
#     )


# class Treatment(db.Model):
#     __tablename__ = "treatments"

#     id = db.Column(db.Integer, primary_key=True)
#     treat_name = db.Column(db.String(100), nullable=False)
#     description = db.Column(db.Text)

#     # Relationship to appointment
#     appointment = db.relationship(
#         "Appointment",
#         back_populates="treatment"
#     )


# class Appointment(db.Model):
#     __tablename__ = 'appointments'
#     id = db.Column(db.Integer, primary_key=True)
#     date = db.Column(db.String(20))
#     time = db.Column(db.String(20))
#     status = db.Column(db.String(50), default='Booked', nullable=False)

#     user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
#     treatment_id = db.Column(db.Integer, db.ForeignKey("treatments.id"), unique=True)

#     user = db.relationship("User", back_populates="appointments")
#     treatment = db.relationship("Treatment", back_populates="appointment")

# @app.route('/login')
# def login():
#     return render_template('login.html')

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/patient_dashboard')
# def registration():
#     return render_template('registration.html')

# @app.route('/registration')
# def registration():
#     return render_template('patient_dashboard.html')




# # ---------------- RUN APP ------------------
# if __name__ == '__main__':
#     with app.app_context():
#         db.create_all()
#         existing_admin = User.query.filter_by(username='admin').first()
#         if not existing_admin:
#             admin_user = User(
#                 username='admin',
#                 password='adminpass',
#                 email='abc@gmail.com',
#                 role='admin'
#             )
#             db.session.add(admin_user)
#             db.session.commit()
#     app.run(debug=True)
import os
from datetime import datetime
from functools import wraps

from flask import (
    Flask, render_template, request, redirect, url_for, flash, jsonify, abort
)
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin

# --- App setup ---
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///healthfusion.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


# ---------------- MODELS ------------------
class Department(db.Model):
    __tablename__ = 'departments'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    description = db.Column(db.Text)

    doctors = db.relationship('User', back_populates='department')


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # admin, doctor, patient
    contact = db.Column(db.String(30))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    department = db.relationship('Department', back_populates='doctors')

    appointments = db.relationship('Appointment', back_populates='user', foreign_keys='Appointment.user_id', cascade='all, delete-orphan')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # flask-login required
    def get_id(self):
        return str(self.id)


class Treatment(db.Model):
    __tablename__ = 'treatments'
    id = db.Column(db.Integer, primary_key=True)
    treat_name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)

    appointments = db.relationship('Appointment', back_populates='treatment')


class Appointment(db.Model):
    __tablename__ = 'appointments'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(20))   # YYYY-MM-DD
    time = db.Column(db.String(10))   # HH:MM
    status = db.Column(db.String(20), default='Booked')  # Booked/Completed/Cancelled
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))  # patient
    doctor_id = db.Column(db.Integer, db.ForeignKey('users.id'))  # doctor
    treatment_id = db.Column(db.Integer, db.ForeignKey('treatments.id'), nullable=True)

    user = db.relationship('User', foreign_keys=[user_id], back_populates='appointments')
    doctor = db.relationship('User', foreign_keys=[doctor_id])
    treatment = db.relationship('Treatment', back_populates='appointments')


# ---------------- LOGIN ------------------
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Role required decorator
def roles_required(*roles):
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if not current_user.is_authenticated:
                return login_manager.unauthorized()
            if current_user.role not in roles:
                flash("Access denied: insufficient permissions.", "warning")
                return redirect(url_for('index'))
            return f(*args, **kwargs)
        return wrapped
    return decorator


# ---------------- ROUTES ------------------
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        role = request.form.get('role')

        user = User.query.filter_by(username=username, role=role).first()
        if user and user.check_password(password):
            login_user(user)
            flash('Login successful', 'success')
            # redirect by role
            if user.role == 'admin':
                return redirect(url_for('admin_dashboard'))
            if user.role == 'doctor':
                return redirect(url_for('doctor_dashboard'))
            return redirect(url_for('patient_dashboard'))
        flash('Invalid credentials', 'danger')
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out', 'info')
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    # patient registration
    if request.method == 'POST':
        username = request.form.get('full_name')
        email = request.form.get('email')
        password = request.form.get('password')

        if User.query.filter((User.username == username) | (User.email == email)).first():
            flash('User with that username or email already exists', 'warning')
            return redirect(url_for('register'))

        patient = User(username=username, email=email, role='patient')
        patient.set_password(password)
        db.session.add(patient)
        db.session.commit()
        flash('Registration successful. Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('registration.html')


# ---- Dashboards ----
@app.route('/patient_dashboard')
@login_required
@roles_required('patient')
def patient_dashboard():
    # patient sees their upcoming and past appointments
    upcoming = Appointment.query.filter_by(user_id=current_user.id).order_by(Appointment.date, Appointment.time).all()
    doctors = User.query.filter_by(role='doctor').all()
    return render_template('patient_dashboard.html', appointments=upcoming, doctors=doctors)


@app.route('/doctor_dashboard')
@login_required
@roles_required('doctor')
def doctor_dashboard():
    # show appointments assigned to this doctor
    appts = Appointment.query.filter_by(doctor_id=current_user.id).order_by(Appointment.date, Appointment.time).all()
    return render_template('doctor_dashboard.html', appointments=appts)


@app.route('/admin_dashboard')
@login_required
@roles_required('admin')
def admin_dashboard():
    total_doctors = User.query.filter_by(role='doctor').count()
    total_patients = User.query.filter_by(role='patient').count()
    total_appointments = Appointment.query.count()
    doctors = User.query.filter_by(role='doctor').all()
    patients = User.query.filter_by(role='patient').all()
    return render_template(
        'admin_dashboard.html',
        total_doctors=total_doctors,
        total_patients=total_patients,
        total_appointments=total_appointments,
        doctors=doctors,
        patients=patients
    )


# ---- Admin: add doctor (admin only) ----
@app.route('/admin/add_doctor', methods=['GET', 'POST'])
@login_required
@roles_required('admin')
def admin_add_doctor():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        specialization = request.form.get('specialization')

        if User.query.filter((User.username == name) | (User.email == email)).first():
            flash('Doctor with that username or email already exists', 'warning')
            return redirect(url_for('admin_add_doctor'))

        # create or get department
        dept = Department.query.filter_by(name=specialization).first()
        if not dept:
            dept = Department(name=specialization)
            db.session.add(dept)
            db.session.commit()

        doctor = User(username=name, email=email, role='doctor', department=dept)
        doctor.set_password(password)
        db.session.add(doctor)
        db.session.commit()
        flash('Doctor added', 'success')
        return redirect(url_for('admin_dashboard'))

    departments = Department.query.all()
    return render_template('admin_add_doctor.html', departments=departments)


# ---- Patient: book appointment ----
@app.route('/book_appointment', methods=['POST'])
@login_required
@roles_required('patient')
def book_appointment():
    doctor_id = int(request.form.get('doctor_id'))
    date = request.form.get('date')  # expect YYYY-MM-DD
    time = request.form.get('time')  # HH:MM
    treatment_name = request.form.get('treatment_name')

    # check doctor exists
    doctor = User.query.filter_by(id=doctor_id, role='doctor').first()
    if not doctor:
        flash('Doctor not found', 'danger')
        return redirect(url_for('patient_dashboard'))

    # Prevent double-booking: same doctor, same date & time
    conflict = Appointment.query.filter_by(doctor_id=doctor_id, date=date, time=time, status='Booked').first()
    if conflict:
        flash('Selected slot is already booked. Choose a different time.', 'warning')
        return redirect(url_for('patient_dashboard'))

    treatment = None
    if treatment_name:
        treatment = Treatment(treat_name=treatment_name)
        db.session.add(treatment)
        db.session.flush()  # get id

    appt = Appointment(date=date, time=time, user_id=current_user.id, doctor_id=doctor_id)
    if treatment:
        appt.treatment = treatment

    db.session.add(appt)
    db.session.commit()
    flash('Appointment booked', 'success')
    return redirect(url_for('patient_dashboard'))


# ---- Appointment status update (doctor/admin) ----
@app.route('/appointment/<int:appt_id>/update', methods=['POST'])
@login_required
def update_appointment(appt_id):
    appt = Appointment.query.get_or_404(appt_id)
    # only doctor assigned or admin can update
    if current_user.role not in ('admin', 'doctor') or (current_user.role == 'doctor' and appt.doctor_id != current_user.id):
        flash('Not authorized to update this appointment', 'danger')
        return redirect(url_for('index'))

    status = request.form.get('status')
    diagnosis = request.form.get('diagnosis')
    treat_name = request.form.get('treatment_name')

    if status:
        appt.status = status
    if treat_name:
        t = Treatment(treat_name=treat_name, description=diagnosis)
        db.session.add(t)
        appt.treatment = t
    db.session.commit()
    flash('Appointment updated', 'success')
    if current_user.role == 'doctor':
        return redirect(url_for('doctor_dashboard'))
    return redirect(url_for('admin_dashboard'))


# ---------------- JSON API (recommended) ------------------
@app.route('/api/v1/doctors', methods=['GET'])
def api_get_doctors():
    doctors = User.query.filter_by(role='doctor').all()
    data = []
    for d in doctors:
        data.append({
            'id': d.id,
            'username': d.username,
            'email': d.email,
            'department': d.department.name if d.department else None,
            'contact': d.contact
        })
    return jsonify(data)


@app.route('/api/v1/patients', methods=['GET'])
def api_get_patients():
    patients = User.query.filter_by(role='patient').all()
    return jsonify([{'id': p.id, 'username': p.username, 'email': p.email} for p in patients])


@app.route('/api/v1/appointments', methods=['GET', 'POST'])
def api_appointments():
    if request.method == 'GET':
        appts = Appointment.query.all()
        out = []
        for a in appts:
            out.append({
                'id': a.id,
                'date': a.date,
                'time': a.time,
                'status': a.status,
                'patient': {'id': a.user.id, 'username': a.user.username} if a.user else None,
                'doctor': {'id': a.doctor.id, 'username': a.doctor.username} if a.doctor else None,
                'treatment': {'id': a.treatment.id, 'name': a.treatment.treat_name} if a.treatment else None
            })
        return jsonify(out)

    # POST create appointment via API
    payload = request.get_json(force=True)
    # expect: date, time, patient_id, doctor_id, treatment_name (optional)
    doctor_id = payload.get('doctor_id')
    patient_id = payload.get('patient_id')
    date = payload.get('date')
    time = payload.get('time')
    treatment_name = payload.get('treatment_name')

    # basic validation
    if not all([doctor_id, patient_id, date, time]):
        return jsonify({'error': 'missing required fields'}), 400

    conflict = Appointment.query.filter_by(doctor_id=doctor_id, date=date, time=time, status='Booked').first()
    if conflict:
        return jsonify({'error': 'slot already booked'}), 409

    appt = Appointment(date=date, time=time, user_id=patient_id, doctor_id=doctor_id)
    if treatment_name:
        t = Treatment(treat_name=treatment_name)
        db.session.add(t)
        db.session.flush()
        appt.treatment_id = t.id

    db.session.add(appt)
    db.session.commit()
    return jsonify({'message': 'appointment created', 'id': appt.id}), 201


# ---------------- STARTUP ------------------
def create_default_admin():
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(username='admin', email='admin@example.com', role='admin')
        admin.set_password('adminpass')
        db.session.add(admin)
        db.session.commit()
        print("Created default admin (username=admin, password=adminpass)")


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        create_default_admin()
    app.run(debug=True)
