from flask import Blueprint, request, jsonify
from authors_app.models.book import Book
from authors_app.models.user import User
from authors_app import db

book = Blueprint('book', __name__, url_prefix='/api/v1/auth')  # creating an instance object

@book.route('/register', methods=['POST'])
def register_book():
    try:
        # extracting request data
        data = request.json
        title = data.get('title')
        description = data.get('description')
        price = data.get('price')
        price_unit = data.get('price_unit')
        pages = data.get('pages')
        publication_date = data.get('publication_date')
        isbn = data.get('isbn')
        genre = data.get('genre')
        user_id = data.get('user_id')
        # image = data.get('user_image')

        # basic input validation
        if not all([title, description, price, price_unit, pages, publication_date, isbn, genre, user_id]):
            return jsonify({'error': 'All fields are required'}), 400

        # creating a new book
        new_book = Book(
            title=title,
            description=description,
            # image=image,
            price=float(price),
            price_unit=price_unit,
            pages=int(pages),
            publication_date=publication_date,
            isbn=isbn,
            genre=genre,
            user_id=int(user_id)
        )

        # adding and committing to the database
        db.session.add(new_book)
        db.session.commit()
        # Building a response message
        return jsonify({"message": f"Book '{new_book.title}', ID '{new_book.id}' has been uploaded"}), 201

    except Exception as e:
        # Handle exceptions appropriately
        return jsonify({'error': str(e)}), 500
