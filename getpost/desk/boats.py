from flask import Blueprint, render_template, redirect, request, session

from bcrypt import hashpw, gensalt

from getpost.models import Account, Student, Employee
from getpost.orm import engine, Session


boats_blueprint = Blueprint('boats', __name__, url_prefix='/signup')

SALT_ROUNDS = 12


@boats_blueprint.route('/')
def boats_index():
    return render_template('boats.html')


@boats_blueprint.route('/new', methods={'POST'})
def boats_new():
    if {'email', 'passone', 'role'} <= set(request.form):
        role = request.form['role']
        if role == 'student':
            if 'tnum' in request.form:
                return activate_student(request.form)
        elif role == 'employee':
            return add_employee(request.form)
    return redirect('/signup', 303)

def activate_student(form):
    email, tnum, password = form['email'], form['tnum'], form['passone']
    account_rows = Session.query(Account.email_address).filter(Account.email_address == email)
    if account_rows.count() == 1:
        password_hash = hashpw(bytes(password, 'ASCII'), gensalt(SALT_ROUNDS))
        account_rows.update({'password': password_hash, 'verified': True})
        Session.commit()
        session['logged_in'] = True
        return redirect('/', 303)
    return redirect('/signup', 303)

def add_employee(form):
    return redirect('/signup', 303)
