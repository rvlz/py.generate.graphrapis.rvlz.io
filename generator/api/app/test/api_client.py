import requests

from app.test import config


def create_link(ref: str, domain: str, path: str, title: str):
    base_url = config.get_api_url()
    return requests.post(
        f"{base_url}/link",
        json={
            "ref": ref,
            "domain": domain,
            "path": path,
            "title": title,
        },
    )


def create_links(links):
    url = config.get_api_url()
    return requests.post(
        f"{url}/link",
        json=links,
    )


def get_link(ref: str):
    url = config.get_api_url()
    return requests.get(f"{url}/link/{ref}")


def get_links(limit: int):
    url = config.get_api_url()
    return requests.get(f"{url}/link?limit={limit}")


def update_link(ref: str, updates):
    url = config.get_api_url()
    return requests.patch(
        f"{url}/link/{ref}",
        json=updates,
    )


def delete_link(ref: str):
    url = config.get_api_url()
    return requests.delete(f"{url}/link/{ref}")
