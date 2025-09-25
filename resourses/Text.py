import io
from flask import request, send_file
from flask_jwt_extended import jwt_required
from flask_restx import Namespace, Resource, fields
from models.Post import PostModel
from extensions import db
from models.Sections import SectionModel
from models.Texts import TextModel


ns = Namespace('texts', description='Texts related operations')

upload_parser = ns.parser()
upload_parser.add_argument(
    'file',
    type='file',
    location='files',
    required=True
)

text_model = ns.model('Text', {
    'id': fields.Integer(readonly=True, description='The text unique identifier'),
    'content': fields.String(required=True, description='The text content'),
    'hasFile': fields.Boolean(description='identify if file exists'),
    'sectionId': fields.Integer(required=True, description='The ID of the section this text belongs to'),
    'created_at': fields.DateTime(readonly=True, description='The text creation date')
})

@ns.route('/')
class Texts(Resource):
    def get(self):
        return [
            text.json() for text in TextModel.query.all()
        ]

    @jwt_required()
    @ns.expect(text_model)
    def post(self):
        data = request.get_json()
        new_text = TextModel(content=data['content'], sectionId=data['sectionId'])
        db.session.add(new_text)
        db.session.commit()
        return new_text.json(), 201


@ns.route('/<int:id>')
class Text(Resource):
    def get(self, id):
        section = SectionModel.query.get_or_404(id)
        texts = [ text.json() for text in TextModel.query.filter_by(sectionId=section.id).all() ]
        return texts

    @jwt_required()
    @ns.expect(text_model)
    def put(self, id):
        text = TextModel.query.get_or_404(id)
        data = request.get_json()
        text.content = data['content']
        text.sectionId = data['sectionId']
        db.session.commit()
        return text.json()

    @jwt_required()
    def delete(self, id):
        text = TextModel.query.get_or_404(id)
        db.session.delete(text)
        db.session.commit()
        return '', 200
    
@ns.route('/<int:id>/upload')
class TextUpload(Resource):
    @jwt_required()
    @ns.expect(upload_parser)
    def post(self, id):
        text = TextModel.query.get_or_404(id)

        file = request.files['file']

        file_bytes = file.read()
        text.file = file_bytes

        db.session.commit()

        return '', 200
    
@ns.route('/<int:id>/file')
class TextFile(Resource):
    def get(self, id):
        text = TextModel.query.get_or_404(id)
        
        return send_file(
            io.BytesIO(text.file),
            mimetype="image/png",  # ou image/jpeg dependendo do tipo
            as_attachment=False,
            download_name=f"text_{id}.png"
        )