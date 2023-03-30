from ..utils import db
from datetime import datetime

class User(db.Model):
    __tablename__ = "users"
    id=db.Column(db.Integer(), primary_key=True)
    firstname=db .Column(db.String(), nullable=False)
    lastname=db.Column(db.String(), nullable=False)
    email=db.Column(db.String(), unique=True, nullable=False)
    password_hash=db.Column(db.Text, nullable=False)
    date_created=db.Column(db.DateTime(), default=datetime.utcnow)
    user_notes=db.relationship("Note", backref="user_note", lazy=True)

    def __repr__(self):
        return f"<User: {self.firstname}>"
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)