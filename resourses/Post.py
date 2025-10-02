from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restx import Namespace, Resource, fields
from models.Post import PostModel
from extensions import db


ns = Namespace('posts', description='Posts related operations')

post_model = ns.model('Post', {
    'id': fields.Integer(readonly=True, description='The post unique identifier'),
    'title': fields.String(required=True, description='The post title'),
    'created_at': fields.DateTime(readonly=True, description='The post creation date')
})

@ns.route('/')
class Posts(Resource):
    def get(self):
        return [
            post.json() for post in PostModel.query.order_by(PostModel.created_at.desc()).all()
        ]
    
    @jwt_required()
    @ns.expect(post_model)  
    def post(self):
        data = request.get_json()
        user_id = get_jwt_identity()

        new_post = PostModel(
            title=data['title'], 
            creator=user_id
        )

        db.session.add(new_post)
        db.session.commit()
        return new_post.json(), 201
    
@ns.route('/<int:creatorId>')
class PostsByCreator(Resource):
    def get(self, creatorId):
        posts = PostModel.query.filter_by(creator=creatorId).all()
        return [post.json() for post in posts]

@ns.route('/<int:id>')
class Post(Resource):
    @jwt_required()
    @ns.expect(post_model)  
    def put(self, id):
        post = PostModel.query.get_or_404(id)
        data = request.get_json()
        post.title = data['title']
        db.session.commit()
        return post.json()
    
    @jwt_required()
    def delete(self, id):
        post = PostModel.query.get_or_404(id)
        db.session.delete(post)
        db.session.commit()
        return '', 200