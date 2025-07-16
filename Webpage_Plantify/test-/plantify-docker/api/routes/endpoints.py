from flask import Blueprint, jsonify, current_app, request, Response
from .endpoint_configs import ENDPOINT_CONFIGS
from .services import handle_db_action

endpoints_blueprint = Blueprint('endpoint', __name__)

@endpoints_blueprint.route("/ping")
def ping():
    return jsonify({"message": "API is running!"})

@endpoints_blueprint.route("/<type>/<endpoint>", methods=["GET","POST","PATCH","DELETE"])
def dispatch(type,endpoint):
    params = (
        request.args.to_dict() if request.method == "GET"
        else request.get_json(silent=True) or {}
    )
    supported_types = {"json", "insert", "update", "delete"}

    if type not in supported_types:
        return Response("Invalid type", status=404)
    if endpoint not in ENDPOINT_CONFIGS:
        return Response("Invalid endpoint", status=404)
    config = ENDPOINT_CONFIGS[endpoint]
    expected_method = config.get("method")

    if expected_method and request.method != expected_method:
        return Response(f"{request.method} not allowed for this endpoint (expected {expected_method})", status=405)

    return handle_db_action(endpoint, params, type)





