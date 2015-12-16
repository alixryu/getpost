from flask import render_template, request, redirect, flash, abort, session as user_session

from ..models import Account
from ..orm import Session

from re import fullmatch

validation_matches = {
    'first_name': "([a-zA-Z '-]+)",
    'last_name': "([a-zA-Z '-]+)",
    'alternative_name': "([a-zA-Z '-]*)",
    't_number': 'T?([0-9]{8})',
    'email_address': r'(.+@.+\..+)',
    'password': '(.{6,})',
    'ocmr': '[0-9]{1,4}'
}

validation_messages = {
    'first_name': 'First name may only contain letters, spaces, apostrophes, and hyphens',
    'last_name': 'Last name may only contain letters, spaces, apostrophes, and hyphens',
    'alternative_name': 'Alternative name may only contain letters, spaces, apostrophes, and hyphens',
    't_number': 'T number must contain exactly eight letters, optionally preceded by a capital "T"',
    'email_address': 'Invalid email address',
    'password': 'Passwords must be at least six characters long',
    'ocmr': 'OCMR numbers must be between one and four digits'
}

# Validate data when updating, and return a sanitized version.
def validate_field(field, value, notify=True, strict=True):
    if field in validation_matches:
        match = fullmatch(validation_matches[field], value)
        if match:
            return ''.join(match.groups())
        else:
            if notify:
                flash(validation_messages[field], 'error')
            return None
    return None if strict else ''

def view_user(id, role, read, write, fields):
    db_session = Session()
    account = db_session.query(Account).get(id)
    if not (account and account.role == role):
        db_session.close()
        abort(404)
    person = account.get_person()
    if person:
        values = {}
        values.update(account.as_dict(read + write))
        values.update(person.as_dict(read + write))
        for name, value in values.items():
            if name in fields:
                if name in read and (value is None or value == ''):
                    fields[name]['value'] = 'None listed'
                elif type(value) in {str, int}:
                    fields[name]['value'] = value
                elif type(value) == bool:
                    if name == 'verified':
                        fields[name]['checked'] = value
                        fields[name]['label'] = True
        db_session.close()
        return render_template(
            'transfigure.html', action='edit/', method='POST', read=read,
            write=write, fields=fields, role=role.capitalize()
        )
    else:
        db_session.close()
        flash('Could locate corresponding ' + role + ' object in database', 'error')
        return redirect('/', 303)

def edit_user(id, role, read, write, form, url=None):
    if url is None:
        url = role + 's'
    db_session = Session()
    account = db_session.query(Account).get(id)
    if account.role != role:
        db_session.close()
        abort(404)
    person = account.get_person()
    if person:
        denied_fields = set(read)
        allowed_fields = set(write)
        requested_fields = set(request.form)
        if not denied_fields.intersection(requested_fields):
            edit_fields = {field: form[field] for field in form if field in allowed_fields}
            if not edit_fields:
                flash('No update parameters given', 'error')
            else:
                if attempt_update(account, person, edit_fields):
                    flash('Account updated successfully!', 'success')
                    db_session.commit()
                else:
                    db_session.rollback()
            db_session.close()
            return redirect("/{}/{}/".format(url, id), 303)
        else:
            db_session.close()
            flash("Cannot edit the following fields for this ' + role + ': {}".format(', ').join(denied_fields.intersection(requested_fields)), 'error')
            return redirect("/{}/{}/".format(url, id), 303)
    else:
        db_session.close()
        flash('Could locate corresponding ' + role + ' object in database', 'error')
        return redirect('/', 303)

def attempt_update(account, person, form):
    success = True
    updates = {}
    for field, value in form.items():
        validated = validate_field(field, value)
        if validated is not None:
            if field == 'email_address':
                account.email_address = validated
                updates['email_address'] = validated
            elif field == 't_number':
                if value[0] == 'T':
                    value = value[1:]
                person.t_number = validated
                updates['t_number'] = validated
            elif field == 'first_name':
                person.first_name = validated
                updates['first_name'] = validated
            elif field == 'last_name':
                person.last_name = validated
                updates['last_name'] = validated
            elif field == 'alternative_name':
                person.alternative_name = validated
                updates['alternative_name'] = validated
            else:
                flash("Cannot update {} field".format(field), 'error')
                success = False
        else:
            success = False
    if success and user_session['id'] == account.id:
        user_session.update(updates)
    return success
