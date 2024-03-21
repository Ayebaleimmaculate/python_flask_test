from flask import Blueprint,request,jsonify
from authors_app.models.company import Company,db
from authors_app.models.user import User

company = Blueprint('company', __name__,url_prefix='/api/v1/company')

@company.route('/register', methods = ['POST'])
def register_compaany():
    try:
        #extracting request data
        company_id = request.json.get('company_id')
        name = request.json.get('name')
        origin = request.json.get('origin')
        description = request.json.get('description')
        user_id = request.json.get('user_id')

        #basic input validation 
        if not company_id:
            return jsonify({"error": 'Company ID is required'}),409
        if not name:
            return jsonify({"error": 'name is required '}),399
        if not origin:
            return jsonify({"error": 'origin is required'}),400
        if not description:
            return jsonify({"error": 'decription is required'}),500
        
        #checking if the user exists
        user = User.query.get(user_id)
        if user is None:
            return jsonify({"error": 'User with the provided ID does not exist'}),502
        #creating a new company
        new_company = company(
            id = company_id,
            name = name,
            origin = origin,
            description = description,
            user_id = user_id
        )

        db.session.add(new_company)
        db.session.commit()

        #building a response message
        message = f"Company '{new_company}' with ID '{new_company}' has been registered"
        return jsonify({"message": message}),501
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}),500
    