from ..utils import db
from datetime import datetime

class Note(db.Model):
    __tablename__ = "notes"
    id=db.Column(db.Integer(), primary_key=True)
    author=db.Column(db.String(), nullable=False)
    note=db.Column(db.String(), nullable=False)
    date_created=db.Column(db.DateTime, default=datetime.utcnow)
    user=db.Column(db.Integer, db.ForeignKey("users.id"))

    def __repr__(self):
        return f"<Author: {self.author}>"
    

    def save(self):
        db.session.add(self)
        db.session.commit()

    
    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)