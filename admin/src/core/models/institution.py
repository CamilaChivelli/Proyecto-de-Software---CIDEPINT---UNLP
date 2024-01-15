"""
Define la entidad que representa a una institución.
"""
from datetime import datetime
from sqlalchemy import func
from src.core.database import db
from src.core.models.service import Service
from src.core.models.user_has_role import UserRoleInstitution


class Institution(db.Model):
    __tablename__ = "institutions"

    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    info = db.Column(db.String(255))
    address = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    web = db.Column(db.String(255), unique=True, nullable=False)
    keywords = db.Column(db.String(255))
    customer_service_hours = db.Column(db.String(255))
    contact_info = db.Column(db.String(255), unique=True, nullable=False)
    enable = db.Column(db.Boolean, default=False)

    services = db.relationship("Service", back_populates="institution")

    inserted_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


    @classmethod
    def create(klass, **kwargs):
        """
        Crea una institución.
        """
        create_attrs = ["name", "info", "address", "location", "web", "keywords", "customer_service_hours", "contact_info", "enable"]
        attrs = { key: kwargs.get(key) for key in create_attrs }

        institution = Institution(**attrs)

        db.session.add(institution)
        db.session.commit()

        return institution


    @classmethod
    def find_by(klass, **kwargs):
        """
        Retorna una institución según el criterio de búsqueda ingresado.
        """
        search = Institution.query

        if kwargs.get('name'):
            name = kwargs.pop('name')
            search = search.filter(func.replace(func.lower(Institution.name), " ", "").ilike(name.replace(" ","")))

        if kwargs.get('info'):
            info = kwargs.pop('info')
            search = search.filter(Institution.info.icontains(info))

        if kwargs.get('address'):
            address = kwargs.pop('address')
            search = search.filter(Institution.address.ilike(address))

        if kwargs.get('location'):
            location = kwargs.pop('location')
            search = search.filter(Institution.location.ilike(location))

        if kwargs.get('web'):
            web = kwargs.pop('web')
            search = search.filter(func.replace(func.lower(Institution.web), " ", "").ilike(web.replace(" ","")))


        if kwargs.get('keywords'):
            keywords = kwargs.pop('keywords')
            search = search.filter(Institution.keywords.icontains(keywords))

        if kwargs.get('customer_service_hours'):
            customer_service_hours = kwargs.pop('customer_service_hours')
            search = search.filter(Institution.customer_service_hours.icontains(customer_service_hours))

        if kwargs.get('contact_info'):
            contact_info = kwargs.pop('contact_info')
            search = search.filter(func.replace(func.lower(Institution.contact_info), " ", "").ilike(contact_info.replace(" ","")))

        return search.filter_by(**kwargs).first()

    @classmethod
    def find_all_by(klass, **kwargs):
        """
        Lista todas las instituciones encontradas según el criterio de búsqueda ingresado.
        """
        search = Institution.query

        if kwargs.get('name'):
            name = kwargs.pop('name')
            search = search.filter(func.replace(func.lower(Institution.name), " ", "").ilike(name.replace(" ","")))

        if kwargs.get('info'):
            info = kwargs.pop('info')
            search = search.filter(Institution.info.icontains(info))

        if kwargs.get('address'):
            address = kwargs.pop('address')
            search = search.filter(Institution.address.ilike(address))

        if kwargs.get('location'):
            location = kwargs.pop('location')
            search = search.filter(Institution.location.ilike(location))

        if kwargs.get('web'):
            web = kwargs.pop('web')
            search = search.filter(func.replace(func.lower(Institution.web), " ", "").ilike(web.replace(" ","")))

        if kwargs.get('keywords'):
            keywords = kwargs.pop('keywords')
            search = search.filter(Institution.keywords.icontains(keywords))

        if kwargs.get('customer_service_hours'):
            customer_service_hours = kwargs.pop('customer_service_hours')
            search = search.filter(Institution.customer_service_hours.icontains(customer_service_hours))

        if kwargs.get('contact_info'):
            contact_info = kwargs.pop('contact_info')
            search = search.filter(func.replace(func.lower(Institution.contact_info), " ", "").ilike(contact_info.replace(" ","")))

        return search.filter_by(**kwargs).all()

    @classmethod
    def search(klass, **kwargs):
        """
        Retorna una lista de institución en base a los parametros de búsqueda ingresados.
        """
        # Paginación
        page = int(kwargs.get("page")) if kwargs.get("page") else 1
        per_page = int(kwargs.get("per_page")) if kwargs.get("per_page") else 25

        # Campos de búsqueda
        name = kwargs.get("name")
        enable = kwargs.get("enable")

        # Se parsea el valor de enable
        enable = None if enable not in ["true", "false"] else enable
        enable = True if enable == "true" else enable
        enable = False if enable == "false" else enable

        # Se construye la query de busqueda
        query = Institution.query

        query = query.filter(Institution.enable == enable) if enable in [True, False] else query
        query = query.filter(Institution.name.icontains(name)) if name not in [None, ""] else query

        aux = db.paginate(query, page=1, per_page=per_page)


        if page > aux.pages or page < 0:
            return aux
        else:
            return db.paginate(query, page=page, per_page=per_page)


    @classmethod
    def update(klass, institution, **kwargs):
        """
        Actualiza una institución.
        """
        update_attrs = ["name", "info", "address", "location", "web", "keywords", "customer_service_hours", "contact_info"]
        attrs = { key: kwargs.get(key) for key in update_attrs }

        for attribute, value in attrs.items():
            setattr(institution, attribute, value)

        institution.updated_at = datetime.utcnow()
        db.session.commit()

        return institution


    @classmethod
    def toggle_enable(klass, institution):
        """
        Si una institución está habilitada, la deshabilita y viceversa.
        """
        institution.enable = not institution.enable
        institution.updated_at = datetime.utcnow()
        db.session.commit()

        return institution


    @classmethod
    def delete_institution(klass, institution):
        """
        Elimina una institución.
        """
        # Se eliminan los usuarios asociados a la institución
        Institution.delete_all_user_roles(institution)

        # Se eliminan los servicios asociados a la institución
        Institution.delete_all_services(institution)

        # Luego se elimina la institución
        db.session.delete(institution)
        db.session.commit()


    @classmethod
    def delete_all_user_roles(klass, institution):
        """
        Elimina todos los roles de usuarios ligados a una institución.
        """
        all_user_roles = UserRoleInstitution.query.filter_by(institution_id=institution.id).all()

        for user_role in all_user_roles:
            UserRoleInstitution.destroy(user_role)


    @classmethod
    def all_services(klass, institution):
        """
        Retorna todos los servicios ligados a una institución.
        """
        return Service.query.filter_by(institution_id=institution.id).all()


    @classmethod
    def delete_all_services(klass, institution):
        """
        Elimina todos los servicios ligados a una institución
        """
        all_services = Institution.all_services(institution)

        for service in all_services:
            Service.delete_service(service)


    @classmethod
    def is_enable(klass, institution):
        """
        Retorna `True` si una institución se encuentra habilitada.
        Caso contrario, retorna `False`.
        """
        return institution.enable
