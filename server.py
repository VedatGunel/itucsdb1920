from flask import Flask
from flask_login import LoginManager

import views
from database import Database
from book import Book
from user import get_user

lm = LoginManager()

@lm.user_loader
def load_user(user_id):
    return get_user(user_id)

def create_app():
    app = Flask(__name__)
    app.config.from_object("settings")
    app.add_template_global(name="zip", f=zip)

    app.add_url_rule("/", view_func=views.home_page)
    app.add_url_rule("/register", view_func=views.registration_page, methods=["GET", "POST"])
    app.add_url_rule("/login", view_func=views.login_page, methods=["GET", "POST"])
    app.add_url_rule("/logout", view_func=views.logout_page)
    app.add_url_rule("/books/", view_func=views.books_page, methods=["GET", "POST"])
    app.add_url_rule("/books/<int:book_id>", view_func=views.book_page, methods=["GET", "POST"])
    app.add_url_rule("/books/<int:book_id>/edit", view_func=views.book_edit_page, methods=["GET", "POST"])
    app.add_url_rule("/books/<int:book_id>/delete", view_func=views.delete_book, methods=["POST"])
    app.add_url_rule("/new-book", view_func=views.book_add_page, methods=["GET", "POST"])
    app.add_url_rule("/reviews/<int:review_id>/delete", view_func=views.delete_review, methods=["GET", "POST"])
    app.add_url_rule("/profile/<int:user_id>", view_func=views.profile_page)

    lm.init_app(app)
    lm.login_view = "login_page"    

    db = Database(app.config["DATABASE_URL"])
    app.config["db"] = db

    return app

if __name__ == "__main__":
    app = create_app()
    port = app.config.get("PORT", 5000)
    app.run(host="0.0.0.0", port=port)
else:
    app = create_app()

