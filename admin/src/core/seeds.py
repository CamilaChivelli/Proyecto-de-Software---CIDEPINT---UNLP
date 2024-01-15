"""
Este módulo se encarga de la carga de datos a la base de datos.
"""
from faker import Faker
from faker.providers import person, internet, misc
from src.core.enums.service_type import ServiceTypeEnum
from src.core.enums.status import StatusEnum
from src.core.models.user import User
from src.core.models.institution import Institution
from src.core.models.service import Service
from src.core.models.service_requests import ServiceRequests
from src.core.models.configuration import Configuration
from src.core.models.user_has_role import UserRoleInstitution
from src.core.models.configuration import Configuration
from src.core.models.permission import Permission
from src.core.models.role import Role
from src.core.models.role_has_permission import RolePermission


fake = Faker()

for provider in (person, internet, misc):
    fake.add_provider(provider)


def run():
    __create_configuration()
    __create_roles()
    __create_permissions()
    __create_users()
    __create_institutions()
    __create_user_role_institution()
    __create_services()
    __create_service_requests()
    __link_roles_and_permissions()


def __create_configuration():
    configuration_data = {
        "email": "grupo09@info.edu.unlp.ar",
        "phone_number": "(221) 123-4567",
        "web": "https://grupo09.info.edu.unlp.ar",
        "maintenance_message": "El sitio se encuentra bajo mantenimiento."
    }

    Configuration.create(**configuration_data)


def __create_roles():
    roles_data = [
        {"name": "super_administrador"},
        {"name": "dueno"},
        {"name": "administrador"},
        {"name": "operador"}
    ]

    for role_data in roles_data:
        Role.create(**role_data)


def __create_permissions():
    permissions_data = [
        # /users
        {"name": "users_index"},
        {"name": "users_show"},
        {"name": "users_new"},
        {"name": "users_create"},
        {"name": "users_edit"},
        {"name": "users_update"},
        {"name": "users_destroy"},
        # /configurations
        {"name": "configurations_show"},
        {"name": "configurations_edit"},
        {"name": "configurations_update"},
        # /institutions
        {"name": "institutions_index"},
        {"name": "institutions_show"},
        {"name": "institutions_edit"},
        {"name": "institutions_update"},
        {"name": "institutions_new"},
        {"name": "institutions_create"},
        {"name": "institutions_destroy"},
        {"name": "institutions_activate"},
        {"name": "institutions_deactivate"},
        # /services
        {"name": "services_index"},
        {"name": "services_show"},
        {"name": "services_new"},
        {"name": "services_create"},
        {"name": "services_edit"},
        {"name": "services_update"},
        {"name": "services_destroy"},
        # /service_requests
        {"name": "service_requests_index"},
        {"name": "service_requests_show"},
        {"name": "service_requests_new"},
        {"name": "service_requests_create"},
        {"name": "service_requests_edit"},
        {"name": "service_requests_update"},
        {"name": "service_requests_destroy"},
        # /institution_users
        {"name": "institution_users_index"},
        {"name": "institution_users_new"},
        {"name": "institution_users_create"},
        {"name": "institution_users_edit"},
        {"name": "institution_users_update"},
        {"name": "institution_users_destroy"}
    ]

    for permission_data in permissions_data:
        Permission.create(**permission_data)


def __create_admin_users():
    role_names = ["super_administrador", "dueno", "administrador", "operador"]

    for role_name in role_names:
        User.create(
            email=f"{role_name}@mail.com",
            password="password",
            active=True,
            firstname=role_name.upper()
        )


def __create_standard_users():
    for _ in range(30):
        User.create(
            email=fake.ascii_email(),
            password="password",
            active=fake.boolean(),
            firstname=fake.first_name(),
            lastname=fake.last_name()
        )


def __create_users():
    __create_admin_users()
    __create_standard_users()


def __create_institutions():
    _address = "-34.92224923830229,-57.95296673328499"

    Institution.create(
        name="CONICET",
        info="El Consejo Nacional de Investigaciones Científicas y Técnicas es el principal organismo dedicado a la promoción de la ciencia y la tecnología en Argentina, dependiente del Ministerio de Ciencia, Tecnología e Innovación de la Nación",
        address=_address,
        location="Ciudad Autónoma de Buenos Aires",
        web="https://www.conicet.gov.ar",
        keywords="investigación, ciencia",
        customer_service_hours="Lunes a Viernes, 9 AM - 1 PM",
        contact_info="correointranet@conicet.gov.ar",
        enable=True
    )

    for _ in range(10):
        Institution.create(
            name = fake.company(),
            info = fake.catch_phrase(),
            address = _address,
            location = fake.address(),
            web = fake.url(),
            keywords = fake.words(nb=5),
            customer_service_hours = fake.random_element(elements=("9 AM - 5 PM", "10 AM - 6 PM", "8 AM - 4 PM")),
            contact_info = fake.email(),
            enable = fake.boolean(chance_of_getting_true=80)
        )


def __create_services():
    institutions = Institution.query.all()

    for _ in range(30):
        institution = fake.random_element(elements=institutions)

        Service.create(
            name=fake.lexify(text="??????????", letters="ABCDE"),
            description=fake.sentence(nb_words=10),
            keywords=fake.words(nb=5),
            enable=fake.boolean(chance_of_getting_true=80),
            service_type=fake.random_element(elements=ServiceTypeEnum),
            institution_id=institution.id
        )


def __create_user_role_institution():
    user_role_institution_list = [
        {"user_id": 1, "role_id": 1, "institution_id": None},
        {"user_id": 2, "role_id": 2, "institution_id": 1},
        {"user_id": 3, "role_id": 3, "institution_id": 1},
        {"user_id": 4, "role_id": 4, "institution_id": 1}
    ]

    for user_role_institution in user_role_institution_list:
        UserRoleInstitution.create(**user_role_institution)

    users = User.query.filter(User.id != 1).all()
    roles = Role.query.filter(Role.id != 1).all()
    institutions = Institution.query.filter(Institution.id != 1).all()

    for _ in range(30):
        user = fake.random_element(elements=users)
        role = fake.random_element(elements=roles)
        institution = fake.random_element(elements=institutions)

        user_role_institution = UserRoleInstitution.query.filter_by(
            user_id=user.id, institution_id=institution.id
        ).first()

        if not user_role_institution:
            UserRoleInstitution.create(
                user_id=user.id,
                role_id=role.id,
                institution_id=institution.id
            )


def __create_service_requests():
    users = User.query.all()
    services = Service.query.all()

    for _ in range(30):
        user = fake.random_element(elements=users)
        service = fake.random_element(elements=services)

        service_request = ServiceRequests.query.filter_by(user_id=user.id, service_id=service.id).first()

        if not service_request:
            ServiceRequests.create(
                service_id=service.id,
                user_id=user.id,
                status = fake.random_element(elements=StatusEnum)
            )


def __link_roles_and_permissions():
    rol_super_administrador = Role.find_by(name="super_administrador")
    rol_dueno = Role.find_by(name="dueno")
    rol_administrador = Role.find_by(name="administrador")
    rol_operador = Role.find_by(name="operador")

    roles_has_permissions = [
        # /users
        {"permission_id": 1, "role_id": rol_super_administrador.id}, # index
        {"permission_id": 2, "role_id": rol_super_administrador.id}, # show
        {"permission_id": 3, "role_id": rol_super_administrador.id}, # new
        {"permission_id": 4, "role_id": rol_super_administrador.id}, # create
        {"permission_id": 5, "role_id": rol_super_administrador.id}, # edit
        {"permission_id": 6, "role_id": rol_super_administrador.id}, # update
        {"permission_id": 7, "role_id": rol_super_administrador.id}, # destroy

        # /configurations
        {"permission_id": 8, "role_id": rol_super_administrador.id},  # show
        {"permission_id": 9, "role_id": rol_super_administrador.id},  # edit
        {"permission_id": 10, "role_id": rol_super_administrador.id}, # update

        # /institutions
        {"permission_id": 11, "role_id": rol_super_administrador.id}, # index
        {"permission_id": 12, "role_id": rol_super_administrador.id}, # show
        {"permission_id": 13, "role_id": rol_super_administrador.id}, # edit
        {"permission_id": 14, "role_id": rol_super_administrador.id}, # update
        {"permission_id": 15, "role_id": rol_super_administrador.id}, # new
        {"permission_id": 16, "role_id": rol_super_administrador.id}, # create
        {"permission_id": 17, "role_id": rol_super_administrador.id}, # destroy
        {"permission_id": 18, "role_id": rol_super_administrador.id}, # activate
        {"permission_id": 19, "role_id": rol_super_administrador.id}, # deactivate

        # /services - index
        {"permission_id": 20, "role_id": rol_dueno.id},
        {"permission_id": 20, "role_id": rol_administrador.id},
        {"permission_id": 20, "role_id": rol_operador.id},

        # /services - show
        {"permission_id": 21, "role_id": rol_dueno.id},
        {"permission_id": 21, "role_id": rol_administrador.id},
        {"permission_id": 21, "role_id": rol_operador.id},

        # /services - new
        {"permission_id": 22, "role_id": rol_dueno.id},
        {"permission_id": 22, "role_id": rol_administrador.id},
        {"permission_id": 22, "role_id": rol_operador.id},

        # /services - create
        {"permission_id": 23, "role_id": rol_dueno.id},
        {"permission_id": 23, "role_id": rol_administrador.id},
        {"permission_id": 23, "role_id": rol_operador.id},

        # /services - edit
        {"permission_id": 24, "role_id": rol_dueno.id},
        {"permission_id": 24, "role_id": rol_administrador.id},
        {"permission_id": 24, "role_id": rol_operador.id},

        # /services - update
        {"permission_id": 25, "role_id": rol_dueno.id},
        {"permission_id": 25, "role_id": rol_administrador.id},
        {"permission_id": 25, "role_id": rol_operador.id},

        # /services - destroy
        {"permission_id": 26, "role_id": rol_dueno.id},
        {"permission_id": 26, "role_id": rol_administrador.id},

        # /service_requests - index
        {"permission_id": 27, "role_id": rol_dueno.id},
        {"permission_id": 27, "role_id": rol_administrador.id},
        {"permission_id": 27, "role_id": rol_operador.id},

        # /service_requests - show
        {"permission_id": 28, "role_id": rol_dueno.id},
        {"permission_id": 28, "role_id": rol_administrador.id},
        {"permission_id": 28, "role_id": rol_operador.id},

        # /service_requests - new
        # {"permission_id": 29, "role_id": rol_dueno.id},
        # {"permission_id": 29, "role_id": rol_administrador.id},
        # {"permission_id": 29, "role_id": rol_operador.id},
        # /service_requests - create
        # {"permission_id": 30, "role_id": rol_dueno.id},
        # {"permission_id": 30, "role_id": rol_administrador.id},
        # {"permission_id": 30, "role_id": rol_operador.id},

        # /service_requests - edit
        {"permission_id": 31, "role_id": rol_dueno.id},
        {"permission_id": 31, "role_id": rol_administrador.id},
        {"permission_id": 31, "role_id": rol_operador.id},

        # /service_requests - update
        {"permission_id": 32, "role_id": rol_dueno.id},
        {"permission_id": 32, "role_id": rol_administrador.id},
        {"permission_id": 32, "role_id": rol_operador.id},

        # /service_requests - destroy
        {"permission_id": 33, "role_id": rol_dueno.id},
        {"permission_id": 33, "role_id": rol_administrador.id},

        # /institution_users
        {"permission_id": 34, "role_id": rol_dueno.id}, # index
        {"permission_id": 35, "role_id": rol_dueno.id}, # new
        {"permission_id": 36, "role_id": rol_dueno.id}, # create
        {"permission_id": 37, "role_id": rol_dueno.id}, # edit
        {"permission_id": 38, "role_id": rol_dueno.id}, # update
        {"permission_id": 39, "role_id": rol_dueno.id}, # destroy
    ]

    for permission in roles_has_permissions:
        RolePermission.create(**permission)
