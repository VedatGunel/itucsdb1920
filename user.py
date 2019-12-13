from flask import current_app
from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, username, email, password, id=None, profile_picture=None, gender=None, is_admin=False):
        self.username = username
        self.email = email
        self.password = password
        self.active = True
        self.is_admin = False
        self.id = id
        self.profile_picture = profile_picture
        self.gender = gender
        self.is_admin = is_admin

    def get_id(self):
        return self.id

    @property
    def is_active(self):
        return self.active


def get_user(user_id):
    db = current_app.config["db"]
    user_ = db.get_user_by_id(user_id)
    if user_ is not None:
        user_.is_admin = db.check_admin(user_id)
    return user_