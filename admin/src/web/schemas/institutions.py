"""
Schemas de institucion.
"""
from marshmallow import Schema, fields


class InstitutionSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.String()
    info = fields.String()
    address = fields.String()
    location = fields.String()
    web = fields.String()
    keywords = fields.String()
    customer_service_hours = fields.String()
    contact_info = fields.String()
    enable = fields.Boolean()
    inserted_at = fields.DateTime()
    updated_at = fields.DateTime()

institution_schema = InstitutionSchema()
institutions_schema = InstitutionSchema(many=True)
