from flask import Flask, render_template, redirect, url_for, flash, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_migrate import Migrate
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# User table
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    # One-to-Many relationships for 'classes' and 'to-dos'
    classes = db.relationship('Class', backref='user', lazy=True)
    todos = db.relationship('ToDo', backref='user', lazy=True)

# Class table
class Class(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# To-Do table
class ToDo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', name='fk_todo_user'), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('class.id', name='fk_todo_class'), nullable=False)
 # Link to the Class table

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/', methods=['GET'])
def home():
    if 'user_id' in session:
        user_id = session['user_id']
        user = User.query.get(user_id)

        # Fetch user's classes
        classes = Class.query.filter_by(user_id=user_id).all()
        return render_template('home.html', user=user, classes=classes)

    return render_template('home.html', user=None)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the username already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists. Please choose a different one.', 'danger')
            return redirect(url_for('signup'))

        # Hash the password
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Save the new user
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('Sign-up successful! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the user exists
        user = User.query.filter_by(username=username).first()

        # Validate credentials
        if user and bcrypt.check_password_hash(user.password, password):
            session['user_id'] = user.id  # Store user ID in the session
            session['username'] = user.username  # Optional: Store username
            flash('Login successful!', 'success')
            return redirect(url_for('home'))  # Redirect to home page
        else:
            flash('Invalid username or password.', 'danger')
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    # Fetch user from the session
    user_id = session.get('user_id')
    user = User.query.get(user_id)

    if not user:
        flash('User not found. Please log in again.', 'danger')
        return redirect(url_for('login'))

    # Fetch classes and to-dos for the current user
    classes = Class.query.filter_by(user_id=user.id).all()
    todos = ToDo.query.filter_by(user_id=user.id).all()

    return render_template('dashboard.html', user=user, classes=classes, todos=todos)

@app.route('/add_class', methods=['POST'])
def add_class():
    if 'user_id' not in session:
        flash('You must be logged in to add a class.', 'danger')
        return redirect(url_for('login'))

    class_name = request.form.get('class_name')
    if class_name:
        new_class = Class(title=class_name, user_id=session['user_id'])
        db.session.add(new_class)
        db.session.commit()
        flash('Class added successfully!', 'success')
    else:
        flash('Class name cannot be empty.', 'danger')

    return redirect(url_for('home'))

@app.route('/class/<int:class_id>', methods=['GET', 'POST'])
def class_page(class_id):
    if 'user_id' not in session:
        flash('You must be logged in to view this page.', 'danger')
        return redirect(url_for('login'))

    # Fetch class and validate ownership
    user_id = session['user_id']
    cls = Class.query.filter_by(id=class_id, user_id=user_id).first()
    if not cls:
        flash('Class not found or unauthorized access.', 'danger')
        return redirect(url_for('home'))

    if request.method == 'POST':
        # Adding a new to-do item
        description = request.form.get('description')
        if description:
            new_todo = ToDo(description=description, user_id=user_id, class_id=class_id)
            db.session.add(new_todo)
            db.session.commit()
            flash('To-Do item added successfully!', 'success')
            return redirect(url_for('class_page', class_id=class_id))
        else:
            flash('To-Do description cannot be empty.', 'danger')

    # Fetch to-do items for this class
    todos = ToDo.query.filter_by(class_id=class_id).all()
    return render_template('class_page.html', cls=cls, todos=todos)

@app.route('/add_todo/<int:class_id>', methods=['POST'])
def add_todo(class_id):
    if 'user_id' not in session:
        flash('You must be logged in to add a to-do item.', 'danger')
        return redirect(url_for('login'))

    user_id = session['user_id']
    description = request.form.get('description')

    if description:
        # Add the to-do item to the database
        new_todo = ToDo(description=description, user_id=user_id, class_id=class_id)
        db.session.add(new_todo)
        db.session.commit()
        flash('To-Do item added successfully!', 'success')
    else:
        flash('Description cannot be empty.', 'danger')

    return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Ensure tables are created
    app.run(debug=True)
