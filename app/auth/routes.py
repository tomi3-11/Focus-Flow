# Routes for authentications i.e. Login, Register & Logout.
from flask import Blueprint, render_template, flash, request, redirect, url_for
from app.models import User
from app import db
from flask_login import login_user, logout_user, current_user, login_required
from app.auth.forms import LoginForm, RegisterForm


auth_bp = Blueprint('auth', __name__, template_folder='../templates/auth')

# Login
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.profile'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash('Login Successfully.', 'success')
            return redirect(url_for(next_page) if next_page else redirect(url_for('main.profile')))
        else:
            flash('Login Unsuccessfull, please enter the correct username and password!', 'danger')
    
    return render_template('login.html',title='Login', form=form)


# Register
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.profile'))
    
    form = RegisterForm()
    if form.validate_on_submit:
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Your Account was created successfully.", "success")
        
        return redirect(url_for('auth.login'))
    
    return render_template('register.html', title='Register', form=form)


# logout
@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', "info")
    return redirect(url_for('main.home'))    
    