# Student Manager

Student Manager is a simple Flask-based web application for managing student records. It allows users to register, log in, and maintain their own student data, including name, age, standard, division, and roll number.

The application uses SQLite for local data storage and keeps each user's student records separate.

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Database](#database)
- [Routes Overview](#routes-overview)
- [Troubleshooting](#troubleshooting)
- [Future Improvements](#future-improvements)
- [Contributors](#contributors)
- [License](#license)

## Features

- User registration and login
- Password hashing using Werkzeug
- Session-based authentication
- Add, edit, and delete student records
- Search students by name
- Filter students by division
- Pagination for student listings
- Per-user student data separation
- Duplicate roll number prevention within the same standard and division
- Account details page
- Password change functionality
- Flash messages for success and error feedback

## Tech Stack

- **Backend:** Flask
- **Database:** SQLite
- **Templating:** Jinja2
- **Authentication:** Flask sessions and Werkzeug password hashing
- **Environment Variables:** python-dotenv
- **Frontend:** HTML and CSS

## Project Structure

```text
student-manager/
├── app/
│   ├── __init__.py
│   ├── db.py
│   ├── decorators.py
│   ├── routes.py
│   ├── static/
│   └── templates/
│       ├── account.html
│       ├── base.html
│       ├── edit.html
│       ├── index.html
│       ├── login.html
│       └── register.html
├── .gitignore
├── README.md
├── requirements.txt
└── run.py
```
##Installation
Prerequisites
Python 3.10 or newer recommended
pip
Git
Steps

Clone the repository:

git clone https://github.com/AmeyDhuri/student-manager.git
cd student-manager

Create and activate a virtual environment:

Windows

python -m venv venv
venv\Scripts\activate

macOS / Linux

python3 -m venv venv
source venv/bin/activate

Install dependencies:

pip install -r requirements.txt

Create a .env file in the project root:

SECRET_KEY=your-secret-key-here

Run the application:

python run.py

The app will start in debug mode and create the SQLite database automatically inside the Flask instance folder.

##Configuration

The app loads environment variables using python-dotenv.

Variable	Description	Default
SECRET_KEY	Secret key used by Flask for sessions	dev-secret-key

Example .env file:

SECRET_KEY=change-this-before-production

The application also sets the following session cookie options:

SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_SAMESITE = "Lax"

Note: SESSION_COOKIE_SECURE = True requires HTTPS. For local development over plain HTTP, login sessions may not work as expected unless this setting is disabled temporarily.

##Usage
Start the Flask application.
Open the app in your browser.
Register a new user account.
Log in with your credentials.
Add student records with:
Name
Age
Standard
Division
Roll number
Use search and division filters to find records.
Edit or delete student records as needed.
Visit the account page to view account details or change your password.
##Database

The app uses SQLite and automatically creates a database named:

instance/students.db

Two tables are created:

users
Column	Type	Description
id	INTEGER	Primary key
username	TEXT	Unique username
password	TEXT	Hashed password
students
Column	Type	Description
id	INTEGER	Primary key
name	TEXT	Student name
age	INTEGER	Student age
standard	TEXT	Student standard/class
division	TEXT	Student division
roll_no	INTEGER	Student roll number
user_id	INTEGER	Linked user ID

A uniqueness constraint prevents duplicate roll numbers for the same user within the same standard and division.

##Routes Overview
Authentication
Route	Method	Description
/register	GET, POST	Register a new user
/login	GET, POST	Log in an existing user
/logout	GET	Log out the current user
Account
Route	Method	Description
/account_details	GET, POST	View account details
/change_password	POST	Change user password
Student Management
Route	Method	Description
/	GET	View student records with search, filter, and pagination
/add	POST	Add a new student
/edit/<int:id>	GET, POST	Edit an existing student
/delete/<int:id>	POST	Delete a student
Troubleshooting
Login session does not persist locally

The app sets:

SESSION_COOKIE_SECURE = True

This means cookies are only sent over HTTPS. If you are testing locally with http://, temporarily set it to:

SESSION_COOKIE_SECURE = False

Do not use this setting in production without understanding the security impact.

Username already exists

Usernames must be unique. Try registering with a different username.

Duplicate roll number error

A student roll number must be unique for the same user, standard, and division.

Dependency installation issue

Make sure you are installing from the correct file:

pip install -r requirements.txt

If installation fails, verify that each dependency in requirements.txt is listed on a separate line.

##Future Improvements
Add stronger form validation
Add CSRF protection to all forms
Add database migrations
Add automated tests
Add Docker support
Improve production deployment configuration
Add admin dashboard support
Add export/import functionality for student records

##Contributors
AmeyDhuri
