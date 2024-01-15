"""
Define la entidad que representa a un permiso.
"""
from src.core.database import db


class Permission(db.Model):
    __tablename__ = "permissions"

    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(255), unique=True, nullable=False)


    @classmethod
    def create(klass, **kwargs):
        """
        Crea un permiso.
        """
        create_attrs = ["name"]
        attrs = { key: kwargs.get(key) for key in create_attrs }

        permission = Permission(**attrs)

        db.session.add(permission)
        db.session.commit()

        return permission
