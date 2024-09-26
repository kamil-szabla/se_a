# ARC DEV Devices - Web Application

## Application Summary and Explanation

### Problem Statement
The **ARC DEV Devices** web application addresses the need for teams to manage and track their hardware devices efficiently. This is particularly relevant for organisations handling large inventories of devices, such as TV equipment or telecom set-top boxes, where keeping track of device assignments, firmware versions, and locations is crucial. The application ensures that devices are properly recorded and assigned to users, and it monitors their status over time.

### Scope of the Application
The web application provides the following core features:
- **CRUD operations** for managing device records (Create, Read, Update, Delete).
- **User roles** for admin and regular users, with role-based access control.
- **Advanced filtering** and searching based on device manufacturer, model, and location.
- **Firmware version tracking** with notifications for updates or issues.
- **Responsive design** for easy navigation on both desktop and mobile devices.

### Technologies and Dependencies
- **Programming Language**: Python 3.8+
- **Framework**: Flask (with Flask-Migrate for database migrations, Flask-Login for authentication)
- **Database Management System**: SQLite (for local development) or PostgreSQL (for cloud deployment)
- **Front-End**: HTML, CSS, JavaScript (with Bootstrap for responsive design)
- **Deployment**: Hosted on Heroku, using Gunicorn as the web server

---

## Entity Relationship Diagram (ERD)

The database consists of two key tables: **Users** and **Devices**. The **ERD** illustrates the relationship between these tables, including:
- **Users**: Stores user information (admin vs. regular users).
- **Devices**: Contains details like manufacturer, model, firmware version, and known issues.

### ERD Structure:
- **Users** → one-to-many → **Devices**
  
![sea_tables](https://github.com/user-attachments/assets/bac47848-3818-4f5b-8717-7263b86193da)

---

## Instructions for Running the Application

### Prerequisites
- Python 3.8 or higher
- Virtual environment set up (optional but recommended)
- Flask and dependencies listed in `requirements.txt`

### Steps to Run Locally
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/kamil-szabla/se_a.git
   cd se_a
   ```
2. Create and Activate Virtual Environment:
  ```bash
  python3 -m venv venv
  source venv/bin/activate  # For Linux/MacOS
  venv\Scripts\activate     # For Windows
  ```
3. Install Dependencies:
  ```bash
  pip install -r requirements.txt
  ```
4. Database Setup:
  ```bash
  flask db upgrade
  ```
This will set up the necessary tables.

5. Run the Application:
  ```bash
  flask run
  ```
The application will run at http://127.0.0.1:5000/.
