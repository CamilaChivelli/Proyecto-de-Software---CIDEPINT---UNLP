"""
Formularios de usuarios.
"""
from flask_wtf import FlaskForm
from wtforms import EmailField, StringField, PasswordField, BooleanField, SelectField
from wtforms.validators import DataRequired, Email, ValidationError, Length
from src.core.models.user import User


def validate_email_uniqueness(form, field):
    """
    Levanta un `ValidationError` si el email ya se encuentra en uso.
    """
    user = User.find_by(email=field.data)

    if user:
        raise ValidationError("Email inválido.")


def validate_password_confirmation(form, field):
    """
    Levanta un `ValidationError` si las passwords no coinciden.
    """
    if field.data != form.data["password"]:
        raise ValidationError("Las passwords no coinciden.")


class NewUserForm(FlaskForm):
    """
    Formulario utilizado para la creación del User.
    """
    email = EmailField("Email", validators=[DataRequired(), Email(), validate_email_uniqueness])
    firstname = StringField("Nombre")
    lastname = StringField("Apellido")
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8, max=16)])
    password_confirmation = PasswordField("Confirmar password", validators=[DataRequired(), validate_password_confirmation])
    active = BooleanField("Activo")


class EditUserForm(FlaskForm):
    """
    Formulario utilizado para la edición del User.
    """
    email = EmailField("Email")
    firstname = StringField("Nombre")
    lastname = StringField("Apellido")
    active = BooleanField("Activo")


class SearchUserForm(FlaskForm):
    """
    Formulario utilizado para la búsqueda de Users.
    """
    email = StringField("Email")
    active = SelectField("Activo", choices=[("none", "Todos los estados"), ("true", "Activo"), ("false", "Bloqueado")])
