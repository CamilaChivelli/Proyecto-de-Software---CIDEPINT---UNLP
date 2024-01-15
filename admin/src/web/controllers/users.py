"""
Controller de `Users`.
"""
from flask import Blueprint, render_template, request, redirect, flash, url_for, abort, g
from src.core.models.user import User
from src.core.models.user_has_role import UserRoleInstitution
from src.core.forms.user import NewUserForm, EditUserForm, SearchUserForm
from src.web.helpers.auth import login_required, check_permission


user_blueprint = Blueprint("users", __name__, url_prefix="/users")


@user_blueprint.get("/")
@login_required
@check_permission(["users_index"])
def index():
    args = request.args
    email = args.get("email")
    active = args.get("active")

    form = SearchUserForm(email=email, active=active)

    pagination = User.search(
        page=args.get("page"),
        per_page=g.configuration.per_page,
        email=email,
        active=active
    )

    super_administrador_users = UserRoleInstitution.list_super_administrador_users()

    return render_template("users/index.html", form=form, pagination=pagination, super_administrador_users=super_administrador_users)


@user_blueprint.get("/<int:id>")
@login_required
@check_permission(["users_show"])
def show(id):
    user = User.query.get(id)

    if user and not UserRoleInstitution.is_super_administrador(user):
        args = request.args
        pagination = UserRoleInstitution.list_user_institutions(
            user,
            page=args.get("page"),
            per_page=g.configuration.per_page
        )

        return render_template("users/show.html", user=user, pagination=pagination)

    else:
        return abort(404)


@user_blueprint.get("/new")
@login_required
@check_permission(["users_new"])
def new():
    form = NewUserForm()
    return render_template("users/new.html", form=form)


@user_blueprint.post("/create")
@login_required
@check_permission(["users_create"])
def create():
    form = NewUserForm()

    if form.validate_on_submit():
        user = User.create(**form.data)

        flash(f"Usuario {user.email} creado!", "success")
        return redirect(url_for("users.show", id=user.id))

    else:
        return render_template("users/new.html", form=form)


@user_blueprint.get("/<int:id>/edit")
@login_required
@check_permission(["users_edit"])
def edit(id):
    user = User.query.get(id)

    if user and not UserRoleInstitution.is_super_administrador(user):
        form = EditUserForm(obj=user)
        return render_template("users/edit.html", form=form, user=user)

    else:
        return abort(404)


@user_blueprint.post("/<int:id>/update")
@login_required
@check_permission(["users_update"])
def update(id):
    user = User.query.get(id)

    if user and not UserRoleInstitution.is_super_administrador(user):
        form = EditUserForm(obj=user)

        if form.validate_on_submit():
            user = User.update(user, **form.data)

            flash(f"Usuario {user.email} actualizado!", "success")
            return redirect(url_for("users.show", id=user.id))

        else:
            return render_template("users/edit.html", form=form)

    else:
        return abort(404)


@user_blueprint.get("/<int:id>/destroy")
@login_required
@check_permission(["users_destroy"])
def destroy(id):
    user = User.query.get(id)

    if user and not UserRoleInstitution.is_super_administrador(user):
        user = User.destroy(user)

        flash(f"Usuario {user.email} eliminado!", "success")
        return redirect(url_for("users.index"))

    else:
        return abort(404)
