# WEB
from src.web.controllers.app import app_blueprint
from src.web.controllers.auth import auth_blueprint
from src.web.controllers.users import user_blueprint
from src.web.controllers.institutions import institution_blueprint
from src.web.controllers.services import service_blueprint
from src.web.controllers.institution_services import institution_services_blueprint
from src.web.controllers.configurations import configuration_blueprint
from src.web.controllers.institution_users import institution_users_blueprint
from src.web.controllers.service_requests import service_requests_blueprint

# API
from src.web.controllers.api.institutions import api_institution_blueprint
from src.web.controllers.api.services import api_service_blueprint
from src.web.controllers.api.auth import api_auth_blueprint
from src.web.controllers.api.me.profiles import api_me_profile_blueprint
from src.web.controllers.api.me.service_requests import api_me_request_blueprint
from src.web.controllers.api.service_types import api_service_types_blueprint

def register(app):
    # Controllers
    app.register_blueprint(app_blueprint)
    app.register_blueprint(configuration_blueprint)
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(user_blueprint)
    app.register_blueprint(service_blueprint)
    app.register_blueprint(institution_blueprint)
    app.register_blueprint(institution_users_blueprint)
    app.register_blueprint(institution_services_blueprint)
    app.register_blueprint(service_requests_blueprint)

    # REST API
    app.register_blueprint(api_institution_blueprint)
    app.register_blueprint(api_service_blueprint)
    app.register_blueprint(api_auth_blueprint)
    app.register_blueprint(api_me_profile_blueprint)
    app.register_blueprint(api_me_request_blueprint)
    app.register_blueprint(api_service_types_blueprint)
