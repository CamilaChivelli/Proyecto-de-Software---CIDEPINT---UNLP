"""
API Controller para `ServiceTypes`.
"""
from flask import Blueprint, jsonify
from src.core.enums.service_type import ServiceTypeEnum


api_service_types_blueprint = Blueprint("api_service_types", __name__, url_prefix="/api/service-types")


@api_service_types_blueprint.get("/")
def index():
    enum_data = [{enum.name: enum.value} for enum in ServiceTypeEnum]
    return jsonify(data=enum_data), 200
