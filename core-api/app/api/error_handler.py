import logging
from flask import jsonify, request
from app.util.exceptions import UnexpectedServerError
import os
import json


def handle_abroad_excp(err):
    resp = json.loads(os.environ.get("JSON_RESPONSE"))
    resp["errors"] = [errors for errors in err.args]
    logging.debug({"message": resp["errors"], "err": err, "route": request.url})
    return jsonify(resp), 200


def handle_all_else(err):
    resp = json.loads(os.environ.get("JSON_RESPONSE"))
    err_info = err.__traceback__
    while err_info.tb_next is not None:
        err_info = err_info.tb_next

    logging.error(
        {
            "message": "Abroad Exception",
            "err": err,
            "route": request.url,
            "json": request.json if request.data else {},
            "line_number": err_info.tb_lineno,
            "file_path": os.path.split(err_info.tb_frame.f_code.co_filename)[1],
            "error_class": type(err).__name__,
        }
    )
    resp["errors"] = UnexpectedServerError().args
    return jsonify(resp), 500


def handle_validation_err(err):
    json_return = json.loads(os.environ.get("JSON_RESPONSE"))
    logging.error({"message": "Lacking arguments.", "err": err})
    for e in json.loads(err.json()):
        data = {"message": f"Missing parameter {e.get('loc')}" if e.get("type") == "value_error.missing" else f"Invalid parameter {e.get('loc')}", "error": "validation_error", "code": "412"}
        json_return["errors"].append(data)
    return jsonify(json_return), 200
