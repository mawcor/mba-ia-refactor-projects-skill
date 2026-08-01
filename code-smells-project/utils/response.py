from flask import jsonify
from http import HTTPStatus

def success_response(data=None, message=None, status=HTTPStatus.OK):
    response = {"sucesso": True}
    if data is not None:
        response["dados"] = data
    if message is not None:
        response["mensagem"] = message
    return jsonify(response), status

def error_response(message, status=HTTPStatus.INTERNAL_SERVER_ERROR):
    return jsonify({"erro": message, "sucesso": False}), status
