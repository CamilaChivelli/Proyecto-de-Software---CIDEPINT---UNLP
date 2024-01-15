"""
Define la entidad que representa a un usuario.
"""
from datetime import datetime
from src.core.database import db
from werkzeug.security import generate_password_hash


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, unique=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean, default=False)
    firstname = db.Column(db.String(255))
    lastname = db.Column(db.String(255))
    random_key = db.Column(db.String(255)) # Sirve para almacenar el enlace temporal de registro
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


    @classmethod
    def create(klass, **kwargs):
        """
        Crea un usuario.
        """
        create_attrs = ["email", "password", "active", "firstname", "lastname", "random_key"]
        attrs = { key: kwargs.get(key) for key in create_attrs }

        if attrs["password"]:
            attrs["password"] = generate_password_hash(attrs["password"], method="scrypt")

        user = User(**attrs)

        db.session.add(user)
        db.session.commit()

        return user


    @classmethod
    def update(klass, user, **kwargs):
        """
        Actualiza un usuario.
        """
        update_attrs = ["email", "active", "firstname", "lastname"]
        attrs = { key: kwargs.get(key) for key in update_attrs }

        for attribute, value in attrs.items():
            setattr(user, attribute, value)

        db.session.commit()

        return user


    @classmethod
    def update_password(klass, user, password):
        user.password = generate_password_hash(password, method='scrypt')
        user.active = True

        db.session.commit()

        return user


    @classmethod
    def find_by(klass, **kwargs):
        """
        Retorna un usuario según el criterio de búsqueda ingresado.
        """
        return User.query.filter_by(**kwargs).first()


    @classmethod
    def search(klass, **kwargs):
        """
        Retorna una lista de usuarios según el criterio de búsqueda ingresado.
        """
        # Pagination
        page = int(kwargs.get("page")) if kwargs.get("page") else 1
        per_page = kwargs.get("per_page")

        # Campos de búsqueda
        email = kwargs.get("email")
        active = kwargs.get("active")

        # Se parsea el valor de active
        active = None if active not in ["true", "false"] else active
        active = True if active == "true" else active
        active = False if active == "false" else active

        # Se construye la query de busqueda
        query = User.query
        query = query.filter(User.active == active) if active in [True, False] else query
        query = query.filter(User.email.icontains(email)) if email not in [None, ""] else query

        aux = db.paginate(query, page=1, per_page=per_page)


        if page > aux.pages or page < 0:
            return aux
        else:
            return db.paginate(query, page=page, per_page=per_page)


    @classmethod
    def destroy(klass, user):
        """
        Elimina un usuario.
        """
        User.delete_all_roles(user)
        User.cancel_all_service_requests(user)

        db.session.delete(user)
        db.session.commit()

        return user


    @classmethod
    def delete_all_roles(klass, user):
        """
        Se eliminan todos los roles del usuario en las instituciones a las que pertenece.
        """
        from src.core.models.user_has_role import UserRoleInstitution

        all_roles = UserRoleInstitution.query.filter_by(user_id=user.id).all()
        for role in all_roles:
            UserRoleInstitution.destroy(role)


    @classmethod
    def cancel_all_service_requests(klass, user):
        """
        Se cancelan todas las solicitudes de servicio del usuario.
        """
        from src.core.models.service_requests import ServiceRequests

        all_service_requests = ServiceRequests.query.filter_by(user_id=user.id).all()
        for request in all_service_requests:
            ServiceRequests.override(request, user_id=user.id)


    def full_name(self):
        """
        Retorna el nombre completo del usuario en formato "apellido, nombre".
        """
        names = [self.lastname, self.firstname]
        names[:] = [name for name in names if name]

        return ", ".join(names) or "-"
