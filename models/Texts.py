from extensions import db

class TextModel(db.Model):
    __tablename__ = 'texts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    sectionId = db.Column(db.Integer, db.ForeignKey('sections.id', ondelete='CASCADE'), nullable=False)
    file = db.Column(db.LargeBinary, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())

    def json(self):
        return {
            'id': self.id,
            'content': self.content,
            'sectionId': self.sectionId,
            'created_at': self.created_at.isoformat()
        }