from flask import Blueprint, render_template, request, session, url_for, redirect, g
from service import default_service


default_blueprint = Blueprint('/', __name__)


@default_blueprint.before_request
def before_request():
    g.user = None
    if 'user' in session:
        g.user = session['user']


@default_blueprint.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@default_blueprint.route('/account', methods=['GET', 'POST'])
def account():
    if request.method == 'GET':
        return render_template('create_account_form.html')
    elif request.method == 'POST':
        if request.form is not None:
            if request.form.get('password_0') == request.form.get('password_1'):
                success_status: int = default_service.create_new_user(
                    username=request.form.get('username'),
                    plaintext_password=request.form.get('password_0'),
                    email=request.form.get('email')
                )
                if success_status == 0:
                    return render_template('sign_in_form.html')
                elif success_status == 1:
                    return "Username Already Exists"
                elif success_status == 2:
                    return "Email Already Exists"
            else:
                # TODO: return an error for invalid matching password
                return "Passwords Do Not Match"
        else:
            # TODO: return an error for no form data
            return "No Form Data"


@default_blueprint.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    if request.method == 'GET':
        return render_template('sign_in_form.html')
    elif request.method == 'POST':
        session.pop('user', None)
        if request.form is not None:
            if request.form.get('username') is not None:
                if request.form.get('password') is not None:
                    authentication_status: int = default_service.authenticate_existing_user(
                        username=request.form.get('username'),
                        password_to_challenge=request.form.get('password')
                    )
                    if authentication_status == 0:
                        session['user'] = request.form.get('username')
                        return redirect(url_for('assets.assets'))
                    elif authentication_status == 1 or authentication_status == 2:
                        return redirect(url_for('.sign_in'))
                else:
                    # TODO: return an error for invalid matching password
                    return "Password Not Provided"
            else:
                # TODO: return an error for invalid matching password
                return "Username Not Provided"
        else:
            # TODO: return an error for no form data
            return "No Form Data"


@default_blueprint.route('/logout', methods=['POST'])
def logout():
    session.pop('user', None)
    return redirect(url_for('/.index'))
