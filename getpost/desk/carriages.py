from flask import Blueprint, render_template, session, redirect, request, flash
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from getpost.models import Account
from getpost.orm import Session


carriages_blueprint = Blueprint('carriages', __name__, url_prefix='/auth')


@carriages_blueprint.route('/', methods={'GET', 'POST'})
def carriages_index():
    if 'logged_in' in session:
        return redirect('/', 303)
    return render_template('carriages.html')

@carriages_blueprint.route('/in/', methods={'GET', 'POST'})
def carriages_in():
    if 'logged_in' in session:
        return redirect('/', 303)
    required_params = {'email', 'password'}
    provided_params = set(request.form)
    if required_params <= provided_params:
        return validate_login(request.form)
    else:
        missing_params = required_params - provided_params
        flash('The following parameters were missing: {}'.format(', '.join(missing_params)))
    return redirect('/auth/', 307)

def validate_login(form):
    email, password = form['email'], form['password']
    try:
        account = Session.query(Account).filter(Account.email_address == email).one()
        if not account.verified:
            flash('This account is not yet verified', 'error')
        elif not account.check_password(password):
            flash('Invalid email/password combination', 'error')
        else:
            account.log_in()
            flash('Login successful!', 'success')
            return redirect('/', 303)
    except NoResultFound:
        flash('Invalid email/password combination', 'error')
    except MultipleResultsFound:
        flash('We found multiple account records for the email {}'.format(email), 'error')
    except Exception:
        flash('An unaccounted-for error occurred', 'error')
    return redirect('/auth/', 307)

@carriages_blueprint.route('/out/')
def carriages_out():
    if 'logged_in' in session:
        if 'id' in session:
            account = Session.query(Account).get(session['id'])
            if account:
                account.log_out()
                flash('Logout successful!', 'success')
            else:
                session.clear()
        else:
            session.clear()
    return redirect('/', 303)
