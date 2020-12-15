import pyotp
from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from werkzeug.utils import secure_filename
from wtforms import StringField, IntegerField, SubmitField, TextAreaField, PasswordField
from wtforms.validators import (
    InputRequired,
    DataRequired,
    NumberRange,
    Length,
    Email,
    EqualTo,
    ValidationError,
    Regexp
)

from .models import User, Product


class SearchForm(FlaskForm):
    search_query = StringField(
        "Query", validators=[InputRequired(), Length(min=1, max=100)]
    )
    submit = SubmitField("Search")


class ProductReviewForm(FlaskForm):
    text = TextAreaField(
        "Comment", validators=[InputRequired(), Length(min=5, max=500)]
    )
    submit = SubmitField("Enter Comment")


class RegistrationForm(FlaskForm):
    username = StringField(
        "Username", validators=[InputRequired(), Length(min=1, max=40)]
    )
    email = StringField("Email", validators=[InputRequired(), Email()])
    password = PasswordField("Password", validators=[InputRequired(),
                                                     Regexp(r'([A-Za-z]+\d+)', message="Field must be AlphaNumeric"),
                                                     Length(min=8, max=32)]
                             )

    confirm_password = PasswordField(
        "Confirm Password", validators=[InputRequired(), EqualTo("password")]
    )
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        user = User.objects(username=username.data).first()
        if user is not None:
            raise ValidationError("Username is taken")

    def validate_email(self, email):
        user = User.objects(email=email.data).first()
        if user is not None:
            raise ValidationError("Email is taken")


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    token = StringField('Token', validators=[InputRequired(), Length(min=6, max=6)])

    submit = SubmitField("Login")
    '''
    def validate_token(self, token):
        user = User.query.filter_by(username=self.username.data).first()
        if user is not None:
            tok_verified = pyotp.TOTP(user.otp_secret).verify(token.data)
            if not tok_verified:
                raise ValidationError("Invalid Token")
                '''



class UpdateUsernameForm(FlaskForm):
    username = StringField(
        "Username", validators=[InputRequired(), Length(min=1, max=40)]
    )
    submit = SubmitField("Update Username")

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.objects(username=username.data).first()
            if user is not None:
                raise ValidationError("That username is already taken")


class ProductSell(FlaskForm):
    # seller = StringField("Seller", validators=[InputRequired(), Length(min=1, max=40)])
    product_name = StringField("Product Name", validators=[InputRequired(), Length(min=3, max=100)])
    price = IntegerField("Price", validators=[InputRequired(),
                                              NumberRange(min=0, max=9999, message='Must be between 1 and 9999')])
    submit = SubmitField("Sell")

    def validate_product_name(self, product_name):
        name = Product.objects(product_name=product_name.data).first()
        if name is not None:
            raise ValidationError("Product name is taken")


class ProductBuy(FlaskForm):
    submit = SubmitField("Buy")


class AddCartForm(FlaskForm):
    submit = SubmitField("Add to Cart")



