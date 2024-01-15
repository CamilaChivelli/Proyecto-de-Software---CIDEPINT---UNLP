"""
Controller de `InstitutionUsers`.
"""
from flask import Blueprint, render_template, request, g, abort, flash, redirect, url_for
from src.core.models.user import User
from src.core.models.role import Role
from src.core.models.institution import Institution
from src.core.models.user_has_role import UserRoleInstitution
from src.web.helpers.auth import login_required, check_permission
from src.core.forms.institution_user import NewInstitutionUserForm, EditInstitutionUserForm


institution_users_blueprint = Blueprint("institution_users", __name__, url_prefix="/institutions")


@institution_users_blueprint.get("/<int:institution_id>/users")
@login_required
@check_permission(["institution_users_index"])
def index(institution_id):
    institution = Institution.query.get(g.current_institution.id)

    pagination = UserRoleInstitution.list_institution_users(
        institution=institution,
        page=request.args.get("page"),
        per_page=g.configuration.per_page
    )

    return render_template("institutions/users/index.html", pagination=pagination, institution=institution)


@institution_users_blueprint.get("/<int:institution_id>/users/new")
@login_required
@check_permission(["institution_users_new"])
def new(institution_id):
    user_id = request.args.get("id")
    institution = Institution.query.get(g.current_institution.id)

    if user_id and int(user_id):
        user = User.query.get(int(user_id))
        user = user if UserRoleInstitution.can_add_user_to_institution(user, institution) else None

        if user:
            form = NewInstitutionUserForm()
            form.role_id.choices = Role.list_selectable_roles()

            return render_template("institutions/users/new.html", user_selection=False, form=form, institution=institution, user=user)

        else:
            return abort(403)

    else:
        pagination = UserRoleInstitution.list_institution_selectable_users(
            institution=institution,
            page=request.args.get("page"),
            per_page=g.configuration.per_page
        )

        return render_template("institutions/users/new.html", user_selection=True, pagination=pagination, institution=institution)


@institution_users_blueprint.post("/<int:institution_id>/users/create")
@login_required
@check_permission(["institution_users_create"])
def create(institution_id):
    form = NewInstitutionUserForm()
    form.role_id.choices = Role.list_selectable_roles()

    if form.validate_on_submit():
        UserRoleInstitution.create(**form.data)

        flash("Usuario agregado!", "success")
        return redirect(url_for("institution_users.index", institution_id=g.current_institution.id))

    else:
        user = User.query.get(form.user_id)
        return render_template("institutions/users/new.html", user_selection=False, form=form, user=user)


@institution_users_blueprint.get("/<int:institution_id>/users/<int:id>/edit")
@login_required
@check_permission(["institution_users_edit"])
def edit(institution_id, id):
    institution = Institution.query.get(g.current_institution.id)
    user = User.query.get(id)
    user_role_institution = UserRoleInstitution.query.filter_by(institution_id=g.current_institution.id, user_id=id).first()

    if user_role_institution:
        form = EditInstitutionUserForm(obj=user_role_institution)
        form.role_id.choices = Role.list_selectable_roles()

        return render_template("institutions/users/edit.html", form=form, institution=institution, user=user)

    else:
        return abort(404)


@institution_users_blueprint.post("/<int:institution_id>/users/<int:id>/update")
@login_required
@check_permission(["institution_users_update"])
def update(institution_id, id):
    user_role_institution = UserRoleInstitution.query.filter_by(institution_id=g.current_institution.id, user_id=id).first()

    form = EditInstitutionUserForm(obj=user_role_institution)
    form.role_id.choices = Role.list_selectable_roles()

    if form.validate_on_submit():
        UserRoleInstitution.update(user_role_institution, **form.data)

        flash("Usuario actualizado!", "success")
        return redirect(url_for("institution_users.index", institution_id=g.current_institution.id))

    else:
        institution = Institution.query.get(g.current_institution.id)
        user = User.query.get(id)

        return render_template("institutions/users/edit.html", form=form, institution=institution, user=user)


@institution_users_blueprint.get("/<int:institution_id>/users/<int:id>/destroy")
@login_required
@check_permission(["institution_users_destroy"])
def destroy(institution_id, id):
    user_role_institution = UserRoleInstitution.query.filter_by(institution_id=g.current_institution.id, user_id=id).first()

    if user_role_institution and not user_role_institution.role.is_super_administrador():
        UserRoleInstitution.destroy(user_role_institution)

        flash("Usuario eliminado de la institución!", "success")
        return redirect(url_for("institution_users.index", institution_id=g.current_institution.id))

    else:
        return abort(401)
