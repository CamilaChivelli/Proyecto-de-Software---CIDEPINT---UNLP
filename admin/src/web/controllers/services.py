"""
Controller de `Services`.
"""
from flask import Blueprint, render_template, request, flash, redirect, url_for, g
from src.core.models.service import Service
from src.web.helpers.auth import login_required, check_permission
from src.core.forms.service import SearchServiceForm, EditServiceForm, NewServiceForm


service_blueprint = Blueprint("services", __name__, url_prefix="/services")


@service_blueprint.get("")
@login_required
@check_permission(["services_index"])
def index():
    args = request.args
    name = args.get("name")
    enable = args.get("enable")
    service_type = args.get("service_type")

    form = SearchServiceForm(name=name, enable=enable, service_type=service_type)

    pagination = Service.search(
        page=args.get("page"),
        per_page=g.configuration.per_page,
        name=name,
        enable=enable,
        service_type=service_type,
        institution=g.current_institution
    )

    return render_template("services/index.html", form=form, pagination=pagination)


@service_blueprint.get("/<string:name>")
@login_required
@check_permission(["services_show"])
def show(name):
    service = Service.find_by(name=name, institution_id=g.current_institution.id)

    if service:
        return render_template("services/show.html", service=service)

    else:
        flash("Servicio no encontrado", "danger")
        return redirect(url_for('services.index'))


@service_blueprint.get("/new")
@login_required
@check_permission(["services_new"])
def new():
    form = NewServiceForm(institution_id=g.current_institution.id)
    return render_template("services/new.html", form=form)


@service_blueprint.post("")
@login_required
@check_permission(["services_create"])
def create():
    form = NewServiceForm(institution_id=g.current_institution.id)

    if form.validate_on_submit():
        new_service = Service.create(**form.data)

        if new_service:
            flash("Servicio creado exitosamente", "success")
            return redirect(url_for('services.show', name=new_service.name))

        else:
            flash("No se pudo crear el servicio", "danger")
            return render_template("services/new.html", form=form)

    else:
        return render_template("services/new.html", form=form)


@service_blueprint.get("/<string:name>/edit")
@login_required
@check_permission(["services_edit"])
def edit(name):
    service = Service.find_by(name=name, institution_id=g.current_institution.id)

    if service:
        form = EditServiceForm(obj=service)

        return render_template("services/edit.html", form=form, service=service)

    else:
        flash("Servicio no encontrado", "danger")
        return redirect(url_for('services.index'))


@service_blueprint.post("/<string:name>/update")
@login_required
@check_permission(["services_update"])
def update(name):
    service = Service.find_by(name=name, institution_id=g.current_institution.id)

    if service:
        form = EditServiceForm(obj=service)
        form.service = service

        if form.validate_on_submit():
            service = Service.update(service, **form.data)

            flash("Servicio actualizado", "success")
            return redirect(url_for("services.show", name=service.name))

        else:
            return render_template("services/edit.html", form=form, service=service)

    else:
        flash("Servicio no encontrado", "danger")
        return redirect(url_for('services.index'))


@service_blueprint.route("/<string:name>/destroy", methods=["GET", "POST"])
@login_required
@check_permission(["services_destroy"])
def destroy(name):
    service = Service.find_by(name=name, institution_id=g.current_institution.id)

    if service:
        Service.delete_service(service)
        flash("Servicio eliminado", "success")

    else:
        flash("Servicio no encontrado", "danger")

    return redirect(url_for('services.index'))
