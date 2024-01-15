"""
Formularios de `Configuration`.
"""
from flask_wtf import FlaskForm
from wtforms import EmailField, StringField, BooleanField, IntegerField, TextAreaField
from wtforms.validators import Email, NumberRange


class EditConfigurationForm(FlaskForm):
    """
    Formulario utilizado para la edición de la `Configuration`.
    """
    # Cantidad de elementos listados por página
    per_page = IntegerField("Elementos por página", validators=[NumberRange(min=1, max=100)])

    # Información de contacto
    email = EmailField("Email", validators=[Email()])
    phone_number = StringField("Telefono")
    web = StringField("Sitio Web")

    # Mantenimiento del sitio
    is_on_maintenance = BooleanField("Sitio en mantenimiento")
    maintenance_message = TextAreaField("Mensaje")