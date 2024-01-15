"""
Schemas de usuario.
"""
from marshmallow import Schema, fields


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    firstname = fields.String()
    lastname = fields.String()
    email = fields.String()
    password = fields.String()
    active = fields.Boolean()
    updated_at = fields.DateTime()
    created_at = fields.DateTime()

user_schema = UserSchema()
