from app.main.service_layer import unit_of_work
from app.main.domain import commands, events, model


class RegisterLinkHandler:
    def __init__(self, uow: unit_of_work.AbstractUnitOfWork):
        self.uow = uow

    def __call__(self, cmd: commands.RegisterLink):
        with self.uow:
            website = self.uow.websites.get(domain=cmd.domain)
            if website is None:
                website = model.Website(domain=cmd.domain)
                self.uow.websites.add(website)
            website.register(
                [
                    model.Link(
                        ref=cmd.ref,
                        domain=cmd.domain,
                        path=cmd.path,
                        title=cmd.title,
                    ),
                ]
            )
            self.uow.websites.add(website)
            self.uow.commit()


class DeregisterLinkHandler:
    def __init__(self, uow: unit_of_work.AbstractUnitOfWork):
        self.uow = uow

    def __call__(self, cmd: commands.DeregisterLink):
        with self.uow:
            website = self.uow.websites.get_by_linkref(cmd.ref)
            link = website.find(cmd.ref)
            link.deactivate()
            self.uow.commit()


class BulkRegisterLinksHandler:
    def __init__(self, uow: unit_of_work.AbstractUnitOfWork):
        self.uow = uow

    def __call__(self, cmd: commands.BulkRegisterLinks):
        with self.uow:
            for ln in cmd.links:
                website = self.uow.websites.get(domain=ln["domain"])
                if website is None:
                    website = model.Website(domain=ln["domain"])
                    self.uow.websites.add(website)
                website.register(
                    [
                        model.Link(
                            ref=ln["ref"],
                            domain=ln["domain"],
                            path=ln["path"],
                            title=ln["title"],
                            active=ln["active"],
                        ),
                    ]
                )
            self.uow.commit()


class AddLinkToReadModelHandler:
    def __init__(self, uow: unit_of_work.SqlAlchemyUnitOfWork):
        self.uow = uow

    def __call__(self, event: events.LinkRegistered):
        with self.uow:
            self.uow.session.execute(
                "INSERT INTO link_view (ref, domain, path, title, active, "
                "created_at) VALUES (:ref, :domain, :path, :title, :active, "
                "current_timestamp)",
                dict(
                    ref=event.ref,
                    domain=event.domain,
                    path=event.path,
                    title=event.title,
                    active=event.active,
                ),
            )
            self.uow.commit()


EVENT_HANDLERS = {
    events.LinkRegistered: [AddLinkToReadModelHandler],
}

COMMAND_HANDLERS = {
    commands.RegisterLink: RegisterLinkHandler,
    commands.DeregisterLink: DeregisterLinkHandler,
    commands.BulkRegisterLinks: BulkRegisterLinksHandler,
}
