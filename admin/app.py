"""
Punto de entrada para correr la aplicación localmente.
"""
from src.web import create_app


app = create_app()


if __name__ == "__main__":
    app.run(ssl_context="adhoc")
