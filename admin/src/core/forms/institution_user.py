"""
Formularios de `InstitutionUser`.
"""
from flask_wtf import FlaskForm
from wtforms import SelectField, IntegerField
from wtforms.widgets import HiddenInput
from wtforms.validators import DataRequired


class NewInstitutionUserForm(FlaskForm):
    """
    Formulario utilizado para agregar un `User` a una `Institution`.
    """
    # IMPORTANTE: `choices` debe ser seteado desde el controlador.
    role_id = SelectField("Seleccione un rol", choices=[], validators=[DataRequired()], coerce=int)
    user_id = IntegerField(widget=HiddenInput())
    institution_id = IntegerField(widget=HiddenInput())


class EditInstitutionUserForm(FlaskForm):
    """
    Formulario utilizado para editar un `User` de una `Institution`.
    """
    # IMPORTANTE: `choices` debe ser seteado desde el controlador.
    role_id = SelectField("Seleccione un rol", choices=[], validators=[DataRequired()], coerce=int)
