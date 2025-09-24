from extensions import db

class PostModel(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    creator = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())

    sections = db.relationship('SectionModel', backref='post', cascade='all, delete-orphan', passive_deletes=True)

    def json(self):
        return {
            'id': self.id,
            'title': self.title,
            'creator': self.creator_user.username if self.creator_user else None,
            'created_at': self.created_at.isoformat()
        }