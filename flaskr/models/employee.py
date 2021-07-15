from .. import orm as db

class Employee(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        emp_name = db.Column(db.String(80), unique=True, nullable=False)
        email = db.Column(db.String(120), unique=True, nullable=False)

        def __repr__(self):
            return F'<Employee {self.emp_name!r}>'