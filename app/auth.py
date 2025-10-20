from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required
from .models import User, get_db
from werkzeug.security import check_password_hash


auth_bp = Blueprint('auth', __name__, template_folder='templates')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
if request.method == 'POST':
username = request.form['username']
password = request.form['password']
user = User.get_by_username(username)
if user and user.check_password(password):
login_user(user)
return redirect(url_for('main.index'))
flash('Usuário ou senha inválidos')
return render_template('login.html')


@auth_bp.route('/logout')
@login_required
def logout():
logout_user()
return redirect(url_for('auth.login'))