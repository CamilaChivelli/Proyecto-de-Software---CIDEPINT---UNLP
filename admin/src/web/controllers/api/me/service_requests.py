"""
API Controller para `ServiceRequests`.
"""
import datetime
from flask import Blueprint, request, g, json, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from marshmallow import ValidationError
from psycopg2 import IntegrityError
from src.core.models.service_requests import ServiceRequests
from src.core.models.user import User
from src.web.schemas.service_requests import service_requests_schema, service_requests_schema_list, create_service_requests_schema
from src.core.enums.status import StatusEnum


api_me_request_blueprint = Blueprint("api_me_requests", __name__, url_prefix="/api/me/requests")


@api_me_request_blueprint.get("/")
@jwt_required()
def index():
    current_user = get_jwt_identity()
    args = request.args
    page = args.get("page", type=int, default=1)
    per_page = args.get("per_page", type=int, default=g.configuration.per_page)
    sort = args.get("sort", default="inserted_at")
    order = args.get("order", default="desc")
    status = args.get("status")

    date_start = args.get("date_start")
    date_end = args.get("date_end")


    pagination = ServiceRequests.search_by_user_api(
        user_id=current_user,
        page=page,
        per_page=per_page,
        sort=sort,
        order=order,
        date_start=date_start,
        date_end=date_end,
        status=status
    )

    return jsonify(
        data=json.loads(service_requests_schema_list.dumps(pagination)),
        page=pagination.page,
        per_page=pagination.per_page,
        total=pagination.total,
    ), 200


@api_me_request_blueprint.get("/<int:id>")
@jwt_required()
def show(id):
    current_user = get_jwt_identity()
    service_request = ServiceRequests.search_by_id_api(id)

    if (service_request.user_id == current_user):
        service_request = ServiceRequests.query.filter_by(id=id).first()

    else:
        service_request = None

    if (service_request) is None:
        return jsonify(result="La solicitud no te pertenece"), 403

    else:
        return service_requests_schema.dumps(service_request), 200


@api_me_request_blueprint.post("")
@jwt_required()
def create():
    current_user = get_jwt_identity()
    params = request.get_json()
    params["user_id"] = current_user

    if "service_id" in params:
        data = create_service_requests_schema.load(params)
        new_request = ServiceRequests.create(**data)
        return service_requests_schema.dumps(new_request), 201
    else:
        return jsonify(result="Se necesita enviar el id del servicio"), 400

@api_me_request_blueprint.put("/<int:id>/notes")
@jwt_required()
def update(id):
    user_id = get_jwt_identity()
    current_user = User.find_by(id=user_id)

    current_user = get_jwt_identity()
    params = request.get_json()
    params["user_id"] = current_user
    try:
        data = create_service_requests_schema.load(params)
        service_request = ServiceRequests.search_by_id_api(id)

        if service_request is None:
            return {"error": "El ID del servicio ingresado no existe"}, 400
        if current_user != service_request.user_id:
            return {"error": "El ID del servicio ingresado no corresponde al usuario"}, 400
        # Actualiza los campos de la solicitud con los nuevos datos
        update = ServiceRequests.update(service_request, **data)

        # Devuelve la solicitud actualizada
        return service_requests_schema.dumps(update), 201

    except IntegrityError:
        return {"error": "Error: No se pudo cambiar las notas"}, 400

    except ValidationError:
        return {"error": "Hay campos enviados que no existen"}, 400


@api_me_request_blueprint.get("/status")
def index_status():
    enum_data = [{enum.name: enum.value} for enum in StatusEnum]
    return jsonify(data=enum_data), 200

@api_me_request_blueprint.get("/ranking-requests")
def ranking_services():
    ranking = ServiceRequests.get_service_ranking()
    ranking_list = {service:count for service, count in ranking}

    return ranking_list, 200

@api_me_request_blueprint.get("/ranking-status")
def ranking_status():
    ranking = ServiceRequests.get_status_ranking()
    ranking_list = {service:count for service, count in ranking}

    return ranking_list, 200

@api_me_request_blueprint.get("/ranking-monthly")
def get_monthly_ranking():
    ranking = ServiceRequests.get_monthly_ranking()
    ranking_json = json.dumps(ranking, sort_keys=False)
    return ranking_json, 200
