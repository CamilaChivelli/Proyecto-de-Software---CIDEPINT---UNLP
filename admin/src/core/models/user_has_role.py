"""
Define la entidad que representa a la tabla intermedia entre usuario, rol e institución.
"""
from operator import not_
from src.core.database import db
from sqlalchemy import and_, or_
from src.core.models.role import Role
from src.core.models.user import User


class UserRoleInstitution(db.Model):
    __tablename__ = "user_has_role"

    id = db.Column(db.Integer, primary_key=True, unique=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', backref='user_has_role')

    institution_id = db.Column(db.Integer, db.ForeignKey('institutions.id'))
    institution = db.relationship('Institution', backref='user_has_role')

    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    role = db.relationship('Role', backref='user_has_role')

    # Restricción de unicidad: institución - usuario
    __table_args__= (db.UniqueConstraint('user_id', 'institution_id', name='id_user_id_institution'),)


    @classmethod
    def create(klass, **kwargs):
        """
        Crea un `UserRoleInstitution`.
        """
        if kwargs.get("role_id") == 1 and kwargs.get("institution_id") is not None:
            raise ValueError("No se puede ser super-administrador de una institución en particular")

        else:
            create_attrs = ["user_id", "role_id", "institution_id"]
            attrs = { key: kwargs.get(key) for key in create_attrs }

            user_has_role = UserRoleInstitution(**attrs)

            db.session.add(user_has_role)
            db.session.commit()

            return user_has_role


    @classmethod
    def update(klass, user_has_role, **kwargs):
        """
        Actualiza el rol de un usuario de una institución dada.
        """
        update_attrs = ["role_id"]
        attrs = { key: kwargs.get(key) for key in update_attrs }

        for attribute, value in attrs.items():
            setattr(user_has_role, attribute, value)

        db.session.commit()

        return user_has_role


    @classmethod
    def destroy(klass, user_has_role):
        """
        Elimina a un usuario de una institución.
        """
        db.session.delete(user_has_role)
        db.session.commit()


    def get_role(user, institution_id):
            """
            Retorna un rol en base a los parámetros de usuario e institución.
            """
            user_role = UserRoleInstitution.get_user_institution_role_by_user(user)

            if user_role is None or len(user_role) == 0:
                return None
            if user_role[0].role_id == 1:
                return user_role[0].role
            else:
                return UserRoleInstitution.get_userInstitutionRole_by_institution_and_user(user,institution_id)


    def get_user_institution_role_by_user(user):
            """
            Retorna una lista que contiene la informacion de las instituciones y los roles asignados de un usuario.
            """
            user_id = getattr(user, "id", None)

            if user_id:
                return UserRoleInstitution.query.filter_by(user_id=user.id).all()
            else:
                return None


    def get_userInstitutionRole_by_institution_and_user(user, institution):
        """
        Retorna la lista de instituciones y sus roles de un usuario.
        """
        user_id = getattr(user, "id", None)
        user_role_institution = UserRoleInstitution.query.filter_by(user_id=user_id,institution_id=institution).first()

        return getattr(user_role_institution, "role", None)


    @classmethod
    def can_add_user_to_institution(klass, user, institution):
        """
        Retorna `True` si el usuario no es `super_administrador` ni tampoco se encuentra agregado en la institución.
        Caso contrario, retorna `False`.
        """
        if klass.is_super_administrador(user):
            return False

        user_has_roles = klass.query.filter(
            klass.user_id == user.id,
            klass.institution_id == institution.id
        ).all()

        if user_has_roles:
            return False

        else:
            return True


    @classmethod
    def is_super_administrador(klass, user):
        """
        Retorna `True` si el usuario es `super_administrador`.
        Caso contrario, retorna `False`.
        """
        query = klass.query.join(
            Role, klass.role_id == Role.id
        ).filter(
            Role.name == "super_administrador", klass.user_id == user.id
        )

        user_has_roles = db.session.execute(query).scalars().all()

        if user_has_roles:
            return True

        else:
            return False


    @classmethod
    def list_institution_users(klass, institution, **kwargs):
        """
        Retorna los usuarios asociados a una institución.
        """
        # Pagination
        page = int(kwargs.get("page")) if kwargs.get("page") else 1
        per_page = kwargs.get("per_page")

        # Se construye la query de busqueda
        query = db.session.query(
            UserRoleInstitution
        ).join(
            UserRoleInstitution.user
        ).join(
            UserRoleInstitution.institution
        ).join(
            UserRoleInstitution.role
        ).filter(
            UserRoleInstitution.institution_id == institution.id
        ).filter(
            not_(UserRoleInstitution.role_id == 1)
        )

        aux = db.paginate(query, page=1, per_page=per_page)


        if page > aux.pages or page < 0:
            return aux
        else:
            return db.paginate(query, page=page, per_page=per_page)


    @classmethod
    def list_institution_selectable_users(klass, institution, **kwargs):
        """
        Retorna los usuarios que pueden ser asociados a una institución.
        """
        # Pagination
        page = int(kwargs.get("page")) if kwargs.get("page") else 1
        per_page = kwargs.get("per_page")

        # Se construye la query de busqueda
        subquery = db.session.query(
             UserRoleInstitution.user_id
        ).filter(
            or_(
                and_(
                    UserRoleInstitution.user_id.isnot(None),
                    UserRoleInstitution.role_id.isnot(None),
                    UserRoleInstitution.institution_id == None),
                and_(
                    UserRoleInstitution.institution_id == institution.id
                )
            )
        )

        query = db.session.query(User).filter(User.id.not_in(subquery))

        aux = db.paginate(query, page=1, per_page=per_page)


        if page > aux.pages or page < 0:
            return aux
        else:
            return db.paginate(query, page=page, per_page=per_page)


    @classmethod
    def list_super_administrador_users(klass):
        """
        Retorna una lista con todo los usuarios con rol de `super_administrador`.

        Todo: se pueden mejorar "can_add_user_to_institution()" y "is_super_administrador"
        """
        subquery = db.session.query(Role.id).filter_by(name="super_administrador")
        query = db.session.query(User).join(klass, klass.user_id == User.id).filter(klass.role_id.in_(subquery))

        return query.all()


    @classmethod
    def list_user_institutions(klass, user, **kwargs):
        """
        Retorna las institución asociadas a un usuario.
        """
        # Pagination
        page = int(kwargs.get("page")) if kwargs.get("page") else 1
        per_page = kwargs.get("per_page")

        # Se construye la query de busqueda
        query = db.session.query(
            UserRoleInstitution
        ).filter(
            UserRoleInstitution.user_id == user.id
        ).filter(
            not_(UserRoleInstitution.role_id == 1)
        )

        aux = db.paginate(query, page=1, per_page=per_page)


        if page > aux.pages or page < 0:
            return aux
        else:
            return db.paginate(query, page=page, per_page=per_page)
