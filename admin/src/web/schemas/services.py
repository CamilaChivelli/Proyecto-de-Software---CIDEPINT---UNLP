"""
Schemas de servicio.
"""
from marshmallow import Schema, fields
from src.core.enums.service_type import ServiceTypeEnum
from src.web.schemas.institutions import InstitutionSchema


class ServiceSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.String()
    description = fields.String()
    keywords = fields.String()
    service_type = fields.Enum(ServiceTypeEnum, by_value=True)
    enable = fields.Boolean()
    institution = fields.Nested(InstitutionSchema)
    inserted_at = fields.DateTime()
    updated_at = fields.DateTime()

service_schema = ServiceSchema()
service_schema_list = ServiceSchema(many=True)
