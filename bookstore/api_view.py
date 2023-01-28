# Views for api view function
import itertools, json
from datetime import datetime
from bookstore import app
from flask import Flask, render_template, request, redirect, make_response, jsonify, flash, session, url_for
from .models import User, Book, Review
from .admin_views import token_required, login_required, is_logged

# =====================================================================================================================
# Create session_token function to check existence of token session
def session_token():
    if not "token" in session:
        return render_template("/public/book/login.html")
    
# ---------------------------------------------------------------------------------------------------------------------
# Route to book api index
@app.route("/book/api/", methods = ["GET"])
def book_api_index():
    if "token" in session:
        return render_template("/public/book/api.html")
    else:
        return redirect("/book")
    
# ---------------------------------------------------------------------------------------------------------------------
# Route to book_api_all_books to load all books in JSON
@app.route("/book/api/all")
def book_api_all_books():
    try:
        books = Book.api_all_books()
        return jsonify([{(k).replace("book_", ""): (str(getattr(book, k)) if k == "book_uuid" else (getattr(book, k).isoformat() if k in ["book_created_date", "book_updated_date"] else getattr(book, k))) for k in book.keys()} for book in books])
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)

# ---------------------------------------------------------------------------------------------------------------------
# Route to book_api_get_one to get 1 book in JSON
@login_required
@token_required
@app.route("/book/api/<string:uuid>", methods = ["GET"])
def book_api_get_one(uuid):
    book = Book.api_one_book(uuid)
    book_dictionary = {}
    if len(book) == 1:
        book_dictionary = Book.get_book_dictionary(book)
        return jsonify(book_dictionary)
    else:
        return make_response(jsonify({"message:" f"Fail to get the book with uuid: {uuid}"}), 404)
    
# ---------------------------------------------------------------------------------------------------------------------
# Route to book_api_add_one to add 1 book in JSON
@login_required
@token_required
@app.route("/book/api/add", methods = ["POST"])
def book_api_add_one():
    data = request.get_json()
    book_dictionary = {}
    try:
        book = Book.find_title(data["title"])
        if len(book) == 0:
            book = Book.add_book(**data)
            book = Book.find_title(data["title"])
            if len(book) == 1:
                book_dictionary = Book.get_book_dictionary(book)
            return jsonify(book_dictionary)   
        else:
            return make_response({"message": f"The book {data['title']} already exists"}, 400)
    except Exception as e:
        return make_response({"message": str(e)}, 500)

# ---------------------------------------------------------------------------------------------------------------------
# Route to book_api_update_one to update 1 book in JSON
@login_required
@token_required
@app.route("/book/api/update", methods = ["PUT"])
def book_api_update_one():
    data = request.get_json()
    if not data:
        return jsonify({"message": "Bad Request: No data provided"}), 400
    if "uuid" not in data:
        return jsonify({"message": "Bad Request: uuid is required"}), 400
    book = Book.find_uuid(data["uuid"])
    if len(book) == 1:
        book_dictionary = Book.get_book_dictionary(book)
        uuid = book_dictionary["uuid"]
        book = Book.update_book_uuid(**data)
        book = Book.api_one_book(uuid)
        if len(book) == 1:
            book_dictionary = Book.get_book_dictionary(book)
            return jsonify(book_dictionary)
        else:
            return jsonify({"message": "The book does not exist"}), 500
    else:
        return jsonify({"message": f"The book {data['title']} is not found"}), 404

# ---------------------------------------------------------------------------------------------------------------------
# Route to book_api_delete_one to delete 1 book in JSON
@login_required
@token_required
@app.route("/book/api/delete", methods=["DELETE"])
def book_api_delete_one():
    try:
        data = request.get_json()
        if data is None or "uuid" not in data:
            return jsonify({"message": "Bad Request: 'uuid' field is missing in the request"}), 400
        uuid = data["uuid"]
        book = Book.query.filter_by(book_uuid=uuid).first()
        if book is None:
            return jsonify({"message": "Not Found: No book found with the given uuid"}), 404        
        Book.delete_book_uuid(uuid)
        return jsonify({f"message": "Successfully deleted book with uuid: {uuid}"}), 200
    except Exception as e:
        return jsonify({"message": "Internal Server Error: {}".format(str(e))}), 500   

# ---------------------------------------------------------------------------------------------------------------------
# Route to book_api_token
# @app.route("/book/api/jwt", methods = ["GET", "POST"])
# def book_api_token():
#     if "token" in session:
#         return jsonify({"token": session["token"]})
#     else:
#         return jsonify({"token": "token is missing."})