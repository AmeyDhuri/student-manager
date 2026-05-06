from flask import render_template, request, redirect, session, flash
from sqlalchemy.exc import IntegrityError

from app.decorators import login_required
from app.models import db, User, Student

def init_routes(app):
    @app.route("/register", methods=["GET", "POST"])
    def register():
        if request.method == "POST":
            username = request.form["username"].strip()
            password = request.form["password"]

            existing_user = User.query.filter_by(username=username).first()
            if existing_user:
                flash("Username already exists", "danger")
                return redirect("/register")

            user = User(username=username)
            user.set_password(password)

            db.session.add(user)
            db.session.commit()

            flash("Registration succsessful. Please Login.", "success")
            return redirect("/login")

        return render_template("register.html")

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            username = request.form["username"].strip()
            password = request.form["password"]

            user = User.query.filter_by(username=username).first()

            if user and user.check_password(password):
                session["user_id"] = user.id
                session["username"] = user.username
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
        user = User.query.get_or_404(session["user_id"])
        return render_template("account.html", users=user)

    @app.route("/change_password", methods=["POST"])
    @login_required
    def change_password():
        new_password = request.form["new_password"]
        confirm_password = request.form["confirm_password"]
        
        user = User.query.get_or_404(session["user_id"])

        current_password = user["password"]

        if new_password != confirm_password:
            flash("Passwords do not match", "danger")
            return redirect("/account_details")
        
        if user.check_password(new_password):
            flash("New password cannot be the same as current password", "danger")
            return redirect("/account_details")

        user.set_password(new_password)
        db.session.commit()

        flash("Password updated successfully", "success")
        return redirect("/account_details")


    @app.route("/")
    @login_required
    def index():
        search = request.args.get("search", "").strip()
        division = request.args.get("division", "").strip()
        page = request.args.get("page", 1, type=int)
        per_page = 5
        user_id = session["user_id"]

        query = Student.query.filter_by(user_id=user_id)

        if search:
            query = query.filter(Student.name.ilike(f"%{search}%"))

        if division:
            query = query.filter_by(division=division)

        pagination = query.order_by(Student.division, Student.roll_no).paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )

        students = pagination.items

        division = (
            db.session.query(Student.division)
            .filter_by(user_id=user_id)
            .distinct()
            .order_by(Student.division)
            .all()
        )
        divisions = [d[0] for d in division]

        return render_template(
            "index.html",
            students=students,
            username=session["username"],
            search=search,
            division=division,
            divisions=divisions,
            page=page,
            total_pages=pagination.pages
        )

    @app.route("/add", methods=["POST"])
    @login_required
    def add():
        name = request.form["name"].strip()
        standard = request.form["standard"].strip()
        division = request.form["division"].strip()
        
        try:
            age = int(request.form["age"])
            roll_no = int(request.form["roll_no"])
        except ValueError:
            flash("Age and Roll Number must be valid numbers!", "danger")
            return redirect("/")

        if age <= 0 or roll_no <= 0:
            flash("Age and Roll Number must be positive!", "danger")
            return redirect("/")

        student = Student(
            name=name,
            age=age,
            standard=standard,
            division=division,
            roll_no=roll_no,
            user_id=session["user_id"]
        )

        try:
            db.session.add(student)
            db.session.commit()
            flash("Successfully added a student!", "success")
        except IntegrityError:
            db.session.rollback()
            flash("Roll number already exists in this class/division!", "danger")

        return redirect("/")

    @app.route("/edit/<int:id>", methods=["GET", "POST"])
    @login_required
    def edit(id):
        student = Student.query.filter_by(
            id = id,
            user_id = session["user_id"]
        ).first_or_404()

        if request.method == "POST":
            name = request.form["name"].strip()
            standard = request.form["standard"].strip()
            division = request.form["division"].strip()

            try:
                age = int(request.form["age"])
                roll_no = int(request.form["roll_no"])
            except:
                flash("Age or Roll no must be valid numbers !", "danger")
                return redirect(f"/edit/{id}")
            
            if age <= 0 or roll_no <= 0:
                flash("Age and Roll Number must be positive!", "danger")
                return redirect(f"/edit/{id}")
            
            student.name = name
            student.age = age
            student.standard = standard
            student.division = division
            student.roll_no = roll_no

            try:
                db.session.commit()
                flash("Student updated successfully!", "success")
                return redirect("/")
            except IntegrityError:
                db.session.rollback()
                flash("Roll number already exists in this class/division!", "danger")
                return redirect(f"/edit/{id}")

        return render_template("edit.html", student=student)

    @app.route("/delete/<int:id>", methods=["POST"])
    @login_required
    def delete(id):
        student = Student.query.filter_by(
            id=id,
            user_id=session["user_id"]
        ).first_or_404()

        db.session.delete(student)
        db.session.commit()

        flash("Student deleted successfully!", "danger")
        return redirect("/")