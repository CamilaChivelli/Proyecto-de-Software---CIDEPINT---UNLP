"""
API Controller para `Services`.
"""
from flask import Blueprint, g, request, json, jsonify
from src.core.models.service import Service
from src.web.schemas.services import service_schema, service_schema_list


api_service_blueprint = Blueprint("services_api", __name__, url_prefix="/api/services")


@api_service_blueprint.get("/search")
def index():
    args = request.args
    page = args.get("page")
    per_page = args.get("per_page")
    q = args.get("q", type=str, default="")
    type = args.get("type", type=str, default="")

    if page and not page.isdigit():
        return jsonify(error="El parámetro 'page' no es un número entero"), 400

    if per_page and not per_page.isdigit():
        return jsonify(error="El parámetro 'per_page' no es un número entero"), 400

    pagination = Service.searchApi(
            page=page,
            per_page=per_page,
            q=q,
            service_type=type
    )

    return jsonify(
            data=json.loads(service_schema_list.dumps(pagination)),
            page=pagination.page,
            per_page=pagination.per_page,
            total=pagination.total
    ), 200


@api_service_blueprint.get("/<id>")
def show(id):
        service = Service.query.filter_by(id=int(id), enable=True).first()

        if service:
            return service_schema.dump(service), 200

        else:
            return jsonify(message="No se encontró el servicio con el ID ingresado"), 404
