from flask import Blueprint, render_template, redirect, request, session, flash
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from getpost.models import Account, Student
from getpost.orm import Session


boats_blueprint = Blueprint('boats', __name__, url_prefix='/signup')

SALT_ROUNDS = 12


@boats_blueprint.route('/', methods={'GET', 'POST'})
def boats_index():
    if 'logged_in' in session:
        return redirect('/', 303)
    return render_template('boats.html')


@boats_blueprint.route('/new/', methods={'GET', 'POST'})
def boats_new():
    if 'logged_in' in session:
        return redirect('/', 303)
    required_params = {'email', 'password', 'tnum'}
    provided_params = set(request.form)
    if required_params <= provided_params:
        return activate_student(request.form)
    else:
        missing_params = required_params - provided_params
        flash('The following parameters were missing: {}'.format(', '.join(missing_params)))
    return redirect('/signup/', 307)

def activate_student(form):
    email, tnum, password = form['email'], form['tnum'], form['password']
    try:
        account = Session.query(Account).filter(Account.email_address == email).one()
        if account.verified:
            flash('An account for {} has already been created'.format(email), 'error')
        if account.role != 'student':
            flash('The email {} does not appear to be associated with a student'.format(email), 'error')
        if not account.verified and account.role == 'student':
            student = Session.query(Student).get(account.id)
            if student:
                account.set_password(password)
                account.verified = True
                student.alternative_name = student.first_name
                Session.commit()
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
