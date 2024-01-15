"""
Controller de `ServiceRequests`.
"""
import datetime
from flask import Blueprint, abort, flash, g, redirect, render_template, request, url_for
from src.core.forms.service_requests import EditServiceRequestForm, SearchServiceRequestForm
from src.core.models.service_requests import ServiceRequests
from datetime import datetime
from src.web.helpers.auth import check_permission, login_required


service_requests_blueprint = Blueprint("service_requests", __name__, url_prefix="/service_requests")


@service_requests_blueprint.get("/")
@login_required
@check_permission(["service_requests_index"])
def index():
    args = request.args
    service_type = args.get("service_type")
    status = args.get("status")
    user = args.get("user")

    date_start_str = request.args.get("date_start")
    date_end_str = request.args.get("date_end")
    date_start = datetime.strptime(date_start_str, '%Y-%m-%d').replace(hour=00, minute=00, second=00, microsecond=0)if date_start_str else None
    date_end = datetime.strptime(date_end_str, '%Y-%m-%d').replace(hour=23, minute=59, second=59, microsecond=0) if date_end_str else None

    form = SearchServiceRequestForm(status=status, service_type=service_type, date_start=date_start, date_end=date_end, user=user)

    pagination = ServiceRequests.search(
        page=args.get("page"),
        per_page=g.configuration.per_page,
        status=status,
        service_type=service_type,
        date_start=date_start,
        date_end=date_end,
        user=user
    )

    return render_template("service_requests/index.html", form=form, pagination=pagination)


@service_requests_blueprint.get("/<int:id>")
@login_required
@check_permission(["service_requests_show"])
def show(id):
    request = ServiceRequests.query.get(id)

    if request:
        return render_template("service_requests/show.html", request=request)

    else:
        return abort(404)


@service_requests_blueprint.get("/<int:id>/edit")
@login_required
@check_permission(["service_requests_edit"])
def edit(id):
    request = ServiceRequests.query.get(id)

    if request:
        form = EditServiceRequestForm(obj=request)
        form.status.default = request.status.name
        form.institution_observation.default = request.institution_observation
        form.process()
        return render_template("service_requests/edit.html", form=form, request=request)

    else:
        flash("Servicio no encontrado", "danger")
        return abort(404)


@service_requests_blueprint.post("/<int:id>/update")
@login_required
@check_permission(["service_requests_update"])
def update(id):
    request = ServiceRequests.query.get(id)

    if request:
        form = EditServiceRequestForm(obj=request)

        if form.validate_on_submit():
            updated = ServiceRequests.update(request, **form.data)

            flash("Servicio actualizado", "success")
            return redirect(url_for("service_requests.show", id=updated.id))

        else:
            flash("No se pudo actualizar el servicio.", "danger")
            return render_template("service_requests/edit.html", form=form)
    else:
        flash("Servicio no encontrado.", "danger")
        return render_template("service_requests/edit.html")


@service_requests_blueprint.route("/<int:id>/destroy", methods=["GET","POST"])
@login_required
@check_permission(["service_requests_destroy"])
def destroy(id):
    service = ServiceRequests.query.get(id)

    if service:
        ServiceRequests.delete(service)
        flash("Solicitud eliminada", "success")
        return redirect(url_for("service_requests.index"))

    else:
        return abort(404)
