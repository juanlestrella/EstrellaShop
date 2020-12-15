from flask import Blueprint, render_template, url_for, redirect, request, flash
from flask_login import current_user

from ..forms import SearchForm, ProductReviewForm, ProductSell, AddCartForm, ProductBuy
from ..models import User, Review, Product
from ..utils import current_time

products = Blueprint("products", __name__)

""" ************ View functions ************ """


@products.route("/", methods=["GET", "POST"])
def index():
    form = SearchForm()

    if form.validate_on_submit():
        return redirect(url_for("products.query_results", query=form.search_query.data))

    return render_template("index.html", form=form)


@products.route("/search-results/<query>", methods=["GET"])
def query_results(query):
    form = SearchForm()
    #formcart = AddCartForm()

    if form.validate_on_submit():
        product = Product.objects(product_name=form.product_name.data).any()

        if product is not None:
            '''
            if formcart.validate_on_submit() and current_user.is_authenticated:
                cart = Cart(
                    buyer=current_user._get_current_object(),
                    product_name=
                    price=
                )
                cart.save()
            '''
            return render_template("query.html", product=product)  # , form=formcart
        else:
            return redirect(url_for("products.index"))
    #else:
        #return redirect(url_for("products.index"))

    product = Product.objects(product_name=query)

    return render_template("query.html", product=product)


@products.route("/products/<product_name>", methods=["GET", "POST"])
def product_detail(product_name):
    try:
        product = Product.objects(product_name=product_name).first()  # not sure if this works
    except ValueError:
        return redirect(url_for("users.login"))

    form = ProductReviewForm()
    if form.validate_on_submit() and current_user.is_authenticated:
        review = Review(
            commenter=current_user._get_current_object(),
            content=form.text.data,
            product_name=product_name,  # might not work
            date=current_time(),
        )
        review.save()

        return redirect(request.path)

    bform = AddCartForm()
    if bform.validate_on_submit() and current_user.is_authenticated:
        product.buyer = current_user._get_current_object()
        product.save()
        return redirect(url_for("products.user_buy", username=current_user.username))

    reviews = Review.objects(product_name=product_name)  # not sure if this works
    return render_template(
        "product_detail.html", form=form, product=product, reviews=reviews, bform=bform
    )


#I might replace this with user_sell and user_buy
@products.route("/user/<username>")
def user_detail(username):
    user = User.objects(username=username).first()
    reviews = Review.objects(commenter=user)

    return render_template("user_detail.html", username=username, reviews=reviews)


@products.route("/user/sale/<username>", methods=["GET", "POST"])
def user_sell(username):
    user = User.objects(username=username).first()  # finds the username in User db

    form = ProductSell()  # call ProductSell from forms.py
    if form.validate_on_submit() and current_user.is_authenticated:  # check if submit and user is true
        product = Product(  # create the product
            seller=current_user._get_current_object(),
            seller_name=username,
            product_name=form.product_name.data,
            price=form.price.data,
            #buyer=None
        )
        product.save()  # save the product in db
        return redirect(request.path)  # return back to page

    all_products = Product.objects(seller=user)  # get all the products sold by user

    return render_template("sell_product.html", username=username, all_products=all_products, form=form)


@products.route("/user/cart/<username>", methods=["GET", "POST"])
def user_buy(username):
    user = User.objects(username=username).first()  # finds the username in User db

    form = ProductBuy()  # call ProductSell from forms.py
    #if form.validate_on_submit() and current_user.is_authenticated:  # check if submit and user is true
        #delete the products in the cart
    #    return redirect(request.path)  # return back to page

    all_products = Product.objects(buyer=user)  # get all the products sold by user

    return render_template("buy_product.html", username=username, all_products=all_products, form=form)
