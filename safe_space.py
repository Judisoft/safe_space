from flask_bcrypt import Bcrypt
from datetime import datetime
from flask import Flask, render_template, request, url_for, jsonify, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from fetch_api_data import get_mod_data
from forms import RegistrationForm, LoginForm
from get_url_data import url_data

app = Flask(__name__)

app.config['SECRET_KEY'] = '9812c2e42fc2ba86735a694f8f7ee714'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///safe_space.db'

db =SQLAlchemy(app)
bcrypt = Bcrypt(app)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)
    profile_pic = db.Column(db.String(60), nullable=False, default='default.jpg')
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"User('{self.name}', '{self.email}', '{self.profile_pic}', '{self.created_at}')"

@app.route("/url", methods=['GET', 'POST'])
def get_url():
    """ Gets the url to moderated and returns the moderation report """
    url = ''
    data = ''

    if request.method == 'POST':
        url = request.form['url']
        data = url_data(url)

    return render_template('test_form.html', url=url, data=data)

@app.route("/", methods=['GET'])
def index():
    """ Returns application's Hompage"""
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():

    """ Handles user registration """

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(name=form.name.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been successfully created!', 'success') 
        return redirect(url_for('login'))

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():

    """ Handles user login """

    form = LoginForm()
    if form.validate_on_submit():
        flash(f'Welcome {form.email.data}', 'success')
        return redirect(url_for('dashboard'))
    return render_template('login.html', form=form)


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():

    """ Displays user's dashboard """
    # text = url_data('param') # param is the API endpoint 

    # mod_report = get_mod_data(text)

    return render_template('dashboard.html')

if __name__ == "__main__":

    app.run(debug=True)