"""
Define la entidad que representa a la tabla intermedia entre roles y permisos.
"""
from src.core.database import db
from src.core.models.role import Role
from src.core.models.permission import Permission


class RolePermission(db.Model):
    __tablename__ = "role_has_permission"

    id = db.Column(db.Integer, primary_key=True, unique=True)

    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    role = db.relationship('Role', backref='role_has_permission')

    permission_id = db.Column(db.Integer, db.ForeignKey('permissions.id'))
    permission = db.relationship('Permission', backref='role_has_permission')

    # Restricción de unicidad: rol - permiso
    __table_args__ = (db.UniqueConstraint('role_id', 'permission_id', name='user_service_request'),)


    def get_permissions_by_role(role_id):
        """
        Retorna la lista de instituciones y sus roles de un usuario.
        """
        return RolePermission.query.filter_by(role_id=role_id).all()


    def list_available_permissions(role):
        """
        Retorna una lista con los nombres de los permisos en base a un rol dado.
        """
        if role is None:
            return []

        query = db.select(
            Permission.name
            ).join(
                RolePermission,
                RolePermission.permission_id == Permission.id
            ).filter(
                RolePermission.role_id == role.id
            )

        return db.session.execute(query).scalars().all()


    @classmethod
    def has_permission(klass, role, required_permission_list):
        """
        Retorna `True` si todos los permisos se encuentran disponibles para un rol dado.
        """
        available_permissions = klass.list_available_permissions(role)

        if available_permissions is None:
            return False

        has_permission = True

        for required_permission in required_permission_list:
            if required_permission not in available_permissions:
                has_permission = False
                break

        return has_permission


    @classmethod
    def create(klass, **kwargs):
        """
        Crea una tupla role_permission.
        Retorna un rol.
        """
        role = Role.query.get(kwargs.get('role_id'))
        permission = Permission.query.get(kwargs.get('permission_id'))

        if role and permission:
            role_permission = RolePermission(**kwargs)

            db.session.add(role_permission)
            db.session.commit()

        else:
            pass

        return role
