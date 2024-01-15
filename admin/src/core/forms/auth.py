"""
Formularios de `Institution`.
"""
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField
from wtforms.validators import DataRequired, ValidationError

from src.core.models.user import User

def validate_email_uniqueness(form, field):
    """
    Levanta un `ValidationError` si la página web ya se encuentra en uso.
    """
    user = User.find_by(web=field.data)

    if user:
        raise ValidationError("El email ya se encuentra registrado")


class LoginForm(FlaskForm):
    """
    Formulario utilizado para la creación del institution.
    """
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])

class RegisterForm(FlaskForm):
    """
    Formulario utilizado para la edición de la institución.
    """
    firstName = StringField("Nombre", validators=[DataRequired()])
    lastName = StringField("Apellido", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), validate_email_uniqueness])


class PasswordForm(FlaskForm):
    """
    Formulario utilizado para la edición de la institución.
    """
    email = StringField("Email", validators=[DataRequired(), validate_email_uniqueness])
    password = PasswordField("Password", validators=[DataRequired()])
    password2 = PasswordField("Repetir Password", validators=[DataRequired()])
