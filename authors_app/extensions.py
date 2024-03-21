from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt

# Define Flask extensions at the global level
db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # Initialize extensions within the application context
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)

    # Other initialization code and routes can be defined here
    
    return app
