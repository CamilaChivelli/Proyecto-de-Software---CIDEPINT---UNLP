# Admin

## Stack

- Servidor de Base de Datos: Postgres 15
- Intérprete Python: Python 3.8.10
- Servidor web: Nginx 1.18.0-0ubuntu1.3

## Setup

1. Clonar el repositorio.

2. Posicionarse en el directorio `/admin` y correr en la terminal el comando:

```sh
poetry install
```

3. Crear dentro del directorio `/admin` un archivo `.env` con el siguiente contenido:

```
# Database
export PDS_DB_USER="postgres"
export PDS_DB_PASS="postgres"
export PDS_DB_HOST="localhost"
export PDS_DB_NAME="grupo09"

# Flask mail
export MAIL_USERNAME='leafcompanysoftware@gmail.com'
export MAIL_PASSWORD='dgijsifzwvpiprvq'
```

Nota: Si tus credenciales son distintas, sólo basta con reemplazarlas en el `.env`.

Luego, cargamos las variables de entorno en nuestra `shell` corriendo en la terminal el siguiente comando:

```sh
source .env
```

4. Crear una nueva DB en Postgres con el mismo nombre definido en la variable de entorno `PDS_DB_NAME`.

5. Abrimos la shell de Poetry para no tener que anteponer `$ poetry run` ante cada comando:

```sh
poetry shell
```

6. Resetear la DB corriendo el siguiente comando:

```sh
flask reset_db
```

7. Una vez que se hizo el reset correctamente, cargar la información del `seeds`:

```sh
flask seed_db
```

8. Correr la aplicación:

```sh
flask run --cert adhoc
```

Notas:
  - No hace falta utilizar el parametro `--debug` ya que la aplicación está configurada para correr en ese modo (ver `DevelopmentConfig(Config)` en `config.py`).
  - En el caso de que el puerto por defecto se encuentre siendo utilizado (`5000`), se puede especificar que use otro: `$ flask run -p 5001`.

--------------------------------------------------

## Usuarios

Todos los usuarios tienen como password la palabra `password`:

- `super_adminitrador@mail.com`
- `dueno@mail.com`
- `administrador@mail.com`
- `operador@mail.com`

Los usuarios `dueno`, `administrador` y `operador` tienen asignados la institución `CONICET`.