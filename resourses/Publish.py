from flask_jwt_extended import jwt_required
from flask_restx import Namespace, Resource
from models.Post import PostModel
from models.Sections import SectionModel
from models.Texts import TextModel
from extensions import db


ns = Namespace('publish', description='Publishing related oprations')

@ns.route('/<int:postId>')
class Publish(Resource):
    @jwt_required()
    def post(self, postId):
        post = PostModel.query.get_or_404(postId)
        post.is_draft = False

        for section in SectionModel.query.filter_by(postId=post.id).all():
            section.is_draft = False
            for text in TextModel.query.filter_by(sectionId=section.id).all():
                text.is_draft = False

        db.session.commit()
        return '', 200