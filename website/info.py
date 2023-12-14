from flask import Blueprint, render_template, session
from flask_login import login_required, current_user
from .models import Product
from .views import categ

info = Blueprint('info', __name__)

@info.route('/about-us')
def about_us():
    cart = session.get('cart', [])
    return render_template("about_us.html", user=current_user, cart=cart)

@info.route('/contact')
def contact():
    cart = session.get('cart', [])
    return render_template("contact.html", user=current_user,  cart=cart)

@info.route('/product/<int:product_id>')
def product(product_id):
    product = Product.query.filter_by(id=product_id).all()
    cart = session.get('cart', [])
    return render_template("product.html",product=product[0], user=current_user, cart=cart)