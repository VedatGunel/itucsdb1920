from datetime import datetime
from passlib.hash import pbkdf2_sha256 as hasher

from flask import abort, current_app, render_template, request, redirect, url_for, flash
from book import Book
from forms import BookEditForm, LoginForm, RegistrationForm, ReviewForm, ProfileEditForm, SearchForm
from user import User
from review import Review
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.utils import secure_filename
import os

def home_page():
    searchform=SearchForm()
    today = datetime.today()
    day_name = today.strftime("%A")
    return render_template("home.html", day=day_name, searchform=searchform)

def books_page():
    searchform=SearchForm()
    db = current_app.config["db"]
    books = db.get_books()
    return render_template("books.html", books=books, searchform=searchform)

def book_page(book_id):
    searchform=SearchForm()
    db = current_app.config["db"]
    book = db.get_book(book_id)
    reviews, user_ids = db.get_reviews(book_id)
    if book is None:
        abort(404)
    form = ReviewForm()
    if form.validate_on_submit():
        score = form.data["score"]
        comment = form.data["comment"]
        author = db.get_user_id(current_user.username)
        review = Review(author=author, book=book_id, score=score, comment=comment)
        review_id = db.add_review(review)
        review.id = review_id
        return redirect(url_for("book_page", book_id = book_id))
    return render_template("book.html", book=book, form=form, reviews=reviews, user_ids=user_ids, searchform=searchform)
	
@login_required
def book_add_page():
    searchform=SearchForm()
    if not current_user.is_admin:
        abort(401)
    form = BookEditForm()
    if form.validate_on_submit():
        title = form.data["title"]
        author = form.data["author"]
        year = form.data["year"]
        genre = form.data["genre"]
        pageNumber = form.data["pageNumber"]
        cover = form.data["cover"]
        book = Book(title=title, author=author, year=year, genre=genre, pageNumber=pageNumber, cover=cover)
        db = current_app.config["db"]
        book_id = db.add_book(book)
        return redirect(url_for("book_page", book_id=book_id))
    return render_template("book_edit.html", form=form, searchform=searchform)
	
@login_required
def book_edit_page(book_id):
    searchform=SearchForm()
    if not current_user.is_admin:
        abort(401)
    db = current_app.config["db"]
    book = db.get_book(book_id)
    if book is None:
        abort(404)
    form = BookEditForm()
    if form.validate_on_submit():
        title = form.data["title"]
        author = form.data["author"]
        year = form.data["year"]
        genre = form.data["genre"]
        pageNumber = form.data["pageNumber"]
        cover = form.data["cover"]
        book = Book(title=title, author=author, year=year, genre=genre, pageNumber=pageNumber, cover=cover)
        db.update_book(book_id, book)
        return redirect(url_for("book_page", book_id=book_id))
    form.title.data = book.title
    form.author.data = book.author if book.author else ""
    form.year.data = book.year if book.year else ""
    form.genre.data = book.genre if book.genre else ""
    form.pageNumber.data = book.pageNumber if book.pageNumber else ""
    form.cover.data = book.cover if book.cover else ""
    return render_template("book_edit.html", form=form, searchform=searchform)

def registration_page():
    searchform = SearchForm()
    db = current_app.config["db"]
    form = RegistrationForm()
    if(current_user.is_authenticated):
        return redirect(url_for("home_page"))
    if form.validate_on_submit():
        username = form.data["username"]
        email = form.data["email"]
        user = db.get_user_by_username(username)
        profile_picture = form.data["profile_picture"]
        if user is None:
            user = db.get_user_by_email(email)
            if user is None:
                password = hasher.hash(form.data["password"])
                filename = None
                if profile_picture:
                    filename = secure_filename(profile_picture.filename)
                    _, f_ext = os.path.splitext(filename)
                    filename = username + f_ext
                    profile_picture.save(os.path.join(
                    current_app.root_path, 'static/profile_pictures', filename
                    ))
                user = User(username, email=email, password=password, profile_picture=filename)
                db.add_user(user)
                user = db.get_user_by_username(username)
                login_user(user)
                flash("Registration successful.")
                next_page = request.args.get("next", url_for("home_page"))
                return redirect(next_page)
            flash("E-mail is already in use.")
            return render_template("register.html", form=form, searchform=searchform)
        flash("Username already exists.")
    return render_template("register.html", form=form, edit_profile=False, searchform=searchform)
    	
def login_page():
    searchform=SearchForm()
    db = current_app.config["db"]
    form = LoginForm()
    if(current_user.is_authenticated):
        return redirect(url_for("home_page"))
    if form.validate_on_submit():
        username = form.data["username"]
        user = db.get_user_by_username(username)
        remember = form.data["remember"]
        if user is not None:
            password = form.data["password"]
            if hasher.verify(password, user.password):
                login_user(user, remember=remember)
                flash("You have logged in.")
                next_page = request.args.get("next", url_for("home_page"))
                return redirect(next_page)
        flash("Invalid credentials.")
    return render_template("login.html", form=form, searchform=searchform)

@login_required
def logout_page():
    logout_user()
    flash("You have logged out.")
    return redirect(url_for("home_page"))

@login_required
def delete_review(review_id):
    db = current_app.config["db"]
    review_ = db.get_review(review_id)
    if review_ is None:
        abort(404)
    if current_user.id == review_.author or current_user.is_admin:
        db.delete_review(review_id)
    else:
        abort(401)
    return redirect(url_for("book_page", book_id=review_.book))

@login_required
def delete_book(book_id):
    db = current_app.config["db"]
    book = db.get_book_by_id(book_id)
    if book is None:
        abort(404)
    if current_user.is_admin:
        db.delete_book(int(book_id))
        flash("Book deleted successfully.")
    else:
        flash("You don't have permission to delete the book.")
    return redirect(url_for("books_page"))

def profile_page(user_id):
    searchform=SearchForm()
    db = current_app.config["db"]
    user = db.get_user_by_id(user_id)
    reviews, book_names = db.get_reviews_by_user(user.id)
    return render_template("profile.html", user=user, reviews=reviews, books=book_names, user_id=user_id, searchform=searchform)

@login_required
def profile_edit_page(user_id):
    searchform=SearchForm()
    db = current_app.config["db"]
    user = db.get_user_by_id(user_id)
    if user is None:
        abort(404)
    if not current_user.id == user_id:
        abort(401)
    form = ProfileEditForm()
    if form.validate_on_submit():
        username = form.data["username"]
        email = form.data["email"]
        password = None
        if form.data["old_password"]:
            password = hasher.hash(form.data["new_password"])
        profile_picture = form.data["profile_picture"]
        filename = None
        if profile_picture:
            filename = secure_filename(profile_picture.filename)
            _, f_ext = os.path.splitext(filename)
            filename = username + f_ext
            profile_picture.save(os.path.join(
            current_app.root_path, 'static/profile_pictures', filename
            ))
        new_user = User(username=username, email=email, password=password, profile_picture=filename)
        if (form.data["old_password"] and hasher.verify(form.data["old_password"], user.password)) or (not form.data["old_password"] and not form.data["new_password"]):
            db.update_user(user_id, new_user)
            flash("User information updated successfully.")
            return redirect(url_for("profile_page", user_id=user_id))
        else:
            flash("Old password is wrong.")
    form.username.data = user.username
    form.email.data = user.email
    return render_template("register.html", form=form, edit_profile=True, searchform=searchform)

@login_required
def delete_profile(user_id):
    db = current_app.config["db"]
    user = db.get_user_by_id(user_id)
    if user is None:
        abort(404)
    if current_user.is_admin or current_user.id == user_id:
        logout_user()
        db.delete_user(int(user_id))
        flash("User deleted successfully.")
    else:
        abort(401)
    return redirect(url_for("home_page"))

@login_required
def review_edit_page(review_id):
    searchform=SearchForm()
    db = current_app.config["db"]
    review = db.get_review(review_id)
    if review is None:
        abort(404)
    if not current_user.id == review.author:
        abort(401)
    form = ReviewForm()
    if form.validate_on_submit():
        score = form.data["score"]
        comment = form.data["comment"]
        author = review.author
        book_id = review.book
        review_id = review.id
        review_ = Review(score=score, comment=comment, author=author, book=book_id, id=review_id)
        db.update_review(review_)
        flash("Review updated successfully.")
        return redirect(url_for("book_page", book_id=book_id))
    form.score.data = str(review.score)
    form.comment.data = review.comment
    return render_template("review_edit.html", form=form, searchform=searchform)
    
def search_page():
    db = current_app.config["db"]
    form = SearchForm()
    print(form.query.data)
    books = db.get_books(request.args.get("query"))
    return render_template("books.html", books=books, searchform=form, search_page=True)