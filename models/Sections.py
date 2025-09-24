from extensions import db

class SectionModel(db.Model):
    __tablename__ = 'sections'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    postId = db.Column(db.Integer, db.ForeignKey('posts.id', ondelete='CASCADE'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())

    texts = db.relationship('TextModel', backref='section', cascade='all, delete-orphan', passive_deletes=True)

    def json(self):
        return {
            'id': self.id,
            'title': self.title,
            'postId': self.postId,
            'created_at': self.created_at.isoformat()
        }