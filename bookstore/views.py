# Views for bookstore function
from datetime import datetime
from bookstore import app
from flask import Flask, render_template, request, redirect, make_response, jsonify, flash, session, url_for
from .models import User, Book, Review
# =====================================================================================================================
# Book functions
# 
# ---------------------------------------------------------------------------------------------------------------------
# Route to Book - index page
@app.route("/book")
def book_index():
    return render_template("public/book/base.html")
# ---------------------------------------------------------------------------------------------------------------------
# Route to Contact - internal link
@app.route("/book/contact")
def book_contact():
    return redirect("/book#contact")
# ---------------------------------------------------------------------------------------------------------------------
# Route to Book - form (add/edit function)
@app.route("/book/form", methods = ["POST"]) 
def book_form():
    book_action = request.form["book_action"] if "book_action" in request.form else ""
    book_action_save = request.form["book_action_save"] if "book_action_save" in request.form else ""
    message, book_dictionary = None, {}
    # method POST: for adding/updating/deleting books
    if request.method == "POST": 
        # If book_action is "add", load the Book form
        if book_action == "add":
            # First load Book form for adding a new book
            if book_action_save == "":
                return render_template("public/book/form.html", book_action=book_action, book_dictionary=book_dictionary)
            # Submit the Book form for adding a new book
            else:
                # Get the error message and book_dictionary from the request form
                message, book_dictionary  = get_book_dictionary_message(request.form)
                # If the message exists, flash the message to the Book form page
                if message:
                    flash(message)
                    return render_template("public/book/form.html", book_dictionary=book_dictionary)
                # If no message, check for any duplicate books
                else:
                    title = book_dictionary["title"]
                    book = Book.find_title(title)
                    # If a Book exists, notify the user of the duplicate books
                    if book:
                        message =f"The <b>{title}</b> exists in our records."
                        flash(message)
                        return render_template("public/book/form.html", book_action="add", book_dictionary=book_dictionary)
                    # If no books are found, add the new book
                    else:
                        Book.add_book(**book_dictionary)
                        book_dictionary = {}
                        message =f"The <b>{title}</b> is added successfully."
                        flash(message)
                        # Return book form for adding new books
                        return render_template("public/book/form.html", book_action="add", book_dictionary={})
        # If book_action is "edit", load the Book form for editing books         
        elif book_action == "edit":
            book_id = request.form["book_id"] if "book_id" in request.form else None
            # Load Book form for editing book
            if book_action_save == "":
                book = Book.one_book(book_id)
                # Store the book list in the dictionary
                book_dictionary = {
                    "id": book.book_id,
                    "uuid": book.book_uuid,
                    "title": book.book_title,
                    "author": book.book_author,
                    "description": book.book_description,
                    "quantity": book.book_quantity,
                    "createdDate": book.book_created_date,
                    "updatedDate": book.book_updated_date
                }
                return render_template("public/book/form.html", book_action=book_action, book_dictionary=book_dictionary)
            # Submit Book form for editing book
            else:
                message, book_dictionary = get_book_dictionary_message(request.form)
                title = book_dictionary["title"]
                book = Book.find_title(title)
                # If a Book exists, notify the user of the duplicate books
                if book:
                    message =f"The <b>{title}</b> exists in our records."
                    flash(message)
                    book_dictionary["id"] = book_id
                    return render_template("public/book/form.html", book_action="edit", book_dictionary=book_dictionary)

                book_dictionary["id"] = book_id
                book = Book.update_book(**book_dictionary)
                message = f"The book <b>{book_dictionary['title']}</b> is updated successfully." 
                flash(message)
                book = Book.one_book(book_id)
                book_dictionary = Book.get_book_dictionary(book)
                return render_template("public/book/form.html", book_action=book_action, book_dictionary=book_dictionary)
        # If book_action is "remove", delete Book by book id
        elif book_action == "remove":
            search_dictionary = {}
            book_id = request.form["book_id"] if "book_id" in request.form else None
            # If book_id found, delete Book by book_id
            if book_id != "":                
                book = Book.one_book(book_id)
                title = book.book_title
                book = Book.delete_book(book_id)
                if book:                    
                    message = f"The book <b>{title}</b> is deleted successfully."
                    flash(message)
                    search_dictionary = session["search_dictionary"]
                    books = Book.book_search(search_dictionary)
                    # books = Book.all_books()
                    return render_template("public/book/index.html", books=books, search_dictionary=search_dictionary)
                else:
                    message = f"No book is found to be deleted."
                    flash(message)
                    search_dictionary = session["search_dictionary"]
                    books = Book.book_search(search_dictionary)
                    return render_template("public/book/index.html", books=books, search_dictionary=search_dictionary)
            # if book id is not found, flash message to notify the user
            else:
                message = f"No book id is found."
                print(f"[book_form]: No book id found to deleted [{book_action}]")
                flash(message)
                books = Book.all_books()
                return render_template("public/book/index.html", books=books)
        # For any other cases, load the Book index page
        else:  
            books = Book.all_books()
            return render_template("public/book/index.html", books=books)
# ---------------------------------------------------------------------------------------------------------------------
# Route to Book Search page
@app.route("/book/search", methods = ["GET", "POST"])
def book_search():
    message = ""
    search_dictionary = {}
    books = None
    # First load the Book search page
    if request.method == "GET":
        return render_template("/public/book/index.html", search_dictionary=search_dictionary)
    # Submit Book search request
    else:        
        search_dictionary = {}
        if "search_dictionary" in session:
            del session["search_dictionary"]

        for key, value in request.form.items():
            search_dictionary[key] = value.strip()            
        # If the search criteria are missing, store the flash message
        if search_dictionary["search_criteria"] != "title" and search_dictionary["search_criteria"] != "author" and search_dictionary["search_criteria"] != "description" and search_dictionary["search_criteria"] != "quantity" or search_dictionary["search_criteria"] =="Search criteria...":
            message = f"Please select <b>SEARCH CRITERIA</b>."
        # If no search criteria are missing, validate inputs
        else: 
            # Check the blank input for title/author/description
            if search_dictionary["search_criteria"] == "title" or search_dictionary["search_criteria"] == "author" or search_dictionary["search_criteria"] == "description":
                if search_dictionary["search_input"] == "":
                    message = f"Please enter <b>{search_dictionary['search_criteria'].upper()}</b>."
            # Check the inputs for quantity range 
            elif search_dictionary["search_criteria"] == "quantity":
                if search_dictionary["quantity_min"] == "":
                    message = f"The <b>MINIMUM</b> quantity must not be blank."
                elif search_dictionary["quantity_max"] == "":
                    message = f"The <b>MAXIMUM</b> quantity must not be blank."
                else:
                    if float(search_dictionary["quantity_min"]) > float(search_dictionary["quantity_max"]):
                        message = f"The <b>MINIMUM</b> quantity must not be less than the <b>MAXIMUM</b> quantity."
        # If a message exists, flash a message to notify the user
        if message:
            flash(message)
            return render_template("public/book/index.html", search_dictionary=search_dictionary)
        # If no message is stored, search Book by book criteria
        else:
            type = search_dictionary["search_criteria"] 
            search_dictionary["type"] = type       
            search_input = search_dictionary["search_input"]
            quantity_min = search_dictionary["quantity_min"]
            quantity_max  = search_dictionary["quantity_max"]
            session["search_dictionary"] = search_dictionary
            if type == "title" or type == "author" or type == "description" and search_input:                
                books = Book.book_search(search_dictionary)
            elif type == "quantity" and quantity_min and quantity_max:
                books = Book.book_search(search_dictionary)
            return render_template("public/book/index.html", search_dictionary=search_dictionary, books=books)
# ---------------------------------------------------------------------------------------------------------------------
# Function get_book_dictionary_message to convert the input book items to the dictionary (for Book from)
def get_book_dictionary_message(form_dictionary):
    book_field_list = ["title", "author", "description", "quantity"]
    book_dictionary = {}
    message = None
    # Check all inputs of the Book form
    for key, value in form_dictionary.items():
        if value.strip() == "":
            message = f"The field <b>{key.upper()}</b> cannot be blank."
            flash(message)
        else:
            if key in book_field_list:
                book_dictionary[key] = value.strip()
    # Return message and book dictionary
    return [message, book_dictionary]
#----------------------------------------------------------------------------------------------------------------------
# Create a datetime filter to convert date format for template
@app.template_filter("datetime")
def datetime(dt):

    if str(dt).find("T"):
        dt = str(dt).replace("T", " ")
        return dt
    else:
        return dt.strftime("%Y-%m-%d %H:%M:%S")
