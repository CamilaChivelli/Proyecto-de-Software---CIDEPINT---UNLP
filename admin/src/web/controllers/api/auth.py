"""
API Controller para `Auth`.
"""
import secrets
from flask import Blueprint, current_app, jsonify, request, make_response, url_for
from flask_jwt_extended import create_access_token, set_access_cookies, unset_jwt_cookies
from src.core.models.user import User
from werkzeug.security import check_password_hash
from flask_mail import Message

api_auth_blueprint = Blueprint("auth_api", __name__, url_prefix="/api/auth")

@api_auth_blueprint.post("/")
def authenticate():
    params = request.get_json()

    if not "email" in params or not "password" in params:
        return {"error": "Correo electrónico y contraseña son necesarios"}, 400

    email = params.get("email")
    password = params.get("password")

    user = User.find_by(email=email, active=True)

    if user is None:
        return jsonify(result="Esta cuenta no existe o esta inhabilitada"), 400

    if user.password is None:
        return jsonify(result="Usted se registró mediante google, inicie sesión desde allí"), 400
    can_authenticate = user and password and check_password_hash(user.password, password)

    if can_authenticate:
        access_token = create_access_token(identity=user.id)

        response = make_response('Autenticación exitosa')
        set_access_cookies(response, access_token)

        return response, 200
    else:
        return jsonify(result="Email y password no concuerda con un usuario del sistema"), 400

@api_auth_blueprint.post("/register")
def register():
    params = request.get_json()

    if "email" not in params or params["email"] == "":
        return jsonify(result="El email no debe estar vacio o ser nulo"), 400

    if "firstname" not in params or params["firstname"] == "":
        return jsonify(result="El nombre no debe estar vacio o ser nulo"), 400

    if "lastname" not in params or params["lastname"] == "":
        return jsonify(result="El apellido no debe estar vacio o ser nulo"), 400

    user = User.find_by(email=params["email"])

    if user:
        return jsonify(result="El email ya se encuentra registrado"), 400

    url_completa = request.args.get('currentUrl')
    mail = current_app.extensions['mail']
    random_key = __generate_register_key()
    msg = Message('Registro en CIDEPINT', sender=current_app.config.get("MAIL_USERNAME"), recipients=[params["email"]])
    msg.body = 'Para generar su password ingrese al siguiente link \n \n' + url_completa + '/' + random_key
    mail.send(msg)

    User.create(
        email=params["email"],
        firstname=params["firstname"],
        lastname=params["lastname"],
        random_key=random_key,
        active=False
    )

    return jsonify(result="El usuario se creó exitosamente"), 201

@api_auth_blueprint.post("/register/<string:random_key>")
def changePassword(random_key):
    params = request.get_json()

    if "email" not in params or params["email"] == "":
        return jsonify(result="El email no debe estar vacio o ser nulo"), 400

    if "password" not in params or params["password"] == "" or "password2" not in params or params["password2"] == "":
        return jsonify(result="Ambos campos de la contraseña no deben estar vacios o ser nulos"), 400

    if params["password2"] != params["password"]:
        return jsonify(result="Las contraseñas no coinciden"), 400

    user = User.find_by(email=params["email"])

    if not user:
        return jsonify(result="No se encontró un usuario bajo el email ingresado"), 400

    if user.random_key != random_key:
        return jsonify(result="No puede cambiar la contraseña de otro usuario"), 400

    if user.password is not None:
        return jsonify(result="Ya no puede cambiar la contraseña por este medio"), 400

    mail = current_app.extensions['mail']

    msg = Message('Registro exitoso en CIDEPINT', sender=current_app.config.get("MAIL_USERNAME"), recipients=[params["email"]])
    msg.body = 'Felicitaciones se ha registrado correctamente!. \n \n Su información es \n\n Usuario: ' + params["email"] + '\n Contraseña: ' + params["password"]
    mail.send(msg)

    User.update_password(user, params["password"])

    return jsonify(result="Se cambió la contraseña exitosamente"), 200

def __generate_register_key():
    """
    Genera un token único seguro.
    """
    return secrets.token_hex(16)

@api_auth_blueprint.post("/login-google")
def login_google():
    params = request.get_json()
    user = User.find_by(email=params['email'])
    if not user:
        user = User.create(
            email=params["email"],
            firstname=params["firstname"],
            lastname=params["lastname"],
            active=True
        )
    if not user.active:
        return jsonify(result="Esta cuenta está inhabilitada, hable con la administracion"), 400
    access_token = create_access_token(identity=user.id)
    response = make_response('Autenticación exitosa')
    set_access_cookies(response, access_token)
    return response, 200

@api_auth_blueprint.get('/logout')
def logout():
    response = jsonify()
    unset_jwt_cookies(response)
    return response, 200