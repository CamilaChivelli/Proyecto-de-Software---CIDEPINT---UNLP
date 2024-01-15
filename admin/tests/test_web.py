from src.web import create_app


app = create_app()
app.testing = True
client = app.test_client()


def test_web():
	response = client.get("/")
