from flask import render_template, request, url_for, jsonify, flash, redirect, request
from safe_space import app
from safe_space.forms import RegistrationForm, LoginForm, UrlForm
from safe_space.models import User 
from safe_space.fetch_api_data import get_mod_data
from safe_space.get_url_data import url_data
from safe_space.chunking import get_chunks
from flask_bcrypt import Bcrypt
from safe_space.models import db
from flask_login import login_user, current_user, logout_user, login_required
import schedule
import time


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
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
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
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        else:
            flash('Login Unsuccessful. Please check your email and password', 'danger')
           
    return render_template('login.html', form=form)


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():

    """ Displays user's dashboard """
    
    url = ''    
    text = ''
    mod_report = ''
    chunk = []

    if request.method == 'POST':
        url = request.form['url'] 
        text = url_data(url)

        # According to the text moderation API, text must not exceed 10,000 characters.
        # However, we don't know the number of characters that will be returned by text after scrapping
        # A walkaround will be to split the text into chunks of 9900 characters and make async requests

        # Chunk long text
        chunks = get_chunks(text, 9900)

        for chunked_text in chunks:
            chunk.append(chunked_text)
            for i in range(0, len(chunk)):
                mod_report = get_mod_data(chunk[i])
        
    # mod_report = get_mod_data(text[0:9900]) #returns the moderation report from  Texr Moderation API
    
    return render_template('dashboard.html', mod_report=mod_report,text=text)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/profile')
@login_required
def profile():
    return "User Profile"

