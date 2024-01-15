"""
Define la entidad que representa a los servicios.
"""
from datetime import datetime
from src.core.database import db
from src.core.enums.service_type import ServiceTypeEnum
from src.core.models.service_requests import ServiceRequests
from sqlalchemy import func, or_


class Service(db.Model):
    __tablename__ = "services"

    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255))
    keywords = db.Column(db.String(255))
    service_type = db.Column(db.Enum(ServiceTypeEnum, name='service_type_enum'), nullable=False)
    enable = db.Column(db.Boolean, default=False, nullable=False)
    inserted_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    institution_id = db.Column(db.Integer, db.ForeignKey('institutions.id'), nullable=False)
    institution = db.relationship('Institution', back_populates='services')

    # Restricción de unicidad: nombre
    __table_args__= (db.UniqueConstraint('name', 'institution_id', name='service_name_institution'),)


    @classmethod
    def create(klass, **kwargs):
        """
        Crea un servicio.
        """
        create_attrs = ["institution_id", "name", "service_type", "description", "keywords", "enable"]
        attrs = { key: kwargs.get(key) for key in create_attrs }

        service = Service(**attrs)

        db.session.add(service)
        db.session.commit()

        return service


    @classmethod
    def find_by(klass, **kwargs):
        """
        Retorna un servicio según el criterio de búsqueda ingresado.
        """
        search = Service.query

        if kwargs.get('name'):
            name = kwargs.pop('name')
            search = search.filter(func.replace(func.lower(Service.name), " ", "").ilike(name.replace(" ","")))

        if kwargs.get('description'):
            info = kwargs.pop('description')
            search = search.filter(Service.description.ilike(info))

        if kwargs.get('keywords'):
            keywords = kwargs.pop('keywords')
            search = search.filter(Service.keywords.ilike(keywords))

        if kwargs.get('service_type'):
            service_type = kwargs.pop('service_type')
            if service_type is not None and service_type in [item.name for item in ServiceTypeEnum]:
                search = search.filter(Service.service_type == service_type)

        return search.filter_by(**kwargs).first()


    @classmethod
    def find_all_by(klass, **kwargs):
        """
        Retorna una lista de servicios según el criterio de búsqueda ingresado.
        """
        search = Service.query

        if kwargs.get('name'):
            name = kwargs.pop('name')
            search = search.filter(func.replace(func.lower(Service.name), " ", "").ilike(name.replace(" ","")))

        if kwargs.get('description'):
            info = kwargs.pop('description')
            search = search.filter(Service.description.ilike(info))

        if kwargs.get('keywords'):
            keywords = kwargs.pop('keywords')
            search = search.filter(Service.keywords.ilike(keywords))

        if kwargs.get('service_type'):
            service_type = kwargs.pop('service_type')
            if service_type is not None and service_type in [item.name for item in ServiceTypeEnum]:
                search = search.filter(Service.service_type == service_type)

        return search.filter_by(**kwargs).all()


    @classmethod
    def search(klass, **kwargs):
        """
        Retorna una lista de servicios según el criterio de búsqueda ingresado.
        """
        # Pagination
        page = int(kwargs.get("page")) if kwargs.get("page") else 1
        per_page = int(kwargs.get("per_page")) if kwargs.get("per_page") else 25

        # Campos de búsqueda
        institution = kwargs.get("institution")
        name = kwargs.get("name")
        enable = kwargs.get("enable")
        service_type = kwargs.get("service_type")

        # Se parsea el valor de enable
        enable = None if enable not in ["true", "false"] else enable
        enable = True if enable == "true" else enable
        enable = False if enable == "false" else enable

        # Se construye la query de busqueda
        query = Service.query

        query = query.filter(Service.institution.has(id=institution.id)) if institution else query
        query = query.filter(Service.service_type == service_type) if service_type else query
        query = query.filter(Service.enable == enable) if enable in [True, False] else query
        query = query.filter(Service.name.icontains(name)) if name not in [None, ""] else query

        aux = db.paginate(query, page=1, per_page=per_page)


        if page > aux.pages or page < 0:
            return aux
        else:
            return db.paginate(query, page=page, per_page=per_page)


    @classmethod
    def update(klass, service, **kwargs):
        """
        Actualiza un servicio.
        """
        update_attrs = ["name", "description", "keywords", "service_type", "enable"]
        attrs = { key: kwargs.get(key) for key in update_attrs }

        for attribute, value in attrs.items():
            setattr(service, attribute, value)

        service.updated_at = datetime.utcnow()
        db.session.commit()

        return service


    @classmethod
    def delete_service(klass, service):
        """
        Elimina un servicio.
        """
        # Primero se cancelan las solicitudes de servicios asociadas al servicio
        Service.cancel_all_service_requests(service)

        # Luego se elimina el servicio
        db.session.delete(service)
        db.session.commit()


    @classmethod
    def cancel_all_service_requests(klass, service):
        """
        Cancela todas las solicitudes de un servicios.
        """
        # Para cada solicitud del servicio, se cambia el estado a "cancelada"
        all_service_requests = ServiceRequests.query.filter_by(service_id=service.id).all()

        for request in all_service_requests:
            ServiceRequests.override(request, service_id=service.id)


    @classmethod
    def searchApi(klass, **kwargs):
        """
        Retorna una lista de servicios según el criterio de búsqueda ingresado.
        """
        # Pagination
        page = int(kwargs.get("page")) if kwargs.get("page") else 1
        per_page = int(kwargs.get("per_page")) if kwargs.get("per_page") else 25

        # Campos de búsqueda
        q = kwargs.get("q")
        service_type = kwargs.get("service_type")

        # Se construye la query de busqueda
        query = Service.query

        query = query.filter(Service.enable == True)
        query = query.filter(Service.service_type == service_type) if service_type else query

        from src.core.models.institution import Institution
        conditions = [
            Service.name.ilike(f"{q}%"),
            Service.keywords.ilike(f"%{q}%"),
            Service.description.ilike(f"%{q}%"),
            Service.institution.has(Institution.name.ilike(f"%{q}%"))
        ]

        # Utilizar or_ para combinar las condiciones con un operador "o"
        query = query.filter(or_(*conditions)) if q not in [None, ""] else query

        aux = db.paginate(query, page=1, per_page=per_page)


        if page > aux.pages or page < 0:
            return aux
        else:
            return db.paginate(query, page=page, per_page=per_page)