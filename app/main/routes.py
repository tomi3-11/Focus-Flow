# Handling the routes for the operations in our application i.e. Profile, Home
from flask import Blueprint, render_template
from flask_login import login_required, current_user

main_bp = Blueprint('main', __name__, template_folder='../templates/main')

@main_bp.route('/')
def home():
    return render_template('home.html', title='Home')

@main_bp.route('/profile')
@login_required
def profile():
    return render_template('profile.html', title='Profile', name=current_user.username)