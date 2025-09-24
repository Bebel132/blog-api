from datetime import timedelta
import os
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_restx import Api
from extensions import db
from flask import Flask
from flask_cors import CORS
from resourses.Post import ns as ns_post
from resourses.Section import ns as ns_section
from resourses.Text import ns as ns_text
from resourses.Auth import ns as ns_auth

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=15)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)

db.init_app(app)
migrate = Migrate(app, db)

CORS(app)

authorizations = {
    "Bearer Auth": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization",
    }
}

api = Api(
    app, 
    doc='/docs', 
    authorizations=authorizations, 
    security="Bearer Auth"
)

api.title = "Blog API"
jwt = JWTManager(app)

api.add_namespace(ns_post)
api.add_namespace(ns_section)
api.add_namespace(ns_text)
api.add_namespace(ns_auth)

with app.app_context():
    db.create_all()
    
if __name__ == '__main__':
    app.run(debug=True)