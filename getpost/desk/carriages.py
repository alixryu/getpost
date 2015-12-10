from flask import Blueprint, render_template, session, redirect, request

from bcrypt import hashpw, gensalt

from getpost.models import Account
from getpost.orm import Session



carriages_blueprint = Blueprint('carriages', __name__, url_prefix='/auth')


@carriages_blueprint.route('/')
def carriages_index():
    return render_template('carriages.html')

@carriages_blueprint.route('/in', methods={'POST'})
def carriages_in():
    if {'email', 'password'} <= set(request.form):
        return validate_login(request.form)
    return redirect('/auth', 303)

def validate_login(form):
    email, password = form['email'], form['password']
    account_rows = Session.query(Account.password).filter(Account.email_address == email)
    if account_rows.count() == 1:
        account = account_rows.first()
        if account.password == hashpw(bytes(password, 'ASCII'), account.password):
            session['logged_in'] = True
            return redirect('/', 303)
    return redirect('/auth', 303)

@carriages_blueprint.route('/out')
def carriages_out():
    session.pop('logged_in', None)
    return redirect('/', 303)
