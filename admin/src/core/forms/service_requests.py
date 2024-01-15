"""
Formularios de `ServiceRequests`.
"""
from flask_wtf import FlaskForm
from wtforms import DateField, StringField, SelectField, TextAreaField
from wtforms.validators import ValidationError, Optional
from src.core.enums.service_type import ServiceTypeEnum
from src.core.enums.status import StatusEnum
from src.core.models.service_requests import ServiceRequests


def validate_request_uniqueness(form, field):
    """
    Levanta un `ValidationError` si el nombre ya se encuentra en uso.
    """
    service = ServiceRequests.find_by(name=field.data)

    if service:
        raise ValidationError("Usted ya tiene en proceso una solicitud bajo este servicio en la institución")


class EditServiceRequestForm(FlaskForm):
    """
    Formulario utilizado para la edición de la solicitud de un servicio.
    """
    status = SelectField("Estado", choices=[(status.name, status.value) for status in StatusEnum])
    institution_observation = TextAreaField("Descripción de la institución")


class SearchServiceRequestForm(FlaskForm):
    """
    Formulario utilizado para la búsqueda de una solicitud.
    """
    status = SelectField("Estado de la solicitud", choices = [("", "Todos los estados")] + [(choice.name, choice.value) for choice in StatusEnum])
    service_type = SelectField("Tipo de servicio", choices=[("", "Todos los tipos")] + [(choice.name, choice.value) for choice in ServiceTypeEnum])
    date_start = DateField("Fecha de inicio", format='%Y-%m-%d', validators=[Optional()])
    date_end = DateField("Fecha de finalización", format='%Y-%m-%d', validators=[Optional()])
    user = StringField("Usuario", validators=[Optional()])
