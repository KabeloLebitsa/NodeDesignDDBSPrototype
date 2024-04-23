#app.py

import database
from flask import Flask, redirect, render_template, request, url_for, jsonify, flash
from flask_login import LoginManager, login_required, login_user, logout_user, current_user 
from config import app_config 

# Application configuration
app = Flask(__name__)
app.config.from_object(app_config)

# Flask-Login configuration
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Home page route
@app.route('/')
def index():
    return render_template('index.html')
# Display patients page route
@app.route('/displaypatients')
@login_required
def display_patients():
    return render_template('display_patients.html')
# Create patients page route
@login_required
@app.route('/createpatient')
def create_patient():
    return render_template('create_patient.html')

# Dashboard route
@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

# User info route
@app.route('/userinfo', methods=['GET'])
@login_required
def get_user_info():
  """
  This function retrieves the currently logged-in user's information.
  """
  return jsonify({'User': {'Username': current_user.Username, 'Role': current_user.Role}})

# User loader function for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return database.load_user(user_id)

# Login page route
@app.route('/loginpage')
def login_page():
    return render_template('login.html')

# Login route
@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return render_template('dashboard.html')  # Redirect to dashboard if already logged in

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = database.authenticate_user(username, password)
        if not user:
            flash('Invalid username or password')
            return redirect(url_for('login'))

        login_user(user)
        return redirect(url_for('dashboard'))  # Redirect to dashboard after successful login

    return render_template('login.html')

# Logout route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# Main function
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
