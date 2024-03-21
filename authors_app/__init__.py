from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

# Initialize Flask app
app = Flask(__name__)

# Configure SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/authors_api'
db = SQLAlchemy(app)

# Initialize Flask-Bcrypt
bcrypt = Bcrypt(app)

def create_app():
    app.config.from_object('config.Config')
    
    # Import blueprints
    from authors_app.controllers.auth.auth_controller import auth
    from authors_app.controllers.auth.book_controllers import book
    from authors_app.controllers.auth.company_controllers import company

    # Register blueprints
    app.register_blueprint(auth, url_prefix='/api/v1/auth')
    app.register_blueprint(book, url_prefix='/api/v1/book')
    app.register_blueprint(company, url_prefix='/api/v1/company')

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
