from flask import Flask, render_template, request, redirect, url_for, jsonify,make_response
import requests

app = Flask(__name__)


backend_service_name = 'backend-service'
backend_account_url = f'http://{backend_service_name}:5000'

backend_account_login_url = backend_account_url+'/login'
backend_account_register_url = backend_account_url+'/register'
@app.route('/')
@app.route('/home')
def home():
    username = request.cookies.get('username')
    return render_template('home.html',username=username)
@app.route('/userpost', methods=['GET', 'POST'])
def userpost():
    return render_template('login.html', error_message="a")
@app.route('/usersearch', methods=['GET', 'POST'])
def usersearch():
    return render_template('login.html', error_message="a")
@app.route('/login', methods=['GET', 'POST'])
def login():
    error_message = None  # Initialize error message

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Send login information to the backend for authentication
        response = requests.post(backend_account_login_url, json={'username': username, 'password': password})

        # Check the response from the backend
        if response.status_code == 200 and response.json()['status'] == 'success':
            response_object = make_response(redirect(url_for('home')))
            response_object.set_cookie('username', username)
            response_object.set_cookie('password', password)
            return response_object
        else:
            # Set the error message
            error_message = "Login failed! Please check your credentials."

    return render_template('login.html', error_message=error_message)

@app.route('/register', methods=['GET', 'POST'])
def register():
    error_message = None

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if not username or not password:
            error_message = 'Username and password are required fields.'
        else:
            response = requests.post(backend_account_register_url, json={'username': username, 'password': password})
            # Check for duplicate username or other registration errors
            if response.status_code == 200 and response.json()['status'] == 'success':
                #Successful registration
                return redirect(url_for('login'))
            else:
                error_message = 'Username already exists. Please choose a different username.'

    return  render_template('register.html', error_message=error_message)

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=False)
