"""
Controller de `Auth`.
"""
import secrets
from werkzeug.security import check_password_hash
from flask import Blueprint, jsonify, request, render_template, flash, redirect, url_for, session, current_app
from flask_mail import Message
from src.core.forms.institution import ChangeInstitutionForm
from src.core.forms.auth import LoginForm, PasswordForm, RegisterForm
from src.core.models.user import User
from src.core.models.institution import Institution
from src.web.helpers.auth import login_required


auth_blueprint = Blueprint("auth", __name__)


@auth_blueprint.get("/login")
def login():
    form = LoginForm()

    google_client_id = current_app.config["GOOGLE_CLIENT_ID"]
    return render_template("auth/login.html", form=form, google_client_id=google_client_id)


@auth_blueprint.post("/authenticate")
def authenticate():
    params = request.form

    user = User.find_by(email=params["email"])

    if user:
        if user.active:
            if user.password in ["", None]:
                flash("Usted se registro mediante google, inicie sesion con esa opcion", "danger")
                return redirect(url_for("auth.login"))

            if check_password_hash(user.password, params["password"]):
                session.clear()
                session["user_id"] = user.id
                flash("Iniciaste sesión correctamente!", "success")

                return redirect(url_for("home"))

        else:
            flash("Usuario inhabilitado.", "danger")
            return redirect(url_for("auth.login"))

    flash("Email o password incorrectos.", "danger")
    return redirect(url_for("auth.login"))


@auth_blueprint.get("/logout")
def logout():
    if session.get("user_id"):
        session.clear()
        flash("Cerraste sesión exitosamente!", "success")

    return redirect(url_for("auth.login"))


@auth_blueprint.get("/register")
def registerForm():
    form = RegisterForm()

    return render_template("auth/register.html", form=form)


@auth_blueprint.post("/register")
def register():
    params = request.form

    if "email" not in params or params["email"] == "":
        flash("El email no puede estar vacío o ser nulo", "danger")
        return redirect(url_for("auth.register"))

    if "firstName" not in params or params["firstName"] == "":
        flash("El nombre no puede estar vacío o ser nulo", "danger")
        return redirect(url_for("auth.register"))

    if "lastName" not in params or params["lastName"] == "":
        flash("El apellido no puede estar vacío o ser nulo", "danger")
        return redirect(url_for("auth.register"))

    user = User.find_by(email=params["email"])

    if user:
        flash("El email ya se encuentra registrado", "danger")
        return redirect(url_for("auth.register"))

    url_completa = request.url
    mail = current_app.extensions['mail']
    random_key = __generate_register_key()
    msg = Message('Registro en CIDEPINT', sender=current_app.config.get("MAIL_USERNAME"), recipients=[params["email"]])
    msg.body = 'Para generar su password ingrese al siguiente link \n \n' + url_completa + '/' + random_key
    mail.send(msg)

    User.create(
        email=params["email"],
        firstname=params["firstName"],
        lastname=params["lastName"],
        random_key=random_key,
        active=False
    )

    flash("Para continuar su registro, siga las instrucciones que le enviamos al mail "+params["email"], "success")
    return redirect(url_for("auth.login"))


@auth_blueprint.get("/register/<string:random_key>")
def changePasswordForm(random_key):
    form = PasswordForm()
    return render_template("auth/uniqueRegisterLink.html",form=form, random_key=random_key)


@auth_blueprint.post("/register/<string:random_key>")
def changePassword(random_key):
    params = request.form

    if "email" not in params or params["email"] == "":
        flash("El email no puede estar vacio o ser nulo", "danger")
        return redirect(url_for("auth.register") + '/' + random_key)

    if "password" not in params or params["password"] == "" or "password2" not in params or params["password2"] == "":
        flash("Ambos campos de la contraseña no deben estar vacíos", "danger")
        return redirect(url_for("auth.register") + '/' + random_key)

    if params["password2"] != params["password"]:
        flash("Las contraseñas no coinciden", "danger")
        return redirect(url_for("auth.register") + '/' + random_key)

    user = User.find_by(email=params["email"])

    if not user:
        flash("No se ha encontrado un usuario bajo el email que ingresó", "danger")
        return redirect(url_for("auth.register") + '/' + random_key)

    if user.random_key != random_key:
        flash("Usted no tiene permitido cambiar la contraseña de otro usuario", "danger")
        return redirect(url_for("auth.register") + '/' + random_key)

    if user.password is not None:
        flash("Usted ya no puede cambiar su contraseña por este medio", "danger")
        return redirect(url_for("auth.register") + '/' + random_key)

    mail = current_app.extensions['mail']

    msg = Message('Registro exitoso en CIDEPINT', sender=current_app.config.get("MAIL_USERNAME"), recipients=[params["email"]])
    msg.body = 'Felicitaciones se ha registrado correctamente!. \n \n Su información es \n\n Usuario: ' + params["email"] + '\n Contraseña: ' + params["password"]
    mail.send(msg)

    User.update_password(user, params["password"])

    flash("Se ha registrado correctamente, para ingresar inicie sesión", "success")
    return redirect(url_for("auth.login"))


@login_required
@auth_blueprint.post("/global/update")
def change_current_institution_variable_in_global():
    institution_id = request.form["selected_institution"]
    form = ChangeInstitutionForm()
    if form.validate_on_submit():
        institution = Institution.find_by(id=institution_id)
        if institution:
            session["current_institution"] = institution
        else:
            session.pop("current_institution", None)
            session.pop("current_role", None)
            session.pop("current_permissions", None)
            session.modified = True
        return redirect(url_for("home"))


def __generate_register_key():
    """
    Genera un token único seguro.
    """
    return secrets.token_hex(16)

@auth_blueprint.post("/login-google")
def login_google():
    oauth = current_app.extensions['oauth']
    redirect_uri = url_for('auth.auth_google', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)


@auth_blueprint.get('/login/callback')
def auth_google():

    oauth = current_app.extensions['oauth']
    token = oauth.google.authorize_access_token()
    userinfo = token.get('userinfo')
    user = User.find_by(email=userinfo['email'])
    if not user:
        user = User.create(
            email=userinfo["email"],
            firstname=userinfo["given_name"],
            lastname=userinfo["family_name"],
            active=True
        )
    if not user.active:
        flash("Esta cuenta está inhabilitada, hable con la administración", "error")
        return redirect("/")
    session["user_id"] = user.id
    return redirect("/")
