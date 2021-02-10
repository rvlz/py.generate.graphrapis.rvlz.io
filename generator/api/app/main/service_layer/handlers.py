from app.main.service_layer import unit_of_work
from app.main.domain import commands, model


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
            link.delete()
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
                            deleted=ln["deleted"],
                        ),
                    ]
                )
            self.uow.commit()


EVENT_HANDLERS = {}

COMMAND_HANDLERS = {
    commands.RegisterLink: RegisterLinkHandler,
    commands.DeregisterLink: DeregisterLinkHandler,
    commands.BulkRegisterLinks: BulkRegisterLinksHandler,
}
