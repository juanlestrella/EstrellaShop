import pyotp
from flask_login import UserMixin
from . import db, login_manager
from . import config
import pyopt
import base64


@login_manager.user_loader
def load_user(user_id):
    return User.objects(username=user_id).first()


class User(db.Document, UserMixin):
    username = db.StringField(required=True, unique=True)
    email = db.EmailField(required=True, unique=True)
    password = db.StringField(required=True)
    otp_secret = db.StringField(required=True, min_length=16, max_length=16, default=pyotp.random_base32())

    # Returns unique string identifying our object
    def get_id(self):
        return self.username


class Product(db.Document):
    seller = db.ReferenceField(User, required=True)
    seller_name = db.StringField(required=True, min_length=1, max_length=50)
    product_name = db.StringField(required=True, min_length=1, max_length=100)
    price = db.IntField(required=True)
    buyer = db.ReferenceField(User, required=False)
    #product_id = db.StringField(required=True)


class Review(db.Document):
    commenter = db.ReferenceField(User, required=True)
    content = db.StringField(required=True, min_length=5, max_length=500)
    date = db.StringField(required=True)
    #product_id = db.ReferenceField(Product, required=True)
    product_name = db.StringField(required=True, min_length=1, max_length=100)


class Cart(db.Document):
    buyer = db.ReferenceField(User, required=True)
    product_name = db.StringField(required=True, min_length=1, max_length=100)
    price = db.IntField(required=True)