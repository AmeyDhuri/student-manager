from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    students = db.relationship(
        "Student",
        backref="owner",
        lazy=True,
        cascade="all, delete-orphan"
    )

    def set_password(self, raw_password):
        self.password = generate_password_hash(raw_password)

    def check_password(self, raw_password):
        return check_password_hash(self.password, raw_password)
    
    def __repr__(self):
        return f"<User {self.username}>"

class Student(db.Model):
      __tablename__ = "students"

      id = db.Column(db.Integer, primary_key=True)
      name = db.Column(db.String(100), nullable=False)
      age = db.Column(db.Integer, nullable=False)
      standard = db.Column(db.String(20), nullable=False)
      division = db.Column(db.String(10), nullable=False)
      roll_no = db.Column(db.Integer, nullable=False)

      user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

      __table_args__ = (
          db.UniqueConstraint(
              "user_id",
              "standard",
              "division",
              "roll_no",
              name="uq_student_roll"
          ),
      )

      def __repr__(self):
          return f"<Student {self.name}>"