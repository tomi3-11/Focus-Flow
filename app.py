from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_required, login_user, logout_user, current_user, UserMixin, LoginManager
from werkzeug.security import generate_password_hash, check_password_hash


# instances of the flask class
app = Flask(__name__)

# Database configurations
app.config['SECRET_KEY'] = 'my-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Models for the User
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password_hash = db.Column(db.String(100))
    
    # Set hashed password
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    # Check hashed password
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    

# Loading user
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Views
# Home Page
@app.route('/')
def home():
    return render_template('home.html')

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False
        
        user = User.query.filter_by(username=username).first()
        
        if not user or not user.check_password(password):
            flash("Please check your login details and try again.")
            return redirect(url_for('login'))
        
        login_user(user, remember=remember)
        return redirect(url_for('profile'))
    
    return render_template('login.html')
        

# Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user:
            flash("Username already exists")
            return redirect(url_for('register'))
        
        new_user = User(username=username)
        new_user.set_password(password)
        
        db.session.add(new_user)
        db.session.commit()
        
        return redirect(url_for('login'))
    
    return render_template('register.html')


# profile
@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.username) 


# Logout
@app.route('/logout')
@login_required    
def logout():
    logout_user()
    return redirect(url_for('home'))


# Run the Application
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
    
