import uuid


def generate_suffix():
    return uuid.uuid4().hex[:8]


def generate_domain():
    return f"{generate_suffix()}-domain.com"


def generate_path():
    return f"path/{generate_suffix()}"


def generate_ref():
    return f"ref-{generate_suffix()}"


def generate_title():
    return f"Intro to {generate_suffix()}"
