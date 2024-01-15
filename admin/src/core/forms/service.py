"""
Formularios de servicios.
"""
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SelectField, IntegerField, validators
from wtforms.validators import DataRequired, ValidationError
from src.core.enums.service_type import ServiceTypeEnum
from src.core.models.service import Service
from src.core.models.institution import Institution


def validate_institution(form, field):
    """
    Levanta un `ValidationError` si no existe la institución o si no está habilitada.
    """
    institution = Institution.find_by(id=field.data)

    if not institution or not institution.enable:
        raise ValidationError("Institución no habilitada.")


def validate_name_uniqueness(form, field):
    """
    Levanta un `ValidationError` si el nombre ya se encuentra en uso.
    """
    service = Service.find_by(name=field.data)

    if service:
        service_id = form.data.get('id', None)

        if service.id != service_id:
            raise ValidationError("Nombre inválido.")

def validate_keywords(form, field):
    """
    Comprueba que el formato de keywords sea una secuencia separado por coma
    """

    keywords = form.data.get('keywords', None)



class NewServiceForm(FlaskForm):
    """
    Formulario utilizado para la creación del servicio.
    """
    institution_id = IntegerField(validators=[DataRequired(), validate_institution])
    name = StringField("Nombre", validators=[DataRequired(), validate_name_uniqueness])
    description = StringField("Descripción")
    keywords = StringField('Palabras claves', [
        validators.Regexp(r'^[a-zA-Z]+(,[a-zA-Z]+)*$', message='Ingresa palabras separadas por coma sin espacios o caracteres especiales')
    ])
    service_type = SelectField("Tipo de servicio", choices=[(choice.name, choice.value) for choice in ServiceTypeEnum])
    enable = BooleanField("Habilitado")


class EditServiceForm(FlaskForm):
    """
    Formulario utilizado para la edición del servicio.
    """
    id = IntegerField()
    name = StringField("Nombre", validators=[DataRequired(), validate_name_uniqueness])
    description = StringField("Descripción")
    keywords = StringField('Palabras claves', [
        validators.Regexp(r'^[a-zA-Z]+(,[a-zA-Z]+)*$', message='Ingresa palabras separadas por coma sin espacios o caracteres especiales')
    ])
    service_type = SelectField("Tipo de servicio", choices=[(service_type.name, service_type.value) for service_type in ServiceTypeEnum])
    enable = BooleanField("Habilitado")


class SearchServiceForm(FlaskForm):
    """
    Formulario utilizado para la búsqueda del servicio.
    """
    name = StringField("Nombre")
    service_type  = SelectField("Tipo de servicio", choices=[("", "Todos los servicios")] + [(choice.name, choice.value) for choice in ServiceTypeEnum])
    enable = SelectField("Habilitado",
                         choices=[
                             ("none", "Habilitado o Deshabilitado"),
                             ("true", "Habilitado"),
                             ("false", "Deshabilitado")
                             ]
                        )
