from flask import Blueprint, render_template, redirect, request, flash, session as user_session
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from getpost.models import Account
from getpost.orm import ManagedSession
from .prefects import logout_required, form_require, login_required


carriages_blueprint = Blueprint('carriages', __name__, url_prefix='/auth')


@carriages_blueprint.route('/', methods={'GET', 'POST'})
@logout_required()
def carriages_index():
    return render_template('carriages.html')

@carriages_blueprint.route('/in/', methods={'POST'})
@logout_required()
@form_require({'email', 'password'}, methods={'POST'})
def carriages_in():
    email, password = request.form['email'], request.form['password']
    with ManagedSession(False) as db_session:
        try:
            account = db_session.query(Account).filter(Account.email_address == email).one()
            if not account.verified:
                flash('This account is not yet verified', 'error')
                return redirect('/signup/', 303)
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
@login_required('/auth/')
def carriages_out():
    with ManagedSession(False) as db_session:
        account = db_session.query(Account).get(user_session['id'])
        if account:
            account.log_out()
            flash('Logout successful!', 'success')
        else:
            user_session.clear()
        return redirect('/', 303)
