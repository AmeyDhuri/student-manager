import os
import sqlite3
from flask import render_template, request, redirect, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

from app.db import get_db_connection
from app.decorators import login_required


def init_routes(app):
    def db_conn():
        db_path = os.path.join(app.instance_path, "students.db")
        return get_db_connection(db_path)

    @app.route("/register", methods=["GET", "POST"])
    def register():
        if request.method == "POST":
            username = request.form["username"]
            password = generate_password_hash(request.form["password"])

            conn = db_conn()
            try:
                conn.execute(
                    "INSERT INTO users (username, password) VALUES (?, ?)",
                    (username, password)
                )
                conn.commit()
            except:
                conn.close()
                flash("Username already exists", "danger")
                return redirect("/register")

            conn.close()
            return redirect("/login")

        return render_template("register.html")

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            username = request.form["username"]
            password = request.form["password"]

            conn = db_conn()
            user = conn.execute(
                "SELECT * FROM users WHERE username=?",
                (username,)
            ).fetchone()
            conn.close()

            if user and check_password_hash(user["password"], password):
                session["user_id"] = user["id"]
                session["username"] = user["username"]
                return redirect("/")

            flash("Invalid credentials!", "danger")
            return redirect("/login")

        return render_template("login.html")

    @app.route("/logout")
    def logout():
        session.clear()
        return redirect("/login")


    @app.route("/account_details", methods=["GET", "POST"])
    @login_required
    def account_details():
        conn = db_conn()
        user = conn.execute("SELECT username, password FROM users WHERE id=?",(session["user_id"],)).fetchone()

        conn.close()

        return render_template("account.html", users=user)

    @app.route("/change_password", methods=["POST"])
    @login_required
    def change_password():
        new_password = request.form["new_password"]
        confirm_password = request.form["confirm_password"]
        conn = db_conn()

        user = conn.execute("SELECT password FROM users WHERE id = ?",(session["user_id"],)).fetchone()

        current_password = user["password"]

        if new_password != confirm_password:
            flash("Passwords do not match", "danger")
            conn.close()
            return redirect("/account_details")
        
        if check_password_hash(current_password, new_password):
            flash("New password cannot be the same as current password", "danger")
            conn.close()
            return redirect("/account_details")

        hashed = generate_password_hash(new_password)

        
        conn.execute(
            "UPDATE users SET password = ? WHERE id = ?",
            (hashed, session["user_id"])
        )
        conn.commit()
        conn.close()

        flash("Password updated successfully", "success")
        return redirect("/account_details")


    @app.route("/")
    @login_required
    def index():
        search = request.args.get("search")
        division = request.args.get("division")
        page = request.args.get("page", 1, type=int)

        per_page = 5
        offset = (page - 1) * per_page

        conn = db_conn()

        divisions = conn.execute(
            "SELECT DISTINCT division FROM students WHERE user_id=? ORDER BY division",
            (session["user_id"],)
        ).fetchall()

        query = "SELECT * FROM students WHERE user_id=?"
        params = [session["user_id"]]

        if search:
            query += " AND name LIKE ? COLLATE NOCASE"
            params.append(f"%{search}%")

        if division:
            query += " AND division=?"
            params.append(division)

        query += " ORDER BY division, roll_no LIMIT ? OFFSET ?"
        params.extend([per_page, offset])

        students = conn.execute(query, params).fetchall()

        count_query = "SELECT COUNT(*) FROM students WHERE user_id=?"
        count_params = [session["user_id"]]

        if search:
            count_query += " AND name LIKE ? COLLATE NOCASE"
            count_params.append(f"%{search}%")

        if division:
            count_query += " AND division=?"
            count_params.append(division)

        total = conn.execute(count_query, count_params).fetchone()[0]

        conn.close()

        total_pages = (total + per_page - 1) // per_page

        return render_template(
            "index.html",
            students=students,
            username=session["username"],
            search=search,
            division=division,
            divisions=divisions,
            page=page,
            total_pages=total_pages
        )

    @app.route("/add", methods=["POST"])
    @login_required
    def add():
        name = request.form["name"]
        age = int(request.form["age"])
        standard = request.form["standard"]
        division = request.form["division"]
        roll_no = int(request.form["roll_no"])

        if age <= 0 or roll_no <= 0:
            flash("Age and Roll Number must be positive!", "danger")
            return redirect("/")

        conn = db_conn()
        try:
            conn.execute(
                "INSERT INTO students (name, age, standard, division, roll_no, user_id) VALUES (?, ?, ?, ?, ?, ?)",
                (name, age, standard, division, roll_no, session["user_id"])
            )
            conn.commit()
            flash("Successfully added a student!", "success")
        except sqlite3.IntegrityError:
            flash("Roll number already exists in this class/division!", "danger")

        conn.close()
        return redirect("/")

    @app.route("/edit/<int:id>", methods=["GET", "POST"])
    @login_required
    def edit(id):
        conn = db_conn()

        if request.method == "POST":
            name = request.form["name"]
            age = request.form["age"]
            standard = request.form["standard"]
            division = request.form["division"]
            roll_no = request.form["roll_no"]

            conn.execute(
                "UPDATE students SET name=?, age=?, standard=?, division=?, roll_no=? WHERE id=? AND user_id=?",
                (name, age, standard, division, roll_no, id, session["user_id"])
            )
            conn.commit()
            conn.close()
            return redirect("/")

        student = conn.execute(
            "SELECT * FROM students WHERE id=? AND user_id=?",
            (id, session["user_id"])
        ).fetchone()
        conn.close()

        return render_template("edit.html", student=student)

    @app.route("/delete/<int:id>", methods=["POST"])
    @login_required
    def delete(id):
        conn = db_conn()
        conn.execute(
            "DELETE FROM students WHERE id=? AND user_id=?",
            (id, session["user_id"])
        )
        conn.commit()
        conn.close()

        flash("Student deleted successfully!", "danger")
        return redirect("/")