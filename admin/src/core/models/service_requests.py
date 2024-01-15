"""
Define la entidad que representa a las solicitudes de servicio.
"""
import calendar
from datetime import datetime
import locale
from flask import g
from sqlalchemy import extract, func, or_, text
from src.core.enums.service_type import ServiceTypeEnum
from src.core.enums.status import StatusEnum
from src.core.models.user import User
from src.core.database import db
from sqlalchemy.orm import joinedload


class ServiceRequests(db.Model):
    __tablename__ = "service_requests"

    id = db.Column(db.Integer, primary_key=True, unique=True)
    user_observation = db.Column(db.Text, default="")
    institution_observation = db.Column(db.Text, default="")
    status = db.Column(db.Enum(StatusEnum), default=StatusEnum.EN_PROGRESO)
    file_path = db.Column(db.String(255))
    inserted_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=True)
    service = db.relationship('Service', backref='service_requests')

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    user = db.relationship('User', backref='service_requests')

    # Restricción de unicidad: usuario - servicio
    # __table_args__= (db.UniqueConstraint('user_id', 'service_id', name='user_request'),)


    @classmethod
    def search(klass, **kwargs):
        """
        Retorna una lista de solicitudes de servicio según el criterio de búsqueda ingresado.
        """
        # Pagination
        page = int(kwargs.get("page")) if kwargs.get("page") else 1
        per_page = kwargs.get("per_page")

        # Campos de búsqueda
        user = kwargs.get("user")
        service_type = kwargs.get("service_type")
        status = kwargs.get("status")
        service_id = kwargs.get("service_id")
        date_start = kwargs.get("date_start")
        date_end = kwargs.get("date_end")
        institution_id = g.current_institution.id

        # Se construye la query de búsqueda
        query = ServiceRequests.query

        if institution_id:
            query = query.filter(ServiceRequests.service.has(institution_id=institution_id))

        if service_type is not None and service_type in [item.name for item in ServiceTypeEnum]:
            query = query.filter(ServiceRequests.service.has(service_type=service_type))

        if status is not None and status in [item.name for item in StatusEnum]:
            query = query.filter(ServiceRequests.status == status)

        if user:
            query = query.filter(or_(
                ServiceRequests.user.has(User.firstname.ilike(f"{user}%")),
                ServiceRequests.user.has(User.lastname.ilike(f"{user}%"))
            ))

        if service_id:
            query = query.filter(ServiceRequests.service.has(id=service_id))

        if date_start and date_end:
            query = query.filter(ServiceRequests.inserted_at.between(date_start, date_end))

        aux = db.paginate(query, page=1, per_page=per_page)


        if page > aux.pages or page < 0:
            return aux
        else:
            return db.paginate(query, page=page, per_page=per_page)

    @classmethod
    def find_by(klass, **kwargs):
        """
        Retorna una solicitud de servicio según el criterio de búsqueda ingresado.
        """
        institution_id = kwargs.pop('institution_id', None)

        query = ServiceRequests.query.filter_by(**kwargs)
        query = query.filter(ServiceRequests.service.has(institution_id=institution_id)) if institution_id else query

        return query.first()


    @classmethod
    def search_by_user_api(klass, **kwargs):
        """
        Retorna una lista de solicitudes de servicio según el criterio de búsqueda ingresado.
        """
        # Pagination
        page = int(kwargs.get("page")) if kwargs.get("page") else 1
        per_page = kwargs.get("per_page")
        sort = kwargs.get("sort")
        order = kwargs.get("order")

        # Campos de búsqueda
        user_id = kwargs.get("user_id")
        field_to_sort = getattr(ServiceRequests, sort, None)
        status = kwargs.get("status")
        date_start = kwargs.get("date_start")
        date_end = kwargs.get("date_end")

        # Se construye la query de búsqueda
        query = (
        ServiceRequests.query
        .join(ServiceRequests.service.property.mapper.class_)
        .options(joinedload(ServiceRequests.service))
        )

        query = query.filter(ServiceRequests.user.has(id=user_id))

        if order == "asc":
            query = query.order_by(field_to_sort.asc())
        else:
            query = query.order_by(field_to_sort.desc())

        if status is not None and status in [item.name for item in StatusEnum]:
            query = query.filter(ServiceRequests.status == status)

        if date_start and not date_end:
            date_end = datetime.utcnow()
            query = query.filter(ServiceRequests.inserted_at.between(date_start, date_end))

        if date_end and not date_start:
            date_start = datetime(1900, 1, 1)
            query = query.filter(ServiceRequests.inserted_at.between(date_start, date_end))

        if date_start and date_end:
            query = query.filter(ServiceRequests.inserted_at.between(date_start, date_end))


        aux = db.paginate(query, page=1, per_page=per_page)


        if page > aux.pages or page < 0:
            return aux
        else:
            return db.paginate(query, page=page, per_page=per_page)


    @classmethod
    def search_by_id_api(klass, id):
        """
        Retorna una solicitud de servicio según el criterio de búsqueda ingresado.
        """
        return ServiceRequests.query.filter_by(id=id).first()


    @classmethod
    def search_by_id_and_filters(klass, **kwargs):
        """
        Retorna una lista de solicitudes de servicio según el criterio de búsqueda ingresado.
        """
        # Pagination
        page = int(kwargs.get("page")) if kwargs.get("page") else 1
        per_page = kwargs.get("per_page")

        # Campos de búsqueda
        firstname = kwargs.get("firstname")
        lastname = kwargs.get("lastname")
        service_type = kwargs.get("service_type")
        status = kwargs.get("status")

        date_start = kwargs.get("date_start")
        date_end = kwargs.get("date_end")

        # Se construye la query de búsqueda
        query = ServiceRequests.query

        if (g.current_role.id != 1):
         query = query.filter(ServiceRequests.service.has(institution_id=g.current_institution.id))

        if service_type is not None and service_type in [item.name for item in ServiceTypeEnum]:
            query = query.filter(ServiceRequests.service.has(service_type=service_type))

        if status is not None and status in [item.name for item in StatusEnum]:
            query = query.filter(ServiceRequests.status == status)

        if firstname:
            query = query.filter(ServiceRequests.user.has((User.firstname.ilike(f"{firstname}%"))))

        if lastname:
            query = query.filter(ServiceRequests.user.has((User.lastname.ilike(f"{lastname}%"))))

        if date_start and date_end:
            query = query.filter(ServiceRequests.inserted_at.between(date_start, date_end))

        aux = db.paginate(query, page=1, per_page=per_page)


        if page > aux.pages or page < 0:
            return aux
        else:
            return db.paginate(query, page=page, per_page=per_page)


    @classmethod
    def create(klass, **kwargs):
        """
        Crea una solicitud de servicio.
        """
        create_attrs = ["service_id", "user_id", "user_observation", "file_path", "status"]
        attrs = { key: kwargs.get(key) for key in create_attrs }

        request = ServiceRequests(**attrs)

        db.session.add(request)
        db.session.commit()

        return request


    @classmethod
    def update(klass, service_requests, **kwargs):
        """
        Actualiza una solicitud de servicio.
        """
        update_attrs = ["status", "user_observation", "institution_observation"]
        attrs = { key: kwargs.get(key) for key in update_attrs }

        if attrs["user_observation"] is None:
            attrs["user_observation"] = service_requests.user_observation

        if attrs["institution_observation"] is None:
            attrs["institution_observation"] = service_requests.institution_observation

        if attrs["status"] is None:
            attrs["status"] = service_requests.status

        for attribute, value in attrs.items():
            setattr(service_requests, attribute, value)

        service_requests.updated_at = datetime.utcnow()

        db.session.commit()

        return service_requests


    @classmethod
    def change_status(klass, service_request, new_status):
        """
        Cambia el estado de la solicitud de servicio.
        """
        service_request.status = new_status

        service_request.updated_at = datetime.utcnow()
        db.session.commit()

        return service_request

    @classmethod
    def override(klass, service_request, **kwargs):
        """
        Sobreescribe una solicitud de servicio.
        """
        if kwargs.get('user_id'):
            service_request.user_id = None
            service_request.user = None

        if kwargs.get('service_id'):
            service_request.institution_observation = f"El servicio '{service_request.service.name}' ha sido eliminado por la institución '{service_request.service.institution.name}'"
            service_request.service_id = None
            service_request.service = None

        ServiceRequests.change_status(service_request, StatusEnum.CANCELADA)

        if service_request.service_id is None and service_request.user_id is None:
            ServiceRequests.delete(service_request)


    @classmethod
    def delete(klass, service_request):
        """
        Elimina una solicitud de servicio.
        """
        db.session.delete(service_request)
        db.session.commit()

    @classmethod
    def get_service_ranking(cls):
        # Consulta para obtener un ranking de servicios más solicitados
        sql_query = """
            SELECT s.name, COUNT(sr.service_id) AS count
            FROM service_requests sr
            JOIN services s ON sr.service_id = s.id
            GROUP BY s.name
            ORDER BY s.name DESC;
        """

        result = db.session.execute(text(sql_query)).fetchall()
        return result

    @classmethod
    def get_status_ranking(cls):
        sql_query = """
            SELECT status, COUNT(status) as count
            FROM service_requests
            GROUP BY status
            ORDER BY count DESC
        """

        result = db.session.execute(text(sql_query)).fetchall()
        return result

    @classmethod
    def get_monthly_ranking(cls):
        # Establecer la localización a español
        current_year = func.extract('year', func.current_date())

        # Consulta para obtener los meses con la cantidad de solicitudes
        result = (
            db.session.query(
                extract('month', ServiceRequests.inserted_at).label('month'),
                func.count().label('request_count')
            )
            .filter(extract('year', ServiceRequests.inserted_at) == current_year)
            .group_by('month')
            .all()
        )

        # Crear un diccionario con los resultados de la consulta
        result_dict = {record.month: record.request_count for record in result}

        # Crear una lista de todos los meses posibles
        all_months = list(range(1, 13))

        # Llenar la lista con los resultados de la consulta o cero si no hay solicitudes
        formatted_result = {calendar.month_name[month].capitalize():result_dict.get(month, 0) for month in all_months}

        return formatted_result