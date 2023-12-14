from flask import Blueprint,render_template, request, flash, redirect, url_for, session
from .models import Client
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    cart = session.get('cart', [])
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = Client.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Вхід пройшов успішно', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Некоректні дані, спробуйте ще раз', category='error')
        else:
            flash('Некоректні дані, спробуйте ще раз', category='error')

    return render_template("login.html", user=current_user, cart=cart)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    cart = session.get('cart', [])
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        sur_name = request.form.get('surName')
        user_contact = request.form.get('usercontact')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = Client.query.filter_by(email=email).first()
        if user:
            flash('Електронна пошта вже існує.', 'error')
        elif len(email) < 4:
            flash('Електронна пошта повинна бути довша ніж 3 символи.', 'error')
        elif len(first_name) < 2:
            flash('Ім\'я має бути довше ніж 1 символ.', 'error')
        elif len(sur_name) < 2:
            flash('Прізвище має бути довше ніж 1 символ.', 'error')
        elif len(user_contact) != 10 and user_contact.isdigit():
            flash('Номер телефону введено неправильно.', 'error')
        elif password1 != password2:
            flash('Паролі не співпадають.', 'error')
        elif len(password1) < 7:
            flash('Пароль має бути мінімум 7 символів.', 'error')
        else:
            new_user = Client(email=email, first_name=first_name, password=generate_password_hash(password1, method='pbkdf2:sha256'), last_name=sur_name, phone_number=user_contact)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Аккаунт створено', category='success')
            return redirect(url_for('views.home'))
    return render_template("sign_up.html", user=current_user, cart=cart)
