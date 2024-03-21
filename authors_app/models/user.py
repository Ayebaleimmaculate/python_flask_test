from flask import Flask, Blueprint, request, jsonify
from flask_bcrypt import bcrypt
from datetime import datetime
from authors_app.extensions import db

auth = Blueprint('auth', __name__)
app = Flask(__name__)

# Register the blueprint
app.register_blueprint(auth)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    contact = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)
    biography = db.Column(db.String(), nullable=True)
    user_type = db.Column(db.String(20), default='author')
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())

    def __init__(self, first_name, last_name, email, contact, password, biography=None, user_type='author'):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.contact = contact
        self.password = password
        self.biography = biography
        self.user_type = user_type

    def get_full_name(self):
        return f'{self.last_name} {self.first_name}'

@auth.route('/api/v1/auth/register', methods=['POST'])
def register():
    try:
        # Retrieving data from the request
        data = request.json
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        contact = data.get('contact')
        email = data.get('email')
        password = data.get('password')
        biography = data.get('biography')

        # Validate input data
        if not all([first_name, last_name, contact, email, password]):
            return jsonify({'error': 'All fields are required'}), 400

        if len(password) < 6:
            return jsonify({'error': 'Password must be at least 6 characters long'}), 400

        # Check if the email or contact already exists
        if User.query.filter_by(email=email).first():
            return jsonify({'error': 'Email already exists'}), 400

        if User.query.filter_by(contact=contact).first():
            return jsonify({'error': 'Contact already exists'}), 400

        # Hash the password
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Create a new User object
        new_user = User(
            first_name=first_name,
            last_name=last_name,
            contact=contact,
            email=email,
            password=hashed_password,  # Use the hashed password
            biography=biography
        )

        # Add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': 'User registered successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
