#app.py

import users
from flask import Flask, redirect, render_template, request, url_for, jsonify
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from models import User  

# Application configuration
app = Flask(__name__)
app.config.from_object('config')

# Flask-Login configuration
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login.html'

@app.route('/user/info', methods=['GET'])
@login_required
def get_user_info():
  """
  This function retrieves the currently logged-in user's information.
  """
  return jsonify({'user': {'username': current_user.username, 'role': current_user.role}})

# User loader function for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('/dashboard'))
    username = request.form.get('username')
    password = request.form.get('password')
    if not username or not password:
        return 'Invalid username or password'
    # Validate username and password inputs
    if not validate_inputs(username, password):
        return 'Invalid username or password'
    try:
        if user := users.authenticate(username, password):
            login_user(user)
            return redirect(url_for('/dashboard'))
        return 'Invalid username or password'
    except Exception as e:
        return f'An error occurred: {str(e)}'

def validate_inputs(username, password):
  # Check if the username and password are not empty
  if not username or not password:
      return False

  # Check for minimum length requirements
  min_username_length = 5
  min_password_length = 8
  if len(username) < min_username_length or len(password) < min_password_length:
      return False

  # Check for password complexity (example: must contain at least one number and one uppercase letter)
  if not any(char.isdigit() for char in password):
      return False
  return any((char.isupper() for char in password))

# Logout route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# Home page route
@app.route('/')
def index():
    return render_template('index.html')

# Dashboard route
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    port = app.config.get('PORT', 5000)
    app.run(debug=False, host='127.0.0.1', port=port)
