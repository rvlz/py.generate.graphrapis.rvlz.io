import os


def get_database_uri():
    return os.environ.get("DB_URI")


def get_api_url():
    host = os.environ.get("API_HOST")
    return f"http://{host}:5000"
