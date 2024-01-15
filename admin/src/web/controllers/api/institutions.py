"""
API Controller para `Institutions`.
"""
from flask import Blueprint, request, json, jsonify
from src.core.models.institution import Institution
from src.web.schemas.institutions import institutions_schema, institution_schema


api_institution_blueprint = Blueprint("institution_api", __name__, url_prefix="/api/institutions")


@api_institution_blueprint.get("/")
def index():
    args = request.args

    page = args.get("page")
    per_page = args.get("per_page")
    name = args.get("name")
    enable = args.get("enable")

    if page and not page.isdigit():
        return jsonify(error="El parámetro 'page' no es un número entero"), 400

    if per_page and not per_page.isdigit():
        return jsonify(error="El parámetro 'per_page' no es un número entero"), 400

    pagination = Institution.search(
        page=page,
        per_page=per_page,
        name = name,
        enable = enable
    )

    return jsonify(
        data=json.loads(institutions_schema.dumps(pagination)),
        page=pagination.page,
        per_page=pagination.per_page,
        total=pagination.total
    ), 200


@api_institution_blueprint.get("/<id>")
def show(id):

    if not id.isdigit():
        return jsonify(error="El parámetro 'id' no es un número natural"), 400

    service = Institution.query.get(int(id))

    if service:
        return institution_schema.dump(service), 200

    else:
        return jsonify(message="No se encontró la institución con el ID ingresado"), 400
