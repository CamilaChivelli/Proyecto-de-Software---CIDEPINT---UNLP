"""
Controller de `Configuration`.
"""
from flask import Blueprint, render_template, redirect, flash, url_for, abort
from src.web.controllers.auth import login_required
from src.core.models.configuration import Configuration
from src.core.forms.configuration import EditConfigurationForm
from src.web.helpers.auth import check_permission


configuration_blueprint = Blueprint("configurations", __name__, url_prefix="/configurations")


@configuration_blueprint.get("/")
@login_required
@check_permission(['configurations_show'])
def show():
    configuration = Configuration.query.first()
    form = EditConfigurationForm()

    if configuration:
        return render_template("configurations/show.html", configuration=configuration, form=form)
    else:
        return abort(404)


@configuration_blueprint.get("/edit")
@check_permission(['configurations_edit'])
@login_required
def edit():
    configuration = Configuration.query.first()
    form = EditConfigurationForm(obj=configuration)

    return render_template("configurations/edit.html", form=form)


@configuration_blueprint.post("/update")
@check_permission(['configurations_update'])
@login_required
def update():
    configuration = Configuration.query.first()
    form = EditConfigurationForm(obj=configuration)

    if form.validate_on_submit():
        configuration = Configuration.update(configuration, **form.data)

        flash("Configuraciones actualizadas!", "success")
        return redirect(url_for("configurations.show"))

    else:
        return render_template("configurations/edit.html", form=form)
