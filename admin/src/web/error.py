"""
Este módulo define cómo se comportara la aplicación en base a los errores encontrados.
"""
from flask import render_template, g


def not_found_error(e):
    kwargs = {
        "error_name": "404",
        "error_description": "La URL a la que quiere acceder no fue encontrada."
    }

    return render_template("error.html", **kwargs), 404


def unauthorized(e):
    kwargs = {
        "error_name": "401 Unauthorized",
        "error_description": "Debe estar logueado para acceder."
    }

    return render_template("error.html", **kwargs), 401


def forbidden(e):
    kwargs = {
        "error_name": "403 Forbidden",
        "error_description": "El contenido no puede ser mostrado porque no posee los permisos."
    }

    return render_template("error.html", **kwargs), 403


def site_under_maintenance(e):
    error_description = g.configuration.maintenance_message or "El sitio se encuentra bajo mantenimiento."

    kwargs = {
        "error_name": "503",
        "error_description": error_description
    }

    return render_template("error.html", **kwargs), 503
