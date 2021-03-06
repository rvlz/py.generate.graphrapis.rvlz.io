from app.main.service_layer import unit_of_work


def link(ref: str, uow: unit_of_work.SqlAlchemyUnitOfWork):
    with uow:
        results = list(
            uow.session.execute(
                "SELECT ref, domain, path, title FROM link_view "
                "WHERE ref = :ref AND active is TRUE",
                dict(ref=ref),
            )
        )
    if results:
        return dict(results[0])
    return {}


def latest_links(limit: int, uow: unit_of_work.SqlAlchemyUnitOfWork):
    with uow:
        results = list(
            uow.session.execute(
                "SELECT ref, domain, path, title FROM link_view WHERE "
                "created_at IS NOT NULL AND active is TRUE ORDER BY "
                "created_at DESC LIMIT :limit",
                dict(limit=limit),
            )
        )
    return [dict(r) for r in results]
