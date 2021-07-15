from .. import orm as db
from datetime import datetime


class Post(db.Model):
        id = db.Column(db.Integer, primary_key=True, autoincrement=True)
        author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
        created = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)
        title = db.Column(db.String(100), nullable=False)
        body = db.Column(db.String(2000), nullable=False)
        
        author = db.relationship('User', backref=db.backref('posts', lazy=True))

        def __repr__(self):
            return F'<Post {self.username!r}>'
