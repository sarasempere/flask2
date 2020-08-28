from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    # tell python how to print the class object on the console
    def __repr__(self):
        return '<Person %r>' % self.username

    # tell python how convert the class object into a dictionary ready to jsonify
    def serialize(self):
        return {
            "username": self.username,
            "email": self.email
        }        



class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    employees = db.relationship("Employee", lazy=True)

      # tell python how to print the class object on the console
    def __repr__(self):
        return '<Department %r>' % self.name

    # tell python how convert the class object into a dictionary ready to jsonify
    def serialize(self):
        return {
            "name": self.name,
            #"employees"
        }        

assignments = db.Table("assignments",
    db.Column("employee_id", db.Integer, db.ForeignKey("employee.id"), primary_key=True),
    db.Column("project_id", db.Integer, db.ForeignKey("project.id"), primary_key=True)
)

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey("department.id"), nullable = False)
    department = db.relationship("Department", lazy=True)
    projects = db.relationship("Project", secondary=assignments, back_populates="employees")


      # tell python how to print the class object on the console
    def __repr__(self):
        return '<Employee %r>' % self.email

    # tell python how convert the class object into a dictionary ready to jsonify
    def serialize(self):
        return {
            "name": self.name
            #"employees"
        }        

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)       
    name = db.Column(db.String(80), unique=True, nullable=False)
    employees = db.relationship("Employee", secondary=assignments, back_populates="projects")

    
      # tell python how to print the class object on the console
    def __repr__(self):
        return '<Project %r>' % self.name

    # tell python how convert the class object into a dictionary ready to jsonify
    def serialize(self):
        return {
            "name": self.name
            #"employees"
        }        