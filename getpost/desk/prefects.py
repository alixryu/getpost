from flask import abort, redirect, flash, request, session as user_session

from functools import wraps

from re import fullmatch

validation_matches = {
    'first_name': "([a-zA-Z '-]+)",
    'last_name': "([a-zA-Z '-]+)",
    'alternative_name': "([a-zA-Z '-]*)",
    't_number': 'T?([0-9]{8})',
    'email_address': r'(.+@.+\..+)',
    'password': '(.{6,})'
}

validation_messages = {
    'first_name': 'First name may only contain letters, spaces, apostrophes, and hyphens',
    'last_name': 'Last name may only contain letters, spaces, apostrophes, and hyphens',
    'alternative_name': 'Alternative name may only contain letters, spaces, apostrophes, and hyphens',
    't_number': 'T number must contain exactly eight letters, optionally preceded by a capital "T"',
    'email_address': 'Invalid email address',
    'password': 'Passwords must be at least six characters long'
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

# Determine whether or the current user is logged in.
def is_logged_in():
    return 'id' in user_session

# Make sure the user is not logged in.
def logout_required(url='/'):
    def intermediary(func):
        @wraps(func)
        def result(*args, **kwargs):
            if not is_logged_in():
                return func(*args, **kwargs)
            else:
                return redirect(url, 303)
        return result
    return intermediary

# Make sure the user is logged in.
def login_required(url=None):
    def intermediary(func):
        @wraps(func)
        def result(*args, **kwargs):
            if is_logged_in():
                return func(*args, **kwargs)
            else:
                return permission_failure(url)
        return result
    return intermediary

# Make sure the user's session contains the given fields.
def user_session_require(required_fields, notify=True, wipe=True, url=None):
    def intermediary(func):
        @wraps(func)
        def result(*args, **kwargs):
            provided_fields = set(user_session)
            if required_fields <= provided_fields:
                return func(*args, **kwargs)
            else:
                if wipe:
                    user_session.clear()
                if notify:
                    missing_fields = required_fields - provided_fields
                    flash('The following required session parameteres were missing: {}. Please try logging in again.'.format(', '.join(missing_fields)), 'error')
                if url is None:
                    return redirect('/auth/')
                else:
                    return redirect(url, 303)
        return result
    return intermediary

# Make sure a submitted form contains the given fields.
def form_require(required_fields, methods={'GET', 'POST'}, notify=True, wipe=True, url='/'):
    methods = {method.upper() for method in methods}
    def intermediary(func):
        @wraps(func)
        def result(*args, **kwargs):
            provided_fields = set()
            if 'GET' in methods:
                provided_fields.update(set(request.args))
            if 'POST' in methods:
                provided_fields.update(set(request.form))
            if required_fields <= provided_fields:
                return func(*args, **kwargs)
            else:
                if wipe:
                    user_session.clear()
                if notify:
                    missing_fields = required_fields - provided_fields
                    flash('The following required form parameteres were missing: {}.'.format(', '.join(missing_fields)), 'error')
                return redirect(url, 303)
        return result
    return intermediary

# Make sure the user has one of the specified roles.
def roles_required(roles, url=None):
    def intermediary(func):
        @wraps(func)
        def result(*args, **kwargs):
            if user_session['role'] in roles:
                return func(*args, **kwargs)
            else:
                return permission_failure(url)
        return result
    return intermediary

# Make sure the user has the requested id.
def match_id(url=None):
    def intermediary(func):
        @wraps(func)
        def result(*args, **kwargs):
            if kwargs['id'] == user_session['id']:
                return func(*args, **kwargs)
            else:
                return permission_failure(url)
        return result
    return intermediary

# Make sure the user has one of the specified roles, or matches the requested id.
def roles_or_match_required(roles, url=None):
    def intermediary(func):
        @wraps(func)
        def result(*args, **kwargs):
            if kwargs['id'] == user_session['id'] or user_session['role'] in roles:
                return func(*args, **kwargs)
            else:
                return permission_failure(url)
        return result
    return intermediary

def permission_failure(url=None):
    if url is None:
        abort(403)
    else:
        return redirect(url, 303)
