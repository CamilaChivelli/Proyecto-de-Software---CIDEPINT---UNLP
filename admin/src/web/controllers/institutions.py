"""
Controller de `Institutions`.
"""
from flask import Blueprint, render_template, abort, request, flash, redirect, url_for, g
from src.core.models.institution import Institution
from src.core.forms.institution import SearchInstitutionForm, EditInstitutionForm, NewInstitutionForm
from src.web.helpers.auth import login_required, check_permission


institution_blueprint = Blueprint("institutions", __name__, url_prefix="/institutions")


@institution_blueprint.get("/")
@login_required
@check_permission(["institutions_index"])
def index():
    args = request.args
    name = args.get("name")
    enable = args.get("enable")

    form = SearchInstitutionForm(name=name, enable=enable)

    pagination = Institution.search(
        page=args.get("page"),
        per_page=g.configuration.per_page,
        name=name,
        enable=enable
    )

    return render_template("institutions/index.html", form=form, pagination=pagination)


@institution_blueprint.get("/<string:name>")
@login_required
@check_permission(["institutions_show"])
def show(name):
    institution = Institution.find_by(name=name)

    if institution:
        return render_template("institutions/show.html", institution=institution)

    else:
        flash("Institución no encontrada", "danger")
        return redirect(url_for('institutions.index'))


@institution_blueprint.get("/<string:name>/edit")
@login_required
@check_permission(["institutions_edit"])
def edit(name):
    institution = Institution.find_by(name=name)

    if institution:
        form = EditInstitutionForm(obj=institution)
        return render_template("institutions/edit.html", form=form, institution=institution)

    else:
        flash("Institución no encontrada", "danger")
        return redirect(url_for('institutions.index'))


@institution_blueprint.post("/<string:name>/update")
@login_required
@check_permission(["institutions_update"])
def update(name):
    institution = Institution.find_by(name=name)

    if institution:
        form = EditInstitutionForm(obj=institution)
        form.institution = institution

        if form.validate_on_submit():
            institution = Institution.update(institution, **form.data)

            flash("Institución actualizada", "success")
            return redirect(url_for("institutions.show", name=institution.name))
        else:
            return render_template("institutions/edit.html", form=form, institution=institution)
    else:
        flash("No se encontró la institución.", "danger")
        return render_template("institutions/edit.html")


@institution_blueprint.get("/new")
@login_required
@check_permission(["institutions_new"])
def new():
    form = NewInstitutionForm()
    return render_template("institutions/new.html", form=form)


@institution_blueprint.post("/create")
@login_required
@check_permission(["institutions_create"])
def create():
    form = NewInstitutionForm()
    if form.validate_on_submit():
        new_institution = Institution.create(**form.data)

        if new_institution:
            flash("Institución creada exitosamente", "success")
            return redirect(url_for("institutions.show", name=new_institution.name))

        else:
            flash("No se pudo crear la institución.", "danger")
            return render_template("institutions/new.html", form=form)

    else:
        return render_template("institutions/new.html", form=form)


@institution_blueprint.route("/<string:name>/destroy", methods=["GET","POST"])
@login_required
@check_permission(["institutions_destroy"])
def destroy(name):
    institution = Institution.find_by(name=name)

    if institution:
        Institution.delete_institution(institution)

        flash("Institución eliminada", "success")
        return redirect(url_for("institutions.index"))

    else:
        return abort(404)


@institution_blueprint.route("/<string:name>/activate", methods=["GET","POST"])
@login_required
@check_permission(["institutions_activate"])
def activate(name):
    institution = Institution.find_by(name=name)

    if institution:
        if not Institution.is_enable(institution):
            institution = Institution.toggle_enable(institution)
            flash("Estado de la institución actualizado", "success")
            return redirect(url_for("institutions.show", name=institution.name))

        else:
            flash("Ya está habilitada", "success")
            return redirect(url_for("institutions.show", name=institution.name))

    else:
        return abort(404)


@institution_blueprint.route("/<string:name>/deactivate", methods=["GET","POST"])
@login_required
@check_permission(["institutions_deactivate"])
def deactivate(name):
    institution = Institution.find_by(name=name)

    if institution:

        if Institution.is_enable(institution):
            institution = Institution.toggle_enable(institution)
            flash("Estado de la institución actualizado", "success")
            return redirect(url_for("institutions.show", name=institution.name))

        else:
            flash("Ya está deshabilitada", "success")
            return redirect(url_for("institutions.show", name=institution.name))

    else:
        return abort(404)