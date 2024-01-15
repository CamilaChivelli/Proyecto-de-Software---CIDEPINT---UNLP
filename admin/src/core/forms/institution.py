"""
Formularios de `Institution`.
"""
from flask_wtf import FlaskForm
from wtforms import HiddenField, StringField, BooleanField, SelectField, URLField
from wtforms.validators import DataRequired, ValidationError, URL
from src.core.models.institution import Institution


def validate_name_uniqueness(form, field):
    """
    Levanta un `ValidationError` si el nombre ya se encuentra en uso.
    """
    institution = Institution.find_by(name=field.data)

    if institution:
        raise ValidationError("Nombre ya se encuentra registrado")


def edit_validate_name_uniqueness(form, field):
    """
    Levanta un `ValidationError` si el nombre ya se encuentra en uso en la edición.
    """
    institution = Institution.find_by(name=field.data)

    if institution and institution.id != form.institution.id:
        raise ValidationError("Nombre ya se encuentra registrado")


def validate_web_uniqueness(form, field):
    """
    Levanta un `ValidationError` si la página web ya se encuentra en uso.
    """
    institution = Institution.find_by(web=field.data)

    if institution:
        raise ValidationError("Web ya se encuentra registrada")


def edit_validate_web_uniqueness(form, field):
    """
    Levanta un `ValidationError` si el nombre ya se encuentra en uso en la edición.
    """
    institution = Institution.find_by(web=field.data)

    if institution and institution.id != form.institution.id:
        raise ValidationError("Web ya se encuentra registrada")


def validate_contactInfo_uniqueness(form, field):
    """
    Levanta un `ValidationError` si la el contacto ya se encuentra en uso.
    """
    institution = Institution.find_by(contact_info=field.data)

    if institution:
        raise ValidationError("Información de contacto ya se encuentra registrada")


def edit_validate_contactInfo_uniqueness(form, field):
    """
    Levanta un `ValidationError` si el nombre ya se encuentra en uso en la edición.
    """
    institution = Institution.find_by(contact_info=field.data)

    if institution and institution.id != form.institution.id:
        raise ValidationError("Información de contacto ya se encuentra registrada")


class NewInstitutionForm(FlaskForm):
    """
    Formulario utilizado para la creación del institution.
    """
    name = StringField("Nombre", validators=[DataRequired(), validate_name_uniqueness])
    info = StringField("Info")
    address = HiddenField("Dirección")
    location = StringField("Detalles de la direccion")
    web = URLField("Web", validators=[DataRequired(), URL(), validate_web_uniqueness])
    keywords = StringField("Palabras clave")
    customer_service_hours = StringField("Días y horarios de atención")
    contact_info = StringField("Información de contacto", validators=[DataRequired(), validate_contactInfo_uniqueness])
    enable = BooleanField("Habilitado")


class EditInstitutionForm(FlaskForm):
    """
    Formulario utilizado para la edición de la institución.
    """
    name = StringField("Nombre", validators=[DataRequired(), edit_validate_name_uniqueness])
    info = StringField("Info")
    address = HiddenField("Dirección")
    location = StringField("Localizacón")
    web = URLField("Web", validators=[DataRequired(), URL(),  edit_validate_web_uniqueness])
    keywords = StringField("Palabras clave")
    customer_service_hours = StringField("Días y horarios de atención")
    contact_info = StringField("Información de contacto", validators=[DataRequired(),  edit_validate_contactInfo_uniqueness])
    enable = BooleanField("Habilitado")


class SearchInstitutionForm(FlaskForm):
    """
    Formulario utilizado para la búsqueda de instituciones.
    """
    name = StringField("Nombre")
    enable = SelectField("Habilitado", choices=[("none", "Todos los estados"), ("true", "Habilitado"), ("false", "Deshabilitado")])

class ChangeInstitutionForm(FlaskForm):
    """
    Formulario utilizado para el cambio de instituciones.
    """
    id = HiddenField("id")
