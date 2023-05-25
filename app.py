from flask import Flask, render_template, request, url_for, jsonify
from get_url_data import url_data
from fetch_api_data import get_mod_data
from forms import RegistrationForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '9812c2e42fc2ba86735a694f8f7ee714'

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

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET'])
def login():

    """ Handles user login """

    form = LoginForm()

    return render_template('login.html', form=form)


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():

    """ Displays user's dashboard """
    text = url_data('param') # param is the API endpoint 

    mod_report = get_mod_data(text)

    return render_template('dashboard.html', mod_report=mod_report)

if __name__ == "__main__":

    app.run(debug=True)