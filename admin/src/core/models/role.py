"""
Define la entidad que representa a un rol.
"""
from src.core.database import db


class Role(db.Model):
    __tablename__ = "roles"

    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(255), unique=True, nullable=False)

    SUPER_ADMINISTRADOR="super_administrador"


    def is_super_administrador(self):
        """
        Retorna `True` si el nombre del rol actual corresponde a `super_administrador`.
        Caso contrario, retorna `False`.
        """
        return self.name == self.SUPER_ADMINISTRADOR


    @classmethod
    def list_selectable_roles(klass):
        """
        Lista los roles que pueden ser asignados a otros usuarios.
        """
        selectable_roles = klass.query.filter(klass.name != klass.SUPER_ADMINISTRADOR).all()
        return [(role.id, role.name.capitalize()) for role in selectable_roles]


    @classmethod
    def create(klass, **kwargs):
        """
        Crea un rol.
        """
        create_attrs = ["name"]
        attrs = { key: kwargs.get(key) for key in create_attrs }

        role = Role(**attrs)

        db.session.add(role)
        db.session.commit()

        return role


    @classmethod
    def find_by(klass, **kwargs):
        """
        Retorna un rol según el criterio de búsqueda ingresado.
        """
        return Role.query.filter_by(**kwargs).first()
