# Student Manager

A simple Flask-based student management system for registering users, logging in, and managing student records with search, division-based filtering, and pagination. The app uses SQLite for persistence and organizes data per authenticated user.

## Table of Contents

- Introduction
- Features
- Project Structure
- Tech Stack
- Installation
- Configuration
- Usage
- Database
- Routes Overview
- Troubleshooting
- Future Improvements
- Contributors

## Introduction

Student Manager is a lightweight web application built with Flask that helps users maintain student records in a simple interface. Each user can create an account, sign in, and manage only their own student entries. Student data includes name, age, standard, division, and roll number. The project follows an app-factory structure and stores data in a local SQLite database created inside the Flask instance folder.

## Features

- User registration and login
- Password hashing for stored credentials
- Session-based authentication
- Add, edit, and delete student records
- Search students by name
- Filter students by division
- Pagination on the student listing page
- Per-user separation of student data
- Duplicate roll-number protection within the same class/division for the same user
- Account page with password change support

## Project Structure

```
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
├── run.py
├── requirement.txt
└── .gitignore
```
The repository contains a Flask application package, HTML templates for the UI, a static assets folder, and a run.py entry point that creates and runs the app.

##Tech Stack

Backend: Flask

Database: SQLite

Templating: Jinja2

Authentication: Werkzeug password hashing + Flask sessions

Environment management: python-dotenv

##Installation
Prerequisites

Python 3.10+ recommended

pip

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

pip install -r requirement.txt

Create a .env file in the project root:

SECRET_KEY=your-secret-key-here

Run the application:

python run.py

The app creates its SQLite database automatically on startup through create_tables(app).

##Configuration

The project loads environment variables using python-dotenv and reads SECRET_KEY from the environment. If no SECRET_KEY is provided, it falls back to "dev-secret-key".

Example:

SECRET_KEY=change-this-in-production
Cookie settings

The application sets:

SESSION_COOKIE_HTTPONLY = True

SESSION_COOKIE_SECURE = True

SESSION_COOKIE_SAMESITE = "Lax"

##Usage

After starting the app:

Open the application in your browser.

Register a new user account.

Log in with your credentials.

Add student records with details such as:

Name

Age

Standard

Division

Roll Number

Use search and division filters to find records quickly.

Edit or delete existing students as needed.

Open the account page to review account details and change your password.

##Database

The app uses SQLite and creates two tables automatically:

users

id

username

password

students

id

name

age

standard

division

roll_no

user_id

A uniqueness constraint prevents duplicate roll numbers for the same user within the same standard and division.

##Routes Overview
Authentication

/register — create a new account

/login — log in

/logout — log out

Account

/account_details — view account details

/change_password — update password

Student management

/ — list students with search, division filter, and pagination

/add — add a new student

Edit and delete handlers are also defined in the routes module for updating and removing student records.

##Troubleshooting
Session/login does not persist locally

The app sets SESSION_COOKIE_SECURE = True, which means session cookies are only sent over HTTPS. When running on plain local HTTP, login sessions may not behave as expected. For local development, you may need to disable this setting temporarily.

Username already exists

Registration enforces unique usernames. Choose a different username if registration fails.

Roll number already exists in the same class/division

The database enforces uniqueness for (user_id, standard, division, roll_no). Use a different roll number or update the existing record.

Dependency install issues on non-Windows systems

The dependency list includes pywin32, which is Windows-specific and may fail on Linux or macOS. Remove it locally if your environment does not support it.

##Future Improvements

Add form validation with WTForms or Flask-WTF in the UI layer

Improve route typing and error handling

Add database migrations

Add unit and integration tests

Add Docker support

Add role-based access or admin dashboards

Improve production configuration and deployment docs

##Contributors

AmeyDhuri
