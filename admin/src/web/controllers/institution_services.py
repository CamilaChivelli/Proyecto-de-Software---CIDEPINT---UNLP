"""
Controller de `InstitutionServices`.
"""
from flask import render_template, request, g, Blueprint
from src.core.models.service import Service
from src.core.models.institution import Institution
from src.core.forms.service import SearchServiceForm
from src.web.helpers.auth import login_required, check_permission


institution_services_blueprint = Blueprint("institution_services", __name__, url_prefix="/cambienestoporfavor")


@institution_services_blueprint.get("/<string:institution_name>/services")
@login_required
@check_permission(["services_index"])
def show_services(institution_name):
    institution = Institution.find_by(name=institution_name)

    if institution:
        args = request.args
        name = args.get("name")
        institution_name = institution.name
        enable = args.get("enable")
        service_type = args.get("service_type")

        form = SearchServiceForm(name=name, institution_name=institution_name, enable=enable, service_type=service_type)

        pagination = Service.search(

            per_page=g.configuration.per_page,
            name=name,
            institution_name=institution_name,
            enable=enable,
            service_type=service_type
        )

        return render_template("services/index.html", form=form, pagination=pagination, institution_name=institution_name)

    else:
        return render_template("/home.html")
