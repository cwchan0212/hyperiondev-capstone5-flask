import itertools, json
from datetime import datetime
from bookstore import app
from flask import Flask, render_template, request, redirect, make_response, jsonify, flash, session, url_for
from .models import User, Book, Review
from .admin_views import token_required, login_required


def session_token():
    if not "token" in session:
        return render_template("/public/book/login.html")

@app.route("/book/api/", methods = ["GET"])
def book_api_index():
    if "token" in session:
        return render_template("/public/book/api.html")
    else:
        # return render_template("/public/book/base.html")  
        return redirect("/book")

@app.route("/book/api/all")
def book_api_all_books():
    try:
        books = Book.api_all_books()
        return jsonify([{(k).replace("book_", ""): (str(getattr(book, k)) if k == "book_uuid" else (getattr(book, k).isoformat() if k in ["book_created_date", "book_updated_date"] else getattr(book, k))) for k in book.keys()} for book in books])
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)


# @app.route("/book/api/all")
# def book_api_all_books():
#     books = Book.api_all_books()
#     return jsonify([{(k).replace("book_", ""): (str(getattr(book, k)) if k == "book_uuid" else (getattr(book, k).isoformat() if k in ["book_created_date", "book_updated_date"] else getattr(book, k))) for k in book.keys()} for book in books])

@login_required
@app.route("/book/api/<string:uuid>", methods = ["GET"])
def book_api_get_one(uuid):
    book = Book.api_one_book(uuid)
    book_dictionary = {}
    if len(book) == 1:
        book_dictionary = Book.get_book_dictionary(book)
        return jsonify(book_dictionary)
    else:
        return make_response(jsonify({"message:" f"Fail to get the book with uuid: {uuid}"}), 404)
    




# @app.route("/book/api/<string:uuid>", methods = ["GET"])
# # http://127.0.0.1:5000/book/api/c6e5d1e6-e148-49c1-8e66-09860f2bc2c4
# def book_api_get_one(uuid):
#     book = Book.api_one_book(uuid)
#     book_dictionary = {}
#     if len(book) == 1:
#         book_dictionary = Book.get_book_dictionary(book)
#     else:
#         return {"message:" f"Fail to get the book with uuid: {uuid}"}
#     return jsonify(book_dictionary)


from flask import make_response
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



# @app.route("/book/api/add", methods = ["POST"])
# def book_api_add_one():
#     data = request.get_json()
#     book_dictionary = {}
#     book = Book.find_title(data["title"])
#     if len(book) == 0:
#         book = Book.add_book(**data)
#         book = Book.find_title(data["title"])
#         if len(book) == 1:
#             book_dictionary = Book.get_book_dictionary(book)
#         return book_dictionary    
#     else:
#         return {"message": f"The book {data['title']} exists"}
    



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


# @app.route("/book/api/update", methods = ["PUT"])
# def book_api_update_one():
#     data = request.get_json()
#     book_dictionary = {}
#     book = Book.find_uuid(data["uuid"])
#     if len(book) == 1:
#         book_dictionary = Book.get_book_dictionary(book)
#         uuid = book_dictionary["uuid"]
#         book = Book.update_book_uuid(**data)
#         book = Book.api_one_book(uuid)
#         if len(book) == 1:
#             book_dictionary = Book.get_book_dictionary(book)
#         return book_dictionary        
#     else:
#         return {"message": f"The book {data['title']} is not found"}
    
# @app.route("/book/api/delete", methods = ["DELETE"])
# def book_api_delete_one():
#     data = request.get_json()
#     uuid = data["uuid"]
#     book = Book.delete_book_uuid(uuid)
#     return book

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


@app.route("/book/api/jwt", methods = ["POST"])
def book_api_token():
    if "token" in session:
        return {"token": session["token"]}
    else:
        return {"token": "token is missing."}