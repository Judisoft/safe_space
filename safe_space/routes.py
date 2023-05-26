from flask import render_template, request, url_for, jsonify, flash, redirect
from safe_space import app
from safe_space.forms import RegistrationForm, LoginForm
from safe_space.models import User 
from safe_space.fetch_api_data import get_mod_data
from safe_space.get_url_data import url_data
from flask_bcrypt import Bcrypt
from safe_space.models import db
from flask_login import login_user


bcrypt = Bcrypt(app)

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
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Login Unsuccessful. Please check your email and password', 'danger')
           
    return render_template('login.html', form=form)


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():

    """ Displays user's dashboard """
    # text = url_data('param') # param is the API endpoint 

    # mod_report = get_mod_data(text)

    return render_template('dashboard.html')