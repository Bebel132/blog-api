from flask import request
from flask_jwt_extended import jwt_required
from flask_restx import Namespace, Resource, fields
from models.Post import PostModel
from extensions import db
from models.Sections import SectionModel


ns = Namespace('sections', description='Sections related operations')

section_model = ns.model('Section', {
    'id': fields.Integer(readonly=True, description='The section unique identifier'),
    'title': fields.String(required=True, description='The section title'),
    'postId': fields.Integer(required=True, description='The ID of the post this section belongs to'),
    'created_at': fields.DateTime(readonly=True, description='The section creation date')
})

@ns.route('/')
class Sections(Resource):
    def get(self):
        return [
            section.json() for section in SectionModel.query.all()
        ]
    
    @jwt_required()
    @ns.expect(section_model)  
    def post(self):
        data = request.get_json()
        new_section = SectionModel(title=data['title'], postId=data['postId'])
        db.session.add(new_section)
        db.session.commit()
        return new_section.json(), 201
    
    
@ns.route('/<int:id>')
class Section(Resource):
    def get(self, id):
        post = PostModel.query.get_or_404(id)
        sections = [section.json() for section in SectionModel.query.filter_by(postId=post.id).all()]
        return sections

    @jwt_required()
    @ns.expect(section_model)  
    def put(self, id):
        section = SectionModel.query.get_or_404(id)
        data = request.get_json()
        section.title = data['title']
        section.postId = data['postId']
        db.session.commit()
        return section.json()
    
    @jwt_required()
    def delete(self, id):
        section = SectionModel.query.get_or_404(id)
        db.session.delete(section)
        db.session.commit()
        return '', 200