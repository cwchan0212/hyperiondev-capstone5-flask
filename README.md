## Capstone Project 5 - Bookstore Management (Flask)
:arrow_right: Preview

### Introduction

This application is a web-based bookstore management system that allows the user to manage the store's inventory by adding, updating, deleting, and searching for books in the database. It was adapted from my previous capstone project and converted into a web application using the Flask framework and SQLite. Additionally, REST API has been added to the web portal to demonstrate the use of REST API.

<p align="center"><img src="capstone_project/assets/images/02.png" width="600"><br>
<i>5.1 The overview of Bookstore Management System </i></p>

### Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

###  Prerequisites

- **Python** 3.10 or later
- **Flask** 2.2.0 or later
- Additional packages: Flask-Bcrypt, PyJWT, SQLAlchemy, flask-sqlalchemy, python-dotenv



#### Installation

1. **Clone** the repository 
```
git clone https://github.com/cwchan0212/hyperiondev-capstone5-flask.git
```
2. **Navigate** to the project directory and copy the files according to the following file structures. 

```
cd bookstore
```

3. Create a virtual environment in **venv** folder 
```
py -3 -m venv venv
```

4. **Activate** the environment
```
source venv/bin/activate  # for Linux/macOS
venv\Scripts\activate     # for Windows

```
> Note: Type **deactivate** to exit venv mode

5. Install **Flask**
```
pip install Flask
```

6. Install the necessary packages:
```
pip install flask-bcrypt
pip install flask-sqlalchemy
pip install PyJWT
pip install python-dotenv
pip install SQLAlchemy
```

Alternatively, the user can installs the packages on the file  requirements.txt 
```
pip install -r requirements.txt
```

7. Set environment variables in the .env and .flaskenv configuration file.

.env
```
FLASK_SECRET_KEY=yoursecretkey
```
.flaskenv
```
FLASK_APP=bookstore
FLASK_ENV=development
FLASK_DEBUG=True
FLASK_RUN_HOST=0.0.0.0
FLASK_SQLALCHEMY_DATABASE_URI=sqlite:///bookstore-dev.db
FLASK_SQLALCHEMY_TRACK_MODIFICATIONS=True
FLASK_SESSION_COOKIE_HTTPONLY=True
FLASK_REMEMBER_COOKIE_HTTPONLY=True
FLASK_SESSION_COOKIE_SAMESITE=Strict
FLASK_PERMANENT_SESSION_LIFETIME=30
FLASK_MAX_CONTENT_LENGTH=5
```

8. Start development server

Normally, the Flask server can be started by the following command:
```
flask --app appName run
```
Set the server visible externally
```
flask --app appName run --host=0.0.0.0
```
set debug mode on
```
flask --app appName --debug run  --host=0.0.0.0
```

After installed python-dotenv and configured .env and .flashenv, the user can type the following command to start the server.

```
flask run
```
Or simply use the following command to start the server:

run.py
```
from bookstore import app

if __name__ == "__main__":
    app.run(
        debug=True,
        host="0.0.0.0",
        port=3000,
    )

```

For Windows, type
```
$env:FLASK_ENV=development
$env:FLASK_APP=bookstore
python run.py
```

For Mac OS, type
```
EXPORT FLASK_ENV=development
EXPORT FLASK_APP=bookstore
python run.py
```
### File Structure
```
bookstore/
├─ templates/
│  ├─ public/
│  │  ├─ book/
│  │  │  ├─ api.html
│  │  │  ├─ base.html
│  │  │  ├─ form.html
│  │  │  ├─ index.html
├─ admin_views.py
├─ api_views.py
├─ data.py
├─ models.py
├─ views.py
├─ __init__.py
instance/
├─ bookstore-dev.db
static/
├─ css/
│  ├─ Banner-Heading-Image-images.css
│  ├─ Black-Navbar.css
│  ├─ bootstrap.min.css
│  ├─ bootstrap2.min.css
│  ├─ style.css
├─ img/
│  ├─ bg.png
├─ js/
│  ├─ bootstrap.min.js
│  ├─ clean-blog.js
│  ├─ Navbar---Apple.js
│  ├─ script.js
.env
.flaskenv
config.py
run.py
```

### Model
#### User 
The User Model has several fields
- user_id as primary key
- user_username 
- user_password
- user_created_date
- user_updated_date

#### Book
The Book Model also has several fields
- book_id as primary key
- book_uuid
- book_title
- book_author
- book_description
- book_quantity
- book_created_date
- book_updated_date

### Usage

1. Starting the development server: You can do this by running the command **flask run** in the terminal.
Opening a web browser and navigating to **http://127.0.0.1:5000/**. This will allow you to access the application on your local machine.


3. **User login system**: Having a login system in place will allow you to restrict access to certain features of the application to only logged-in users.
4. **CRUD functions** and **search queries**: Allowing users to add, modify, delete books and make search queries based on different criteria such as book title, author, description, and quantity ranges.
5. Search query for **non-logged users**: Allowing non-logged users to make search queries, but with the **exception of quantity range** as a search criteria.
6. **Restricting access to the REST API**: Limit the access to your REST API only to logged-in users to ensure that only authorised users can perform certain actions.

#### Login

The user is required to enter a **username** and **password**. If the user enters an invalid username or password, an error message will be displayed and the user will be prompted to try again.


<p align="center"><img src="capstone_project/assets/images/02.png" width="600"><br>
<i>5.2 Login screen</i></p>

> Note: The test accounts are used for testing purposes

#### Book

The logged user is allowed to add, modify, delete books and make search queries based on different criteria such as book title, author, description, and quantity ranges. Non-logged user is also allowed to make search queries but with the **exception of quantity range** as a search criteria.

<p align="center"><img src="capstone_project/assets/images/02.png" width="600"><br>
<i>5.3 Add new book in the form</i></p>

<p align="center"><img src="capstone_project/assets/images/02.png" width="600"><br>
<i>5.4 The new book is added successfully</i></p>


<p align="center"><img src="capstone_project/assets/images/02.png" width="600"><br>
<i>5.5 Update book in the form</i></p>

<p align="center"><img src="capstone_project/assets/images/02.png" width="600"><br>
<i>5.6 The book is updated successfully. </i></p>

<p align="center"><img src="capstone_project/assets/images/02.png" width="600"><br>
<i>5.7 Click the delete button to delete book</i></p>

<p align="center"><img src="capstone_project/assets/images/02.png" width="600"><br>
<i>5.8 Search book by title, author, description and quantity range </i></p>

<p align="center"><img src="capstone_project/assets/images/02.png" width="600"><br>
<i>5.9 The user is required to enter the minimum quantity and maximum quantity as quantity is the search criteria. </i></p>

<p align="center"><img src="capstone_project/assets/images/02.png" width="600"><br>
<i>5.10 The quantity is not shown to the non-logged user. </i></p>


#### REST API
The logged user is allowed to use REST API to add, update, delete book as well make queries. The output will be displayed in JSON format.

<p align="center"><img src="capstone_project/assets/images/02.png" width="600"><br>
<i>5.11 Click Get all books to get the records of all book </i></p>


<p align="center"><img src="capstone_project/assets/images/02.png" width="600"><br>
<i>5.12 The output is shown in the JSON format for <b>Get all</b></i></p>

> Note: For testing purpose, one book of the books will be passed to next sections for **Get 1**, **Update 1** and **Delete 1** respectively. 

<p align="center"><img src="capstone_project/assets/images/02.png" width="600"><br>
<i>5.13 Click <b>Get 1</b> to get the record of 1 book</i></p>

<p align="center"><img src="capstone_project/assets/images/02.png" width="600"><br>
<i>5.14 The output is shown in the JSON format for <b>Get 1</b></i></p>

<p align="center"><img src="capstone_project/assets/images/02.png" width="600"><br>
<i>5.15 Click <b>Add 1</b> to add the new book</i></p>

<p align="center"><img src="capstone_project/assets/images/02.png" width="600"><br>
<i>5.16 The output is shown in the JSON format for <b>Add 1</b></i></p>

<p align="center"><img src="capstone_project/assets/images/02.png" width="600"><br>
<i>5.17 Click <b>Update 1</b> to update the book</i></p>

<p align="center"><img src="capstone_project/assets/images/02.png" width="600"><br>
<i>5.18 The output is shown in the JSON format for <b>Update 1</b></i></p>

<p align="center"><img src="capstone_project/assets/images/02.png" width="600"><br>
<i>5.19 Click <b>Delete 1</b> to delete the book</i></p>

<p align="center"><img src="capstone_project/assets/images/02.png" width="600"><br>
<i>5.20 The output is shown in the JSON format for <b>Delete 1 </b></i></p>

### Acknowledgments
This project was inspired by <a href="https://www.hyperiondev.com" target="_blank">HyperionDev</a>.