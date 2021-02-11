from flask import Flask, g, request, jsonify

from app.main.service_layer import message_bus, errors
from app.main import views
from app.main.domain import commands


def generate_app_factory(bus: message_bus.MessageBus):
    def create_app():
        app = Flask(__name__)

        @app.before_request
        def set_message_bus():
            g.bus = bus

        @app.route("/ping", methods=["GET"])
        def _ping():
            return "ping"

        @app.route("/link/<ref>", methods=["GET"])
        def _get_link(ref):
            result = views.link(ref, g.bus.uow)
            return jsonify(result), 200

        @app.route("/link", methods=["GET"])
        def _get_links():
            limit = request.args.get("limit")
            results = views.latest_links(limit, g.bus.uow)
            return jsonify(results), 200

        @app.route("/link", methods=["POST"])
        def _create_link():
            cmd = None
            try:
                if isinstance(request.json, list):
                    cmd = commands.BulkRegisterLinks(links=request.json)
                else:
                    cmd = commands.RegisterLink(
                        ref=request.json["ref"],
                        domain=request.json["domain"],
                        path=request.json["path"],
                        title=request.json["title"],
                        active=request.json["active"],
                    )
                g.bus.handle(cmd)
            except errors.DuplicateFieldError as exc:
                return (
                    jsonify(
                        {
                            "error": "duplicate_ref",
                            "message": (
                                f'{exc.field}: "{exc.value}" already taken'
                            ),
                        }
                    ),
                    403,
                )
            return "OK", 201

        return app

    return create_app
