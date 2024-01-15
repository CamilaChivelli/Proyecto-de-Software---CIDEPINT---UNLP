"""
Schemas de solicitud de servicios.
"""
from marshmallow import Schema, fields, validate
from src.core.enums.status import StatusEnum
from src.web.schemas.services import ServiceSchema


class ServiceRequestsSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int()
    service = fields.Nested(ServiceSchema)
    user_observation = fields.String()
    institution_observation = fields.String()
    status = fields.Enum(StatusEnum, by_value=True)
    inserted_at = fields.DateTime()
    updated_at = fields.DateTime()
    file_path = fields.String()

service_requests_schema = ServiceRequestsSchema()
service_requests_schema_list = ServiceRequestsSchema(many=True)


class CreateServiceRequestsSchema(Schema):
    user_id = fields.Int()
    service_id = fields.Int()
    user_observation = fields.String()
    status = fields.String(validate=validate.OneOf([e.value for e in StatusEnum]), attribute='status')
    file_path = fields.String()

create_service_requests_schema = CreateServiceRequestsSchema()
