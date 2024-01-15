"""
Este módulo contiene helpers utilizados en los controllers.
"""
from functools import wraps
from flask import g, session, abort
from src.core.models.role_has_permission import RolePermission


def is_authenticated(session):
    """
    Retorna `True` si el usuario se encuentra logeado.
    Caso contrario, retorna `False`.
    """
    return session.get("user_id") is not None


def login_required(view):
    """
    Decorador que indica que la accion del controller requiere estar logueado.
    """
    @wraps(view)
    def wrapped_view(*args,**kwargs):
        if not is_authenticated(session):
            return abort(401)

        return view(*args,**kwargs)

    return wrapped_view


def check_permission(required_permission_list):
    """
    Decorador que indica que la accion del controller requiere tener permisos.
    """
    def decorator(view):
        @wraps(view)
        def wrapped_view(*args, **kwargs):
            if not RolePermission.has_permission(g.current_role, required_permission_list):
                return abort(403)

            return view(*args, **kwargs)

        return wrapped_view

    return decorator
