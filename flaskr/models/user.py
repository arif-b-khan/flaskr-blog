from .. import orm as db

class User(db.Model):
        id = db.Column(db.Integer, primary_key=True, autoincrement=True)
        username = db.Column(db.String(80), unique=True, nullable=False)
        password = db.Column(db.String(200), unique=False, nullable=False)

        def __repr__(self):
            return F'<User {self.username!r}>'