# Model for User/Book/Review
# Note: Review for future enhancement
import uuid, json
from flask import Flask, jsonify
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, asc, desc, exists, text, inspect
from flask_sqlalchemy import SQLAlchemy
# Import the app from bookstore
from bookstore import app
# Use for setup database, later to use back bookstore config
# app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bookstore-dev.db'
# Create db session from SQLAlchmey with bookstore app
db = SQLAlchemy(app)
#----------------------------------------------------------------------------------------------------------------------
# User Model
class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    user_username = db.Column(db.String(10), unique=True)
    user_password = db.Column(db.String(255), nullable=False)
    user_created_date = db.Column(db.DateTime, server_default=text("CURRENT_TIMESTAMP"))
    user_updated_date = db.Column(db.DateTime, server_default=text("CURRENT_TIMESTAMP"), onupdate=text("CURRENT_TIMESTAMP"))
# ---------------------------------------------------------------------------------------------------------------------
# Create add_user function to add the username and password
    def add_user(username, password):
        rowcount = 0
        try: 
            # Raw SQL method to insert record to return rowcount
            # result = db.session.execute(db.insert(User).values(user_username=username, user_password=password))
            # rowcount = result.rowcount
            # ORM method to insert record to return rowcount
            # Drawback: Additional query to affect perofrmance as the larger size of database
            user = User(user_username=username, user_password=password)
            db.session.add(user)
            db.session.flush()
            rowcount = db.session.query(User).filter_by(user_username=username).count()
            db.session.commit()            
        except Exception as e:
            print(f"Error in registering user {e}")
            db.session.rollback()
            raise()
        return rowcount
# ---------------------------------------------------------------------------------------------------------------------
# Create login_time function to update the last login time.
    def login_time(username):
        user = User.query.filter_by(user_username=username).first()
        user.user_updated_date = datetime.now()
        db.session.commit()
        return user
# ---------------------------------------------------------------------------------------------------------------------
# Create find_user function to get the user by username
    def find_user(username):
        user = None
        try:
            user = db.session.query(User).filter_by(user_username=username).all()
        except Exception as e:
            print(f"Error in retrieving user {e}")
        return user
#======================================================================================================================
# Book Model
class Book(db.Model):
    book_id = db.Column(db.Integer, primary_key=True)
    book_uuid = db.Column(db.String(36), unique=True)
    book_title = db.Column(db.String(255), nullable=False)
    book_author = db.Column(db.String(255), nullable=False)
    book_description = db.Column(Text)
    book_quantity = db.Column(db.Integer)
    # book_created_date = db.Column(db.DateTime, default=datetime.utcnow)
    # book_updated_date = db.Column(db.DateTime, default=datetime.utcnow)
    book_created_date = db.Column(db.DateTime, server_default=text("CURRENT_TIMESTAMP"))
    book_updated_date = db.Column(db.DateTime, server_default=text("CURRENT_TIMESTAMP"), onupdate=text("CURRENT_TIMESTAMP"))
    reviews = db.relationship('Review', backref='related_book', lazy=True)
#======================================================================================================================
    # Create string representation for Book Model
    def __str__(self):
        return f"{self.book_id},{self.book_uuid},{self.book_title},{self.book_author},{self.book_description},{self.book_quantity}"
# ---------------------------------------------------------------------------------------------------------------------
    # Create add_book function to adding the new book
    def add_book(title, author, description, quantity):
        book = Book(book_uuid=str(uuid.uuid4()), book_title=title, book_author=author, book_description=description, book_quantity=quantity)
        db.session.add(book)
        db.session.commit()
# ---------------------------------------------------------------------------------------------------------------------
    # Create all_books function to load all book
    def all_books():
        books = Book.query.order_by(desc(Book.book_id)).all()
        return books
# ---------------------------------------------------------------------------------------------------------------------
    # Create find_title function to find the book by title
    def find_title(title):
        book = db.session.query(Book).filter(Book.book_title == title).all()
        return book
# ---------------------------------------------------------------------------------------------------------------------
    # Create find_uuid function to find the book by uuid
    def find_uuid(uuid):
        book = db.session.query(Book).filter(Book.book_uuid== uuid).all()
        return book
# ---------------------------------------------------------------------------------------------------------------------
    # Create one_book function to find one book by id
    def one_book(id):
        book = db.session.query(Book).get(id)
        return book
# ---------------------------------------------------------------------------------------------------------------------
    # Create update_book function to update title, author, description, quantity
    def update_book(id, title, author, description, quantity):
        book = db.session.query(Book).filter_by(book_id=id).update({'book_title': title, 'book_author': author, 'book_description': description, 'book_quantity': quantity})
        db.session.commit()
        return book
# ---------------------------------------------------------------------------------------------------------------------
    # Create delete_book function to delete the book by id
    def delete_book(id):
        book = db.session.query(Book).filter(Book.book_id == id).delete()
        db.session.commit()
        return book
# ---------------------------------------------------------------------------------------------------------------------
    # Create delete_book_uuid function to delete the book by uuid
    def delete_book_uuid(uuid):
        book = db.session.query(Book).filter(Book.book_uuid == uuid).delete()
        db.session.commit()
        return book
# ---------------------------------------------------------------------------------------------------------------------
    # Create update_book_uuid function to update title, author, description, quantit
    def update_book_uuid(uuid, title, author, description, quantity):
        book = db.session.query(Book).filter_by(book_uuid=uuid).update({'book_title': title, 'book_author': author, 'book_description': description, 'book_quantity': quantity})
        db.session.commit()
        return book
# ---------------------------------------------------------------------------------------------------------------------
    # Create book_search function to search books by criteria: title/author/description/quantity range
    def book_search(search_dictionary):
        books = None
        type = search_dictionary["type"]
        title, author, description, quantity_min, quantity_max = "", "", "", 0, 0
        if type == "title":
            title = search_dictionary["search_input"]
        elif type == "author":
            author = search_dictionary["search_input"]
        elif type == "description":
            description = search_dictionary["search_input"]
        else:
            quantity_min = search_dictionary["quantity_min"]
            quantity_max = search_dictionary["quantity_max"]
        if type == "title":
            if title:
                books = db.session.query(Book).filter(Book.book_title.like(f"%{title}%")).order_by(asc(Book.book_id)).all()
        elif type == "author":
            if author:
                books = db.session.query(Book).filter(Book.book_author.like(f"%{author}%")).order_by(asc(Book.book_id)).all()
        elif type == "description":
            if description:
                books = db.session.query(Book).filter(Book.book_description.like(f"%{description}%")).order_by(asc(Book.book_id)).all()
        elif type == "quantity":
            if quantity_min and quantity_max:
                books = db.session.query(Book).filter(Book.book_quantity.between(quantity_min, quantity_max)).order_by(asc(Book.book_id)).all()
                print("model", books)
        else:
            books = None
        return books
# =====================================================================================================================
# Book API
    # Create api_all_books function to get all books without the field of book_id
    def api_all_books():
        books = db.session.query(Book.book_uuid, Book.book_title, Book.book_author, Book.book_description, Book.book_quantity, Book.book_created_date, Book.book_updated_date).order_by(desc(Book.book_id)).all()    
        return books
# ---------------------------------------------------------------------------------------------------------------------
    # Create api_one_book function to get one book without the field of book_id
    def api_one_book(book_uuid):
        # book = db.session.query(Book).filter_by(book_id=book_id).first()        
        book = db.session.query(Book.book_uuid, Book.book_title, Book.book_author, Book.book_description, Book.book_quantity, Book.book_created_date, Book.book_updated_date).filter(Book.book_uuid == book_uuid).all()
        return book
# ---------------------------------------------------------------------------------------------------------------------
    # Create get_book_dictionary function to convert the book list to dictionary 
    # If is_API is True, it does not get book_id
    def get_book_dictionary(book, is_API=False):
        book_dictionary = {}
        if len(book) == 1:
            book_dictionary = {
                "uuid": str(book[0].book_uuid),
                "title": book[0].book_title,
                "author": book[0].book_author,
                "description": book[0].book_description,
                "quantity": book[0].book_quantity,
                "createdDate": book[0].book_created_date.isoformat(),
                "updatedDate": book[0].book_updated_date.isoformat(),
            }

            if not is_API:
                book_dictionary["id"] = book[0].book_id
        return book_dictionary
# =====================================================================================================================
# Review Model
class Review(db.Model):
    review_id = db.Column(db.Integer, primary_key=True)
    review_uuid = db.Column(db.String(36), unique=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.book_id'), nullable=False)
    review_is_anonymous = db.Column(db.Boolean, default=True)
    review_nickname = db.Column(db.String(255), nullable=True)
    review_email = db.Column(db.String(255), nullable=True) 
    review_rating = db.Column(db.Integer, nullable=False)
    review_text = db.Column(Text)
    review_date = db.Column(db.DateTime, server_default=text("CURRENT_TIMESTAMP"))