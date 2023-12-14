from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_required, current_user
from website.models import Product


views = Blueprint('views', __name__)
categ = "Всі меблі"

@views.route('/', methods=['GET', 'POST'])
def home():
    if categ == "Всі меблі":
        products = Product.query.all()
    else:
        products = Product.query.filter_by(category=categ).all()

    if request.method == 'POST':
        product_id = int(request.form.get('add-to-cart'))
        product = next((p for p in products if p.id == product_id), None)

        if product:
            cart = session.get('cart', [])
            for item in cart:
                if product_id == item.get('id'):
                    if item['cnt'] < item['quantity']:  # Перевірка, чи кількість товару не перевищує quantity
                        item['cnt'] = item.get('cnt', 0) + 1
                        flash(f'{product.description} додано в корзину', 'success')
                    else:
                        flash('Максимальна кількість досягнута для цього товару', 'error')
                    break
            else:
                cart.append({'cnt': 1, **product.to_dict()})
                session['cart'] = cart
                flash(f'{product.description} додано в корзину', 'success')
        else:
            flash('Товар не знайдено', 'error')

    cart = session.get('cart', [])

    return render_template("home.html", user=current_user, products=products, categ = categ, cart=cart)

@views.route('/update_category', methods=['POST'])
def update_category():
    global categ
    categ = request.form.get('category', categ)
    return redirect(url_for('views.home'))


@views.route('/remove_from_cart/<int:product_id>', methods=['POST'])
def remove_from_cart(product_id):
    if 'cart' in session:
        cart = session['cart']

        for item in cart:
            if item.get('id') == product_id:
                item['cnt'] = max(0, item.get('cnt', 0) - 1)

                if item['cnt'] == 0:
                    cart.remove(item)

                session['cart'] = cart
                flash('Товар видалено з корзини', 'success')
                break
    else:
        flash('Корзина пуста', 'error')

    return redirect(url_for('views.home'))