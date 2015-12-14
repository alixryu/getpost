from flask import Blueprint, render_template, session, redirect, flash


wizards_blueprint = Blueprint('wizards', __name__, url_prefix='/students')


@wizards_blueprint.route('/')
@wizards_blueprint.route('/view/')
def wizards_index():
    return render_template('wizards.html')

@wizards_blueprint.route('/me/', methods={'GET'})
def wizards_user_view():
    if 'logged_in' not in session:
        flash('You must be logged in to view that page', 'error')
        return redirect('/', 303)
    if session['role'] != 'student':
        flash('You must be a student to view that page', 'error')
        return redirect('/', 303)
    
    return render_template('transfigure.html')

@wizards_blueprint.route('/edit/me/', methods={'POST'})
def wizards_user_edit():
    if 'logged_in' not in session:
        flash('You must be logged in to perform that action', 'error')
        return redirect('/', 303)
    return redirect('/view/me/', 307)
