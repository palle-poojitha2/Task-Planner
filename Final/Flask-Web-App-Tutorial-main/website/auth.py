from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

def validate_user_login(email, password):
    user = User.query.filter_by(email=email).first()
    if user:
        if check_password_hash(user.password, password):
            return user
    return None

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = validate_user_login(email, password)
        if user:
            flash('Logged in successfully!', category='success')
            login_user(user, remember=True)
            return redirect(url_for('views.home'))
        else:
            flash('Incorrect email or password, try again.', category='error')

    return render_template("login.html", user=current_user)

def validate_user_registration(email, first_name, password1, password2):
    user = User.query.filter_by(email=email).first()
    if user:
        return "Email already exists."
    elif len(email) < 4:
        return "Email must be greater than 3 characters."
    elif len(first_name) < 2:
        return "First name must be greater than 1 character."
    elif password1 != password2:
        return "Passwords don't match."
    elif len(password1) < 7:
        return "Password must be at least 7 characters."
    return None

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        validation_error = validate_user_registration(email, first_name, password1, password2)
        if validation_error:
            flash(validation_error, category='error')
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(
                password1, method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
