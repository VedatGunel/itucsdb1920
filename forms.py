from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField 
from wtforms.validators import DataRequired, NumberRange, Optional, Length, EqualTo
from wtforms_components import IntegerField

from datetime import datetime


class BookEditForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    author = StringField("Author")

    year = IntegerField(
        "Year",
        validators=[
            Optional(),
            NumberRange(min=0, max=datetime.now().year),
        ],
    )
    genre = StringField("Genre")
    pageNumber = IntegerField("Number of Pages")



class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=20)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6, max=32)])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])