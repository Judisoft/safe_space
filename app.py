from flask import Flask

app = Flask(__name__)

@app.route("/", methods=['GET'])
def index():
    """ Returns application's Hompage"""
    return "Homepage"

@app.route('/register', methods=['GET'])
def register_form():

    """ Displays applications's registration form """

    return "Registration Form"

@app.route('/login', methods=['GET'])
def login_form():

    """ Displays applications's registration form """

    return "Login Form"


@app.route('/dashboard', methods=['GET'])
def dashboard():

    """ Displays user's dashboard """

    return "Dashboard"

if __name__ == "__main__":

    app.run(debug=True)