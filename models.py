from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()

class User(db.Model,SerializerMixin):
    __tablename__ ="users"
    
    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(100), nullable=False)
    email=db.Column(db.String, nullable=False,unique=True)
    password_hash=db.Column(db.String(255), nullable=False)
    role=db.Column(db.String(20),nullable=False,default="user")
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

# Method to hash password before storing
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Method to convert user object to dictionary
def to_dict(self):
    return{
        'id':self.id,
        'email':self.email,
        'role':self.role,
        'created_at':self.created_at
        }



class Author(db.Model):
    __tablename__ = 'authors'

    id = db.Column(db.Integer, primary_key=True)
    user_id =db.Column(db.Integer,nullable=True)
    first_name = db.Column(db.String(25), nullable=False)
    second_name = db.Column(db.String(25), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    nationality = db.Column(db.String(50), nullable=False)
    bio = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    # Relationship to books
    books = db.relationship('Book', back_populates='author', cascade="all, delete-orphan")
   
    # validations for author
    @validates('nationality')
    def validate_nationality(self, key, value):
        if len(value) < 2:
            raise ValueError("Nationality must be at least 2 characters long")
        return value

    @validates('email')
    def validate_email(self, key, email):
        if '@' not in email:
            raise ValueError("Invalid email address missing '@'")
        if len(email) > 50:
            raise ValueError("Email address too long")
        return email
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'first_name': self.first_name,
            'second_name': self.second_name,
            'email': self.email,
            'nationality': self.nationality,
            'bio': self.bio,
            'created_at': self.created_at,
            'books': [{'id': book.id, 'title': book.title} for book in self.books]  # Only book IDs & titles
        }

class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(50), nullable=False)
    publication_date = db.Column(db.Date, nullable=True)
    description = db.Column(db.String(255), nullable=True)
    book_img =db.Column(db.String,nullable=True)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'), nullable=False)

    # Relationships
    author = db.relationship('Author', back_populates='books')
    
    # Validations
    @validates('title')
    def validate_title(self, key, value):
        if len(value) < 3:
            raise ValueError("Title must be at least 3 characters long")
        return value

    @validates('genre')
    def validate_genre(self, key, value):
        allowed_genres = ['Fiction', 'Non-Fiction', 'Mystery', 'Fantasy', 'Sci-Fi', 'Romance', 'Action', 'Drama']
        if value not in allowed_genres:
            raise ValueError(f"Genre must be one of the following: {', '.join(allowed_genres)}")
        return value
    
    
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'genre': self.genre,
            'publication_date': self.publication_date.strftime("%Y-%m-%d"),
            'description': self.description,
            'book_img': self.book_img,
            'author_id': self.author_id  # Only the author ID, not full details
        }

class Bookstore(db.Model):
    __tablename__ = 'bookstores'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(150), nullable=False)
    established_date = db.Column(db.Date, nullable=True)

    # Relationship to BookstoreBook
    books = db.relationship('BookstoreBook', back_populates='bookstore', cascade='all, delete-orphan')
    
    
    # Validations
    @validates('name')
    def validate_name(self, key, value):
        if len(value) < 3:
            raise ValueError("Bookstore name must be at least 3 characters long")
        return value
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'location': self.location,
            "established_date": self.established_date.strftime("%Y-%m-%d"),
            # List of books in this bookstore, showing only book_id and stock details
            'inventory': [{'book_id': bb.book_id, 'stock': bb.stock, 'price': bb.price} for bb in self.books]
        }

class BookstoreBook(db.Model):
    __tablename__ = 'bookstore_books'

    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    bookstore_id = db.Column(db.Integer, db.ForeignKey('bookstores.id'), nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)
    price = db.Column(db.Float, nullable=False)

    # Relationships
    book = db.relationship('Book')
    bookstore = db.relationship('Bookstore', back_populates='books')
    
    
    # validations 
    @validates('stock')
    def validate_stock(self, key, value):
        if value < 0:
            raise ValueError("Stock cannot be negative")
        return value

    @validates('price')
    def validate_price(self, key, value):
        if value <= 0:
            raise ValueError("Price must be greater than 0")
        return value
    
    
     
    def to_dict(self):
        return {
            'id': self.id,
            'book_id': self.book_id,
            'bookstore_id': self.bookstore_id,
            'stock': self.stock,
            'price': self.price
        }
        
        
class Feedback (db.Model):
    __tablename__ ='feedbacks'
    
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String, nullable=False)
    email=db.Column(db.String, nullable=False)
    # subject=db.Column(db.String, nullable=False)
    message=db.Column(db.String(300), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    @validates('name')
    def validate_name(self, key, value):
        if len(value) < 0:
            raise ValueError("Name must be at least 20 characters long")
        return value
    
    @validates('email')
    def validate_email(self,key,value):
        if '@' not in value:
            raise ValueError("Invalid email address missing '@'")
        if len(value) > 50:
            raise ValueError("Email address too long")
        return value
    
    # @validates('subject')
    # def validate_subject(self, key, value):
    #     if not value or value.strip() == "":
    #         raise ValueError("Subject cannot be empty")
    #     if len(value) < 3:
    #         raise ValueError("Subject must be at least 3 characters long")
    
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            # 'subject': self.subject,
            'message': self.message,
            'created_at': self.created_at
        }