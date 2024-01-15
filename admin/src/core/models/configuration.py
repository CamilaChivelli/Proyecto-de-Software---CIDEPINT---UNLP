"""
Define la entidad que representa la configuración global del sistema.
Sólo habrá una única tupla en la DB.
"""
from src.core.database import db


class Configuration(db.Model):
    __tablename__ = "configurations"

    id = db.Column(db.Integer, primary_key=True, unique=True)

    # Cantidad de elementos listados por página
    per_page = db.Column(db.Integer, default=25, nullable=False)

    # Información de contacto
    email = db.Column(db.String(50))
    phone_number = db.Column(db.String(50))
    web = db.Column(db.String(50))

    # Mantenimiento del sitio
    is_on_maintenance = db.Column(db.Boolean, default=False, nullable=False)
    maintenance_message = db.Column(db.Text)


    @classmethod
    def create(klass, **kwargs):
        """
        Crea una `Configuration`.
        """
        create_attrs = ["per_page", "email", "phone_number", "web", "is_on_maintenance", "maintenance_message"]
        attrs = { key: kwargs.get(key) for key in create_attrs }

        configuration = Configuration(**attrs)

        db.session.add(configuration)
        db.session.commit()

        return configuration


    @classmethod
    def update(klass, configuration, **kwargs):
        """
        Actualiza una `Configuration`.
        """
        update_attrs = ["per_page", "email", "phone_number", "web", "is_on_maintenance", "maintenance_message"]
        attrs = { key: kwargs.get(key) for key in update_attrs }

        for attribute, value in attrs.items():
            setattr(configuration, attribute, value)

        db.session.commit()
