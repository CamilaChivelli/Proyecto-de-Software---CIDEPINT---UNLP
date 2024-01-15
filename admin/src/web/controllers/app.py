"""
Controller de `App`.
"""
from flask import Blueprint, session, g, abort
from src.core.forms.institution import ChangeInstitutionForm
from src.web.helpers.auth import login_required
from src.core.models.user import User
from src.core.models.user_has_role import UserRoleInstitution
from src.core.models.institution import Institution
from src.core.models.role_has_permission import RolePermission
from src.core.models.configuration import Configuration

app_blueprint = Blueprint("app", __name__)


@login_required
@app_blueprint.before_app_request
def setup():
    """
    Carga las variables globales necesarias antes de cada request.
    """
    g.form = ChangeInstitutionForm()

    g.current_user = __load_logged_in_user()

    if g.current_user:
        g.user_rows_in_userInstitutionRole = __load_info_from_userInstitutionRole()

        if "current_institution" in session:
            g.current_institution = session["current_institution"]
        else:
            if "current_institution" not in session:
                institution_id = (
                    g.user_rows_in_userInstitutionRole[0].institution.id
                    if g.user_rows_in_userInstitutionRole and
                    g.user_rows_in_userInstitutionRole[0] and
                    g.user_rows_in_userInstitutionRole[0].institution
                    else None
                )

                if institution_id is not None:
                    session["current_institution"] = Institution.find_by(id=institution_id)
                    g.current_institution = session["current_institution"]

        g.current_role = __load_current_role()
        g.current_permissions = __load_current_permissions()

    g.configuration = __load_configuration()

    __block_access_if_site_is_on_maintenance()

    return None


def __block_access_if_site_is_on_maintenance():
    """
    Bloquea el acceso del usuario a la web redireccionandolo con un código de estado HTTP 503.
    """
    if g.configuration.is_on_maintenance and (g.get("current_role") and not g.current_role.is_super_administrador()):
        return abort(503)


def __load_logged_in_user():
    """
    Busca al usuario logeado en la DB según el `user_id` de la session.
    """
    return User.find_by(id=session.get("user_id"), active=True)


def __load_info_from_userInstitutionRole():
    """
    Retorna las tuplas de UserInstitutionRole donde aparezca el usuario actual
    """
    return UserRoleInstitution.get_user_institution_role_by_user(g.current_user)


def __load_current_role():
    """
    Retorna el `rol` del `current_user` en base a la `current_institution`.
    """
    if "current_institution" in session:
        institution = session["current_institution"]
        return UserRoleInstitution.get_role(g.current_user, institution.id)

    else:
        return UserRoleInstitution.get_role(g.current_user, None)


def __load_current_permissions():
    """
    Retorna una lista con los `permissions` que tiene el `current_user` en base al `role` que tiene para la `current_institution`.
    """
    return RolePermission.list_available_permissions(g.current_role)


def __load_configuration():
    """
    Retorna la `configuration` del sistema.
    """
    return Configuration.query.first()
