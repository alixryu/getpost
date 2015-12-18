from copy import deepcopy

from flask import Blueprint, render_template, redirect, request, flash, session as user_session

from .prefects import login_required, roles_required, roles_or_match_required, form_require
from .transfigure import view_user, edit_user
from getpost.orm import Session, ManagedSession
from getpost.models import Account, Student, Employee, Administrator

from re import fullmatch


headmaster_blueprint = Blueprint(
    'headmaster',
    __name__,
    url_prefix='/admin'
)

READ_ONLY = {
    'administrator': ()
}

READ_WRITE = {
    'administrator': ('verified', 'first_name', 'last_name', 'email_address')
}

INPUT_FIELDS = {
    'first_name': {
        'type': 'text',
        'title': 'First Name',
        'pattern': "[a-zA-Z '-]+"
    },
    'last_name': {
        'type': 'text',
        'title': 'Last Name',
        'pattern': "[a-zA-Z '-]+"
    },
    'email_address': {
        'type': 'email',
        'title': 'Email Address',
        'pattern': r'.+@.+\..+'
    },
    'verified': {
        'type': 'checkbox',
        'title': 'Verified'
    }
}

def get_read_only(id):
    if id == user_session['id'] and 'match' in READ_ONLY:
        return READ_ONLY['match']
    else:
        return READ_ONLY.get(user_session['role'], [])

def get_read_write(id):
    if id == user_session['id'] and 'match' in READ_WRITE:
        return READ_WRITE['match']
    else:
        return READ_WRITE.get(user_session['role'], [])


@headmaster_blueprint.route('/')
@login_required()
@roles_required({'administrator'})
def headmaster_index():
    return render_template('headmaster.html')

@headmaster_blueprint.route('/viewall/')
@login_required()
@roles_required({'administrator'})
def headmaster_all():
    return render_template('headmaster.html')

@headmaster_blueprint.route('/addaccount/')
@login_required()
@roles_required({'administrator'})
def headmaster_add_get():
    return render_template('letter.html')

@headmaster_blueprint.route('/addaccount/', methods={'POST'})
@login_required()
@roles_required({'administrator'})
@form_require({'role', 'email', 'fname', 'lname'})
def headmaster_add_post():
    role = request.form.get('role', None)
    if role == 'student':
        return add_student(request.form)
    elif role == 'employee':
        return add_employee(request.form)
    elif role == 'admin':
        return add_admin(request.form)
    else:
        flash("Bad role name: {}".format(role), 'error')
        return render_template('letter.html')

def validate_input(key, value):
    match = None
    if key in {'first_name', 'last_name'}:
        match = fullmatch("([a-zA-Z '-]+)", value)
    elif key == 'alternative_name':
        match = fullmatch("([a-zA-Z '-]*)", value)
    elif key == 'email_address':
        match = fullmatch('([a-zA-Z0-9]+@oberlin.edu)', value)
    elif key == 'ocmr':
        match = fullmatch('([0-9]{1,4})', value)
    elif key == 't_number':
        match = fullmatch('T?([0-9]{8})', value)
    if match is not None:
        return ''.join(match.groups())
    else:
        return None

@form_require({'tnum', 'ocmr'})
def add_student(form):
    first_name = validate_input('first_name', form['fname'])
    alternative_name = validate_input('alternative_name', form.get('aname', ''))
    last_name = validate_input('last_name', form['lname'])
    email_address = validate_input('email_address', form['email'])
    ocmr = validate_input('ocmr', form['ocmr'])
    t_number = validate_input('t_number', form['tnum'])
    if all((
        first_name, alternative_name is not None, last_name,
        email_address, ocmr, t_number
    )):
        with ManagedSession(Session, True) as db_session:
            account = Account(
                email_address=email_address,
                password=None,
                role='student',
                verified=False
            )
            db_session.add(account)
            db_session.flush()
            id = account.id
            student = Student(
                id=id,
                first_name=first_name,
                alternative_name=alternative_name,
                last_name=last_name,
                ocmr=ocmr,
                t_number=t_number
            )
            db_session.add(student)
            flash('Account created successfully!', 'success')
            return redirect("/students/{}/".format(id), 303)
    else:
        flash('Unable to create new account', 'error')

def add_employee(form):
    first_name = validate_input('first_name', form['fname'])
    last_name = validate_input('last_name', form['lname'])
    email_address = validate_input('email_address', form['email'])
    if all((first_name, last_name, email_address)):
        with ManagedSession(Session, True) as db_session:
            account = Account(
                email_address=email_address,
                password=None,
                role='employee',
                verified=False
            )
            db_session.add(account)
            db_session.flush()
            id = account.id
            employee = Employee(
                id=id,
                first_name=first_name,
                last_name=last_name,
            )
            db_session.add(employee)
            flash('Account created successfully!', 'success')
            return redirect("/employees/{}/".format(id), 303)
    else:
        flash('Unable to create new account', 'error')


def add_admin(form):
    first_name = validate_input('first_name', form['fname'])
    last_name = validate_input('last_name', form['lname'])
    email_address = validate_input('email_address', form['email'])
    if all((first_name, last_name, email_address)):
        with ManagedSession(Session, True) as db_session:
            account = Account(
                email_address=email_address,
                password=None,
                role='employee',
                verified=False
            )
            db_session.add(account)
            db_session.flush()
            id = account.id
            admin = Administrator(
                id=id,
                first_name=first_name,
                last_name=last_name,
            )
            db_session.add(admin)
            flash('Account created successfully!', 'success')
            return redirect("/admin/{}/".format(id), 303)
    else:
        flash('Unable to create new account', 'error')


@headmaster_blueprint.route('/me/')
@login_required('/auth/')
@roles_required({'administrator'})
def headmaster_self():
    return redirect("/admin/{}/".format(user_session['id']), 303)

@headmaster_blueprint.route('/<int:id>/')
@login_required()
@roles_required({'administrator'})
def headmaster_view(id):
    read, write = get_read_only(id), get_read_write(id)
    fields = deepcopy(INPUT_FIELDS)
    return view_user(id, 'administrator', read, write, fields)

@headmaster_blueprint.route('/<int:id>/edit/', methods={'POST'})
@login_required()
@roles_or_match_required({'administrator'})
def headmaster_edit(id):
    read, write = get_read_only(id), get_read_write(id)
    return edit_user(id, 'administrator', read, write, request.form, url='admin')
