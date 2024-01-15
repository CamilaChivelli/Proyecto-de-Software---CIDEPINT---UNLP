"""
El servidor esta configurado para buscar la funcion `create_app()` aquí.
"""
from flask import Flask, render_template
from flask_jwt_extended import JWTManager
from flask_session import Session
from src.web import error, routes
from src.web.config import configs
from src.core import database, seeds
from flask_mail import Mail
from flask_cors import CORS
from authlib.integrations.flask_client import OAuth
from flask_wtf.csrf import CSRFProtect


sess = Session()
csrf = CSRFProtect()


def create_app(env="development", static_folder="../../static"):
    app = Flask(__name__, static_folder=static_folder)
    mail = Mail(app)
    jwt = JWTManager(app)
    app.config.from_object(configs[env])

    mail.init_app(app)
    sess.init_app(app)
    jwt.init_app(app)
    database.init_app(app)
    database.config_db(app)
    routes.register(app)

    # OAuth
    CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
    oauth = OAuth(app)
    oauth.register(
        name='google',
        server_metadata_url=CONF_URL,
        client_kwargs={
        'scope': 'openid email profile'
        }
    )

    # CSRF
    csrf.init_app(app)
    csrf.exempt(app.blueprints['auth_api'])
    csrf.exempt(app.blueprints['api_me_requests'])

    cors = CORS(app, supports_credentials=True)

    app.extensions['oauth'] = oauth

    # Comandos
    @app.cli.command(name="reset_db")
    def reset_db():
        database.reset_db()

    @app.cli.command(name="seed_db")
    def seed_db():
        seeds.run()

    # Errores
    app.register_error_handler(404, error.not_found_error)
    app.register_error_handler(401, error.unauthorized)
    app.register_error_handler(403, error.forbidden)
    app.register_error_handler(503, error.site_under_maintenance)

    # Rutas
    @app.get("/")
    def home():
        return render_template("home.html")

    return app
