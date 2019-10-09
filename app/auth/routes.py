from app.auth import bp
from .forms import LoginForm, RegistrationForm
from flask import render_template, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user
from app.models import User
from app import db

# Login Form
@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main/index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None and not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth/login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('main/index'))
    return render_template('auth/login.html', title='Login in', form=form)


# Registration Form
@bp.route('/register')
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main/index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Successfully created user account')
        return redirect(url_for('main/login'))
    return render_template('auth/login.html', title='Login in', form=form)

# Log out
@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main/index'))