from app import db
from app.auth import login_manager
from flask_bcrypt import Bcrypt
from flask_login import UserMixin

bcrypt = Bcrypt()


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
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    authenticated = db.Column(db.Boolean, default=False)
    active = db.Column(db.Boolean, default=True)

    likes = db.relationship('Image', backref='user', lazy=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email

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
