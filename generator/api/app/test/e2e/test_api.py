from app.test import api_client, random_values


def test_happy_path_returns_201_and_link_created():
    ref = random_values.generate_ref()
    domain = random_values.generate_domain()
    path = random_values.generate_path()
    title = random_values.generate_title()

    response = api_client.create_link(
        ref=ref,
        domain=domain,
        path=path,
        title=title,
    )

    assert response.status_code == 201

    response = api_client.get_link(ref=ref)

    assert response.status_code == 200
    assert response.json()["ref"] == ref
    assert response.json()["domain"] == domain
    assert response.json()["path"] == path
    assert response.json()["title"] == title


def test_duplicate_refs_returns_403_and_link_not_created():
    ref = random_values.generate_ref()
    domain = random_values.generate_domain()
    path, other_path = (
        random_values.generate_path(),
        random_values.generate_path(),
    )
    title, other_title = (
        random_values.generate_title(),
        random_values.generate_title(),
    )

    response = api_client.create_link(
        ref=ref,
        domain=domain,
        path=path,
        title=title,
    )

    assert response.status_code == 201

    response = api_client.create_link(
        ref=ref,
        domain=domain,
        path=other_path,
        title=other_title,
    )

    assert response.status_code == 403
    assert response.json()["error"] == "duplicate_ref"
    assert response.json()["message"] == f'ref: "{ref}" already taken'


def test_happy_path_returns_200_and_latest_links_retrieved():
    links = [
        {
            "ref": random_values.generate_ref(),
            "domain": random_values.generate_domain(),
            "path": random_values.generate_path(),
            "title": random_values.generate_title(),
        }
        for _ in range(4)
    ]
    for link in links:
        api_client.create_link(
            ref=link["ref"],
            domain=link["domain"],
            path=link["path"],
            title=link["title"],
        )

    response = api_client.get_links(limit=3)

    results = response.json()
    assert response.status_code == 200
    assert len(results) == 3
    assert links[3] == results[0]
    assert links[2] == results[1]
    assert links[1] == results[2]


def test_happy_path_returns_201_and_bulk_create_links():
    links = [
        {
            "ref": random_values.generate_ref(),
            "domain": random_values.generate_domain(),
            "path": random_values.generate_path(),
            "title": random_values.generate_title(),
        }
        for _ in range(3)
    ]
    response = api_client.create_links(links=links)
    assert response.status_code == 201

    response = api_client.get_links(limit=3)
    results = response.json()
    assert response.status_code == 200
    assert len(results) == 3
    assert links[0] in results
    assert links[1] in results
    assert links[2] in results
