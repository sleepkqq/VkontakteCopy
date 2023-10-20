from app import db
from app.auth import login_manager
from flask_bcrypt import Bcrypt
from flask_login import UserMixin
import random
import string

bcrypt = Bcrypt()


def save_edit():
    db.session.commit()


class Item:
    def save(self):
        db.session.add(self)
        db.session.commit()

    def remove(self):
        db.session.delete(self)
        db.session.commit()


class User(Item, db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    second_name = db.Column(db.String(30), nullable=False)
    phone_number = db.Column(db.String(13), unique=True, nullable=False)
    status = db.Column(db.String(100))
    password = db.Column(db.String(128), nullable=False)
    authenticated = db.Column(db.Boolean, default=False)
    active = db.Column(db.Boolean, default=True)

    images = db.relationship('Image', backref='user', lazy=True)

    def __init__(self, phone_number, first_name, second_name):
        while True:
            username = ''.join(random.choice(string.ascii_letters) for _ in range(10))
            user = User.query.filter_by(username=username).first()
            if not user:
                break
        self.username = username
        self.phone_number = phone_number
        self.first_name = first_name
        self.second_name = second_name

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)


class Image(db.Model, Item):
    id = db.Column(db.Integer, primary_key=True)
    photo_id = db.Column(db.String(15), nullable=False)
    url = db.Column(db.String(128), nullable=False)
    name = db.Column(db.String(40), nullable=False)
    username = db.Column(db.String(25), db.ForeignKey('user.username'), nullable=False)

    def __init__(self, photo_id, url, username, name):
        self.photo_id = photo_id
        self.url = url
        self.username = username
        self.name = name


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
