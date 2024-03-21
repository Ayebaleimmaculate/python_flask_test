from flask import Flask, Blueprint, request, jsonify
from flask_bcrypt import bcrypt
from authors_app.models.user import User
from authors_app import db

# Create Flask application
app = Flask(__name__)

# Register the 'auth' blueprint
auth = Blueprint('auth', __name__)

@app.route('/api/v1/auth/register', methods=['POST'])
def register():
    try:
        # Retrieve data from the request JSON
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
            password=hashed_password,
            biography=biography
        )

        # Add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': 'User registered successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Register the 'auth' blueprint with the application
app.register_blueprint(auth)

if __name__ == '__main__':
    app.run(debug=True)
