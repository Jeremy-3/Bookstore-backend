from models import db, Author, Book, Bookstore,BookstoreBook,User
from flask_migrate import Migrate
from flask import Flask, request, jsonify
from datetime import datetime, timedelta
import datetime
from functools import wraps
from flask_jwt_extended import JWTManager
from flask_jwt_extended import create_access_token
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from flask_cors import CORS  
import os
import time



BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'Store.db')}")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.environ.get("JWT_SECRET_KEY", "super-secret-key")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=24)
jwt = JWTManager(app)
CORS(app)


#Initialize SQLAlchemy
db.init_app(app)

#Initialize Flask-Migrate after db 
migrate = Migrate(app, db)



@app.route('/')
def welcome():
    return jsonify({
        'message': '📚 Welcome to the Bookstore API! 🚀',
        'info': 'Use this API to explore and manage books, authors, and bookstores.',
        'routes': {
            'Register': '/register (POST)',
            'Login': '/login (POST)',
            'Books': '/books (GET, POST,PATCH)',
            'Authors': '/Authors (GET,POST,PATCH)',
            'Bookstoes': '/bookstores (GET, POST,PATCH)',
        },
        'note': 'Make sure to include your JWT token in the headers for protected routes.'
    })

 

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    role=data.get('role')

    if User.query.filter_by(email=email).first():
        return jsonify({"msg": "Email already in use."}), 400

    new_user = User(username=username, email=email, role=role)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({"msg": "User registered successfully!"}), 201


@app.route('/login',methods=["POST"])
def login():
    time.sleep(5)
    data=request.get_json()
    email=data.get('email')
    password=data.get('password')
    
    user = User.query.filter_by(email=email).first()
    
    if user and user.check_password(password):
       access_token=create_access_token(identity=user.id)

    token_payload = {
        "user_id": user.id,
        "username": user.username,
        "access_token":access_token,
        "role": user.role
        }
   
    return jsonify({
        "message": "Login successful",
        "access_token":access_token,
        "role": user.role  
    }), 200

    return jsonify({"Message":"Invalid credentials"}), 401




        

# ROLE BASED ROUTES
def token_required(allowed_roles=None):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                # Verify JWT in request headers
                verify_jwt_in_request()

                # Get the current user ID from the token
                current_user_id = get_jwt_identity()
                current_user = db.session.get(User,current_user_id)
                print("Extracted User ID:", current_user_id)


                if not current_user:
                    return jsonify({'message': 'User not found'}), 404

                # Check if the user has the required role
                if allowed_roles and current_user.role not in allowed_roles:
                    return jsonify({'message': 'Unauthorized access'}), 403

                return f(current_user, *args, **kwargs)

            except Exception as e:
                return jsonify({'message': 'Token is invalid or expired', 'error': str(e)}), 401

        return decorated_function
    return decorator

# Admin-only route
@app.route('/admin', methods=['GET'])
@token_required(allowed_roles=['admin'])
def get_admin_data(current_user):
    if current_user.role != 'admin':
        return jsonify({'message': 'Access denied. Admins only.'}), 403
    return jsonify({'message': 'Welcome, admin!'})

# Author routes

@app.route('/authors',methods=['GET'])
@token_required(allowed_roles=['user','admin'])
def get_authors(current_user):
    authors = Author.query.all()
    return jsonify([author.to_dict() for author in authors])

@app.route('/authors/<int:id>',methods=['GET'])
@token_required(allowed_roles=['user','admin'])
def get_author_id(current_user,id):
    author = Author.query.get(id)
    if not author:
        return jsonify({"message": "Author not found"}),404
    
    return jsonify(author.to_dict())

@app.route('/authors',methods=['POST'])
@token_required(allowed_roles=['user','admin'])
def create_author(current_user):
    try:
        data=request.get_json()
        
        #check if all required fields are provided
        required_fields=['first_name','second_name','email','nationality']
        for field in required_fields:
            if field not in data or not  data[field]:
                return jsonify({"message":f"missing required fields: {field}"}), 400
        
        new_author= Author(
            first_name=data['first_name'],
            second_name=data['second_name'],
            email=data['email'],
            nationality=data['nationality'],
            user_id=current_user.id,
            bio = data.get('bio', None)
            
        ) 
        db.session.add(new_author)
        db.session.commit()
        response_data = new_author.to_dict()
        response_data["author_id"] = new_author.id
        
        return jsonify(response_data), 201
    except Exception as e:
        return jsonify({"Error":str(e)}), 500
    
@app.route('/authors/<int:id>',methods=['PATCH'])
@token_required(allowed_roles=['admin'])
def update_author(current_user, id):
    author = Author.query.get(id)    
    if not author:
        return jsonify({"message": "Author not found"}),404
   
    data=request.get_json()
        
    if 'first_name' in data:
        author.first_name=data['first_name']
    if 'second_name' in data:
        author.second_name=data['second_name']
    if 'email' in data:
        author.email=data['email']
    if 'nationality' in data:
        author.nationality=data['nationality']
    
    db.session.commit()
    
    return jsonify(author.to_dict()), 200  

@app.route('/authors/<int:id>',methods=['PUT'])
@token_required(allowed_roles=['admin'])
def full_update(current_user, id):
    author = Author.query.get(id)
    if not author:
        return jsonify({"message":"Author not found"}), 404
    
    data =request.get_json()
    
    #ensure all required fields
    required_fields=['first_name','second_name','email','nationality','bio']
    
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({"Error":f"Missing required field:{field}"}), 400
        
    # Update the existing author instance
    author.first_name = data['first_name']
    author.second_name = data['second_name']
    author.email = data['email']
    author.nationality = data['nationality']
    author.bio = data['bio']
    
    db.session.commit()
    
    return jsonify(author.to_dict()), 200    




@app.route('/authors/<int:id>',methods=['DELETE'])
@token_required(allowed_roles=['admin'])
def delete_author(current_user, id):
    author = Author.query.get(id)
    if not author:
        return jsonify({"message": "Author not found"}),404
    db.session.delete(author)
    db.session.commit()
    return jsonify({"message": f"Author {author.email} deleted"}), 200

# Books Routes

@app.route('/books', methods=['GET'])
@token_required(allowed_roles=['user','admin'])
def get_books(current_user):
    books = Book.query.all()
    return jsonify([book.to_dict() for book in books])  

@app.route('/books/<int:id>',methods=['GET'])
@token_required(allowed_roles=['user','admin'])
def get_books_id(current_user,id):
    book = Book.query.get(id)
    if not book:
        return jsonify({"message": "Book not found"}),404
    return jsonify(book.to_dict())


@app.route('/books',methods=['POST'])
@token_required(allowed_roles=['user'])
def create_book(current_user):
    try:
        data = request.get_json()
        # print(data)
        # required fields
        required_fields = ['title', 'genre','publication_date','description','author_id','book_img']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({"Error":f'Missing required field {field}'}), 400
            
        # check if author exists
        author = db.session.get(Author, data['author_id'])
        if not author:
            return jsonify({"Error": "Author not found"}), 404
        
        # convert publication_date from string to datetime
        try:
            print("Received_date", data.get("publication_date"))
           
            publication_date = datetime.datetime.strptime(str(data['publication_date']), '%Y-%m-%d').date()
        except ValueError:
            return jsonify({"Error": "Invalid date format. Use YYYY-MM-DD."}), 400
        
        # Create new book instance
        new_book =Book(
            title=data['title'],
            genre=data['genre'],
            publication_date=publication_date,
            description=data['description'],
            book_img=data['book_img'],
            author_id=data['author_id']
        )
        db.session.add(new_book)
        db.session.commit()
        
        return jsonify(new_book.to_dict()), 201
    
    except Exception as e:
        return jsonify({'error':str(e)}),400

@app.route('/books/<int:id>',methods=['DELETE'])
@token_required(allowed_roles=['admin'])
def delete_book(current_user, id):
    book = Book.query.get(id)
    if not book:
        return jsonify({"Error":f"Book {id} not found"}),404
    
    db.session.delete(book)
    db.session.commit()
    
    return jsonify({"message":f"Book {book.title} deleted"}),200


@app.route('/books/<int:id>',methods=['PATCH'])
@token_required(allowed_roles=['user','admin'])
def update_book(current_user,id):
    book = Book.query.get(id)
    if not book:
        return jsonify({"Error":f"Book {id} not found"}),404
    
    data = request.get_json()
    
    # Update only provided fields
    if 'title' in data:
        book.title = data['title']
    if 'genre' in data:
        book.genre =data['genre']
    if 'description' in data:
        book.description = data['description']
    if 'publication_date' in data:
        try:
            book.publication_date = datetime.strptime(data['publication_date'],"%Y-%m-%d").date()
        except ValueError:
            return jsonify({"Error":"Invalid date formate. Use YYYY-MM-DD"}),400
    
    db.session.commit()
    
    return jsonify(book.to_dict()), 200                

# Bookstore Routes

@app.route('/bookstores', methods=['GET'])
@token_required(allowed_roles=['admin','user'])
def get_bookstores(current_user):
    bookstores = Bookstore.query.all()
    return jsonify([bookstore.to_dict() for bookstore in bookstores])

@app.route('/bookstores/<int:id>',methods=['GET'])
@token_required(allowed_roles=['admin','user'])
def get_bookstore_id(current_user,id):
    bookstore = Bookstore.query.get(id)
    if not bookstore:
        return jsonify({"Error":f"Bookstore {id} not found"}),404
    return jsonify(bookstore.to_dict()),200

@app.route('/bookstores', methods=['POST'])
@token_required(allowed_roles=['admin'])
def create_bookstore(current_user):
    data = request.get_json()
    print(data)
    required_fields =['name','location','established_date']
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({"error":f"Missing required field: {field}"}) , 400
    
    try:
        established_date=datetime.strptime(data['established_date'],"%Y-%m-%d").date()
    
    except ValueError:
        return jsonify({"Error":"Invalid date formate. Use YYYY-MM-DD"}),400
    
    
    new_bookstore=Bookstore(
        name=data['name'],
        location=data['location'],
        established_date=established_date
    )
    
    db.session.add(new_bookstore)
    db.session.commit()
    
    return jsonify(new_bookstore.to_dict()), 201    

@app.route('/bookstores/<int:id>',methods=['PATCH'])
@token_required(allowed_roles=['admin'])
def update_bookstore(current_user, id):
    bookstore = Bookstore.query.get(id)
    if not bookstore:
        return jsonify({"Error":f"Bookstore {id} not found"}),404
    data = request.get_json()
    
    if 'name' in data:
        bookstore.name=data['name']
    if 'location' in data:
        bookstore.location=data['location']
    if 'established_date' in data:
        try:
            bookstore.established_date=datetime.strptime(data['established_date'],"%Y-%m-%d").date()
            
        except ValueError:
            return jsonify({"error":"Invalid date formate. Use YYYY-MM-DD"}),400
    
    db.session.commit()
    return jsonify(bookstore.to_dict()),200


@app.route('/bookstores/<int:id>',methods=['DELETE'])
@token_required(allowed_roles=['admin'])
def delete_bookstore(current_user,id):
    bookstore = Bookstore.query.get(id)
    if not bookstore:
        return jsonify({"Error":f"Bookstore {id} not found"}),404
    db.session.delete(bookstore)
    db.session.commit()
    return jsonify({"message":f"Bookstore {bookstore.name} deleted"}),200


#routes for relationship between books in bookstores
#adding books to a bookstore
@app.route('/bookstores/<int:bookstore_id>/books', methods=['POST'])
@token_required(allowed_roles=['admin']) 
def add_book_to_bookstore(current_user, bookstore_id):
    bookstore = Bookstore.query.get(bookstore_id)
    if not bookstore:
        return jsonify({"Error": f"Bookstore {bookstore_id} not found"}), 404

    data = request.get_json()

    # If the data is a list, loop through each book and add to the bookstore
    if isinstance(data, list):
        for item in data:
            required_fields = ['book_id', 'stock', 'price']
            for field in required_fields:
                if token_required not in item or not item[field]:
                    return jsonify({"error": f"Missing required field: {field}"}), 400
            
            # Check if the book exists
            book = Book.query.get(item['book_id'])
            if not book:
                return jsonify({"error": f"Book {item['book_id']} not found"}), 404
            
            try:
                stock = int(item['stock'])
                price = float(item['price'])
            except ValueError:
                return jsonify({"error": "Invalid stock or price"}), 400

            new_bookstore_book = BookstoreBook(
                bookstore_id=bookstore_id,
                book_id=item['book_id'],
                stock=stock,
                price=price
            )
            db.session.add(new_bookstore_book)
        
        db.session.commit()  # Commit once for all books
        return jsonify({"message":f"Books added successfully to {bookstore.name}"}), 201

    else:  # If data is a single book
        required_fields = ['book_id', 'stock', 'price']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({"error": f"Missing required field: {field}"}), 400
            
        # Check if the book exists
        book = Book.query.get(data['book_id'])
        if not book:
            return jsonify({"error": f"Book {data['book_id']} not found"}), 404
        
        try:
            stock = int(data['stock'])
            price = float(data['price'])
        except ValueError:
            return jsonify({"error": "Invalid stock or price"}), 400
        
        new_bookstore_book = BookstoreBook(
            bookstore_id=bookstore_id,
            book_id=data['book_id'],
            stock=stock,
            price=price
        )
        db.session.add(new_bookstore_book)
        db.session.commit()

        return jsonify(new_bookstore_book.to_dict()), 200

# getting all the books in a bookstore
@app.route('/bookstores/<int:bookstore_id>/books',methods=['GET'])
@token_required(allowed_roles=['user','admin'])
def get_books_in_bookstore(current_user, bookstore_id):
    bookstore = Bookstore.query.get(bookstore_id)
    if not bookstore:
        return jsonify({"Error":f"Bookstore {bookstore_id} not found"}),404
    bookstore_books = BookstoreBook.query.filter_by(bookstore_id=bookstore_id).all()
    
    return jsonify([{
        'book':bookstore_book.book.to_dict(),
        'stock':bookstore_book.stock,
        'price':bookstore_book.price
    } for bookstore_book in bookstore_books])

# getting specific book in the bookstore
@app.route('/bookstores/<int:bookstore_id>/books/<int:book_id>',methods=['GET'])
@token_required(allowed_roles=['admin','user'])
def get_book_from_bookstore(current_user,bookstore_id,book_id):
    bookstore = Bookstore.query.get(bookstore_id)
    if not bookstore:
        return jsonify({"Error":f"Bookstore {bookstore_id} not found"}),404
    bookstore_book = BookstoreBook.query.filter_by(bookstore_id=bookstore_id,book_id=book_id).first()
    if not bookstore_book:
        return jsonify({"Error":f"Book {book_id} not found in bookstore {bookstore_id}"}), 404
    
    return jsonify({
        'book':bookstore_book.book.to_dict(),
        'stock':bookstore_book.stock,
        'price':bookstore_book.price    
        }),200

# Update a bookstorebook (stock and price) for a specific book 
    
@app.route('/bookstores/<int:bookstore_id>/books/<int:book_id>', methods=['PATCH'])
@token_required(allowed_roles=['admin'])
def update_bookstore_book(current_user,bookstore_id, book_id):
    bookstore = Bookstore.query.get(bookstore_id)
    if not bookstore:
        return jsonify({"error": f"Bookstore {bookstore_id} not found"}), 404

    bookstore_book = BookstoreBook.query.filter_by(bookstore_id=bookstore_id, book_id=book_id).first()
    if not bookstore_book:
        return jsonify({"error": f"Book {book_id} not found in bookstore {bookstore_id}"}), 404

    data = request.get_json()

    if 'stock' in data:
        try:
            bookstore_book.stock = int(data['stock'])
        except ValueError:
            return jsonify({"error": "Invalid stock value"}), 400
    
    if 'price' in data:
        try:
            bookstore_book.price = float(data['price'])
        except ValueError:
            return jsonify({"error": "Invalid price value"}), 400

    db.session.commit()

    return jsonify({
        'book': bookstore_book.book.to_dict(),
        'stock': bookstore_book.stock,
        'price': bookstore_book.price
    }), 200
    
# delete a specific book from the bookstore    
    
@app.route('/bookstores/<int:bookstore_id>/books/<int:book_id>', methods=['DELETE'])
@token_required(allowed_roles=['admin'])
def delete_bookstore_book(current_user,bookstore_id, book_id):
    bookstore = Bookstore.query.get(bookstore_id)
    if not bookstore:
        return jsonify({"error": f"Bookstore {bookstore_id} not found"}), 404

    bookstore_book = BookstoreBook.query.filter_by(bookstore_id=bookstore_id, book_id=book_id).first()
    if not bookstore_book:
        return jsonify({"error": f"Book {book_id} not found in bookstore {bookstore_id}"}), 404

    db.session.delete(bookstore_book)
    db.session.commit()

    return jsonify({"message": f"Book {book_id} deleted from bookstore {bookstore.name}"}), 200
    
# No roles specified, so any logged-in user can access    
    
@app.route('/profile', methods=['GET'])
@token_required(allowed_roles=["user","admin"])  
def profile(current_user):
    is_author = Author.query.filter_by(user_id=current_user.id).first() is not None
    return jsonify({
        'id': current_user.id,
        'username': current_user.username,
        'email': current_user.email,
        'role': current_user.role,
        'is_author': is_author,
        'author_id': Author.query.filter_by(user_id=current_user.id).first().id if is_author else None
    })



if __name__ == '__main__':
    app.run(debug=True, port=8000)
