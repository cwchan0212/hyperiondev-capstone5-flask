import itertools
from datetime import datetime
from bookstore import app
from flask import Flask, render_template, request, redirect, make_response, jsonify, flash, session, url_for
from .models import User, Book, Review






# ---------------------------------------------------------------------------------------------------------------------
# Book functions
# 
# Route to the book index page
@app.route("/book")
def book_index():
    print(f"book index")
    books = Book.all_books()
    print(type(books), books)
    return render_template("public/book/base.html", books=books)

@app.route("/book/contact")
def book_contact():
    return redirect("/book#contact")

@app.route("/book/form", methods = ["GET", "POST"]) 
def book_form():

    book_action = request.form["book_action"] if "book_action" in request.form else ""
    book_action_save = request.form["book_action_save"] if "book_action_save" in request.form else ""
    message, book_dictionary = None, {}

    if request.method == "GET":
        return render_template("public/book/form.html", book_action=book_action, book_dictionary=book_dictionary)

    if request.method == "POST": 

        # print(f"book_action={book_action}, book_action_save={book_action_save}")
        if book_action == "add":
            if book_action_save == "":
                print(f"[book_form]: Load the new book form [{book_action}]")
                return render_template("public/book/form.html", book_action=book_action, book_dictionary=book_dictionary)
                # new form
            else:
                message, book_dictionary  = get_book_dictionary(request.form)
                if message:
                    print(f"[book_form]: error(s) found in the form [{book_action}]")
                    flash(message)
                    return render_template("public/book/form.html", book_dictionary=book_dictionary)
                else:
                    print(f"[book_form]: check any duplicated books [{book_action}]")
                    title = book_dictionary["title"]
                    book = Book.find_title(title)
                    if book:
                        print(f"[book_form]: {title} - {len(book)} founds. [{book_action}]")
                        message =f"The <b>{title}</b> exists in our records."
                        flash(message)
                        return render_template("public/book/form.html", book_action="add", book_dictionary=book_dictionary)
                    else:
                        print(f"[book_form]: Add a new book {title} successfully [{book_action}]")
                        Book.add_book(**book_dictionary)
                        book_dictionary = {}
                        message =f"The <b>{title}</b> is added successfully."
                        flash(message)
                        return render_template("public/book/form.html", book_action="add", book_dictionary={})
                    # return redirect(request.url)
                    
        elif book_action == "edit":
            book_id = request.form["book_id"] if "book_id" in request.form else None
            if book_action_save == "":
                print(f"[book_form]: Load the new book form [{book_action}]")
                book = Book.one_book(book_id)
                book_dictionary = {
                    "book_id": book.book_id,
                    "uuid": book.book_uuid,
                    "title": book.book_title,
                    "author": book.book_author,
                    "description": book.book_description,
                    "quantity": book.book_quantity,
                    "created_date": book.book_created_date,
                    "updated_date": book.book_updated_date
                }
                return render_template("public/book/form.html", book_action=book_action, book_dictionary=book_dictionary)
            else:
                print(f"[book_form]: Edit book {book_id} successfully [{book_action}]")
                message, book_dictionary = get_book_dictionary(request.form)
                book_dictionary["id"] = book_id
                book = Book.update_book(**book_dictionary)
                message = f"The book <b>{book_dictionary['title']}</b> is updated successfully." 
                flash(message)
                books = Book.all_books()
                return render_template("public/book/index.html", book_action=book_action, books=books)
        elif book_action == "remove":
            book_id = request.form["book_id"] if "book_id" in request.form else None
            if book_id != "":
                print(f"[book_form]: Attempt to delete a book {book_id} [{book_action}]")
                book = Book.one_book(book_id)
                title = book.book_title
                book = Book.delete_book(book_id)
                if book:
                    print(f"[book_form]: Delete a book {book_id} successfully [{book_action}]")
                    books = Book.all_books()
                    message = f"The book <b>{title}</b> is deleted successfully."
                    flash(message)
                    return render_template("public/book/index.html", books=books)
                else:
                    print(f"[book_form]: No book found with {book_id} [{book_action}]")
                    message = f"No book is found to be deleted."
                    flash(message)
                    books = Book.all_books()
                    return render_template("public/book/index.html", books=books)
            else:
                message = f"No book id is found."
                print(f"[book_form]: No book id found to deleted [{book_action}]")
                flash(message)
                books = Book.all_books()
                return render_template("public/book/index.html", books=books)

        else:  
            print(f"[book_form]: Any other cases, load the book index page [{book_action}]")          
            books = Book.all_books()
            return render_template("public/book/index.html", books=books)
        # return render_template("public/book/form.html", book_dictionary=book_dictionary)


@app.route("/book/search", methods = ["GET", "POST"])
def book_search():
    message = ""
    search_dictionary = {}
    books = None
    if request.method == "GET":
        return render_template("/public/book/index.html", search_dictionary=search_dictionary)
    else:
        search = request.form
        search_dictionary = {}
        search_field_list = ["search_criteria", "search_input", "quantity_min", "quantity_max"]
        for key, value in request.form.items():
            search_dictionary[key] = value.strip()
            

        if search_dictionary["search_criteria"] != "title" and search_dictionary["search_criteria"] != "author" and search_dictionary["search_criteria"] != "description" and search_dictionary["search_criteria"] != "quantity" or search_dictionary["search_criteria"] =="Search criteria...":
            message = f"Please select <b>SEARCH CRITERIA</b>."
            
        else: 
            if search_dictionary["search_criteria"] == "title" or search_dictionary["search_criteria"] == "author" or search_dictionary["search_criteria"] == "description":
                if search_dictionary["search_input"] == "":
                    message = f"Please enter <b>{search_dictionary['search_criteria'].upper()}</b>."
            elif search_dictionary["search_criteria"] == "quantity":
                if search_dictionary["quantity_min"] == "":
                    message = f"The <b>MINIMUM</b> quantity must not be blank."
                elif search_dictionary["quantity_max"] == "":
                    message = f"The <b>MAXIMUM</b> quantity must not be blank."
                else:
                    if float(search_dictionary["quantity_min"]) > float(search_dictionary["quantity_max"]):
                        message = f"The <b>MINIMUM</b> quantity must not be less than the <b>MAXIMUM</b> quantity."

        if message:
            print(message)
            flash(message)

            return render_template("public/book/index.html", search_dictionary=search_dictionary)
        else:
            type = search_dictionary["search_criteria"] 
            search_dictionary["type"] = type       
            search_input = search_dictionary["search_input"]
            quantity_min = search_dictionary["quantity_min"]
            quantity_max  = search_dictionary["quantity_max"]
            if type == "title" or type == "author" or type == "description" and search_input:                
                # books = Book.book_search(type, search_input)
                books = Book.book_search(search_dictionary)
            elif type == "quantity" and quantity_min and quantity_max:
                books = Book.book_search(search_dictionary)
            return render_template("public/book/index.html", search_dictionary=search_dictionary, books=books)


def get_book_dictionary(form_dictionary):
    book_field_list = ["title", "author", "description", "quantity"]
    book_dictionary = {}
    count, message = 0, None

    for key, value in form_dictionary.items():
        # print("key", key)
        if value.strip() == "":
            message = f"The field <b>{key.upper()}</b> cannot be blank."
            flash(message)
            # return redirect(request.url)
        else:
            if key in book_field_list:
                book_dictionary[key] = value.strip()
                
    return [message, book_dictionary]

#----------------------------------------------------------------------------------------------------------------------
@app.template_filter("datetime")
def datetime(dt):
    return dt.strftime("%Y-%m-%d %H:%M:%S")

@app.template_filter("clean_date")
def clean_date(dt):
    return dt.strftime("%d %b %Y")

# @app.route("/")
# def index():
#     return render_template("public/index.html")

# @app.route("/about")
# def about():
#     return "<h1>about</h1>"

# @app.route("/json", methods = ["POST"])
# def json():

#     if request.is_json:
#         req = request.get_json()
#         print(req)
#         response = {
#             "message": "JSON received",
#             "name": req.get("name")
#         }
#         res = make_response(jsonify(response), 200)
#         return res
#     else:
#         response = {
#             "message": "JSON received",
#         }

#         res = make_response(jsonify(response), 400)
#         return res


# @app.route("/cookies")
# def cookies():
#     res = make_response("Cookies", 200)
#     res.set_cookie("flavor", "chocolate chip2")
#     print(request.cookies.get("flavor"))
#     return res



# @app.route("/save", methods = ["GET", "POST"])
# def save():
#     if request.method == "POST":
#         req = request.form
        
#         title = req["title"]
#         author = req["author"]
#         description = req["description"]
#         quantity = req["quantity"]

#         print(title, author, description, quantity)
#         return redirect(request.url)

#     return render_template("/public/index.html")