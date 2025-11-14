MODERN APPLICATION DEVELOPMENT 1 PROJECT -

HOSPITAL MANAGEMENT SYSTEM 

Project Name: HaethFusion_24X7
Course: App Development I
Project Type: Web Application
Frameworks & Tools: Flask (Backend), Jinja2, HTML, CSS, Bootstrap (Frontend), SQLite (Database)

Overview:
HaethFusion_24X7 is a comprehensive Hospital Management System (HMS) designed to streamline the management of hospitals, doctors, patients, and appointments. Hospitals often struggle with fragmented or manual systems, resulting in scheduling conflicts, loss of patient history, and inefficient resource utilization. This web application addresses these challenges by providing a centralized platform that allows Admins, Doctors, and Patients to interact efficiently based on their roles.

The system is built with a Flask backend, SQLite database for persistent storage, and a responsive frontend using HTML, CSS, Bootstrap, and Jinja2 templates. The application is fully functional on a local machine and programmatically generates all database tables during initialization, eliminating the need for manual database creation.

Roles and Functionalities:

Admin (Hospital Staff):

Admin is the superuser pre-created in the system.

Can manage doctor profiles (add, update, delete).

Can view, manage, and search all appointments.

Can search patients or doctors by name, specialization, or contact information.

Can edit patient and doctor information and blacklist users if needed.

Admin dashboard displays overall statistics such as total doctors, patients, and appointments.

Doctor:

Doctors can log in and view their assigned appointments.

Can mark appointments as Completed or Cancelled and update patient treatment history (diagnosis, prescriptions, and notes).

Can provide their availability for the next 7 days.

Can access the complete medical history of their patients for informed consultations.

Patient:

Patients can register, log in, and manage their profiles.

Can search for doctors by specialization and availability.

Can book, reschedule, or cancel appointments while preventing conflicts for the same doctor at the same time.

Can view upcoming appointments and their status.

Can access past appointment history with diagnosis, prescriptions, and doctor notes.

Core Features:

Dynamic appointment management (Booked → Completed → Cancelled).

Prevention of double-booking for doctors.

Treatment history management for patients.

Search functionality for doctors and patients by various attributes.

Programmatically created admin account and database tables.

Responsive design using Bootstrap, with a user-friendly interface.

Optional API endpoints for interacting with appointments, users, or treatments (returning JSON or using Flask-RESTful).

Form validations both on frontend (HTML5/JS) and backend (Flask).

Additional Features:

Doctors can update availability for the week.

Charts or dashboards for statistics (optional, via libraries like Chart.js).

Full history access for both doctors and patients to ensure continuity of care.

Secure login and role-based access control implemented using Flask extensions like flask_login.

Benefits:
HaethFusion_24X7 ensures seamless communication between patients, doctors, and hospital administration. It reduces manual errors, avoids appointment conflicts, provides real-time access to patient histories, and improves overall hospital management efficiency.

Conclusion:
HaethFusion_24X7 is a robust and scalable HMS designed to modernize hospital operations. By integrating user-friendly dashboards, role-specific functionalities, and a secure database, the system provides an end-to-end solution for hospitals aiming to deliver better patient care and efficient administrative workflows.