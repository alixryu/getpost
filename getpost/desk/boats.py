from flask import Blueprint, render_template, redirect, request,  flash
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from getpost.models import Account, Student
from getpost.orm import Session, ManagedSession
from .prefects import logout_required, form_require


boats_blueprint = Blueprint('boats', __name__, url_prefix='/signup')

SALT_ROUNDS = 12


@logout_required()
@boats_blueprint.route('/', methods={'GET', 'POST'})
def boats_index():
    return render_template('boats.html')


@logout_required()
@form_require({'email', 'password', 'tnum'}, methods={'POST'})
@boats_blueprint.route('/new/', methods={'GET', 'POST'})
def boats_new():
    email, tnum, password = request.form['email'], request.form['tnum'], request.form['password']
    if tnum[0] == 'T':
        tnum = tnum[1:]
    try:
        with ManagedSession(Session, True) as db_session:
            account = db_session.query(Account).filter(Account.email_address == email).one()
            if account.verified:
                flash('An account for {} has already been created'.format(email), 'error')
            if account.role != 'student':
                flash('The email {} does not appear to be associated with a student'.format(email), 'error')
            if len(password) < 6:
                flash('Password too short', 'error')
            if not account.verified and account.role == 'student' and len(password) >= 6:
                student = db_session.query(Student).get(account.id)
                if student:
                    account.set_password(password)
                    account.verified = True
                    account.log_in()
                    flash('Your account was created succesfully!', 'success')
                    return redirect('/', 303)
                else:
                    flash('Although your email was verified successfully, we could not find a record of it belonging to a student', 'error')
    except NoResultFound:
        flash('We could not verify the email {}'.format(email), 'error')
    except MultipleResultsFound:
        flash('We found multiple account records for the email {}'.format(email), 'error')
    except Exception:
        flash('An unaccounted-for error occurred', 'error')
    return redirect('/signup/', 307)
