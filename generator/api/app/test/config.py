import os


def get_database_uri(integration=True):
    return os.environ.get("TEST_DB_URI")


def get_api_url():
    host = os.environ.get("TEST_API_HOST")
    return f"http://{host}:5000"
