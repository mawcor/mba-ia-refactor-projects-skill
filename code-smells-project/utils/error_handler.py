from utils.response import error_response
from http import HTTPStatus

def register_error_handlers(app):
    @app.errorhandler(Exception)
    def handle_exception(e):
        return error_response(str(e), HTTPStatus.INTERNAL_SERVER_ERROR)
    
    @app.errorhandler(404)
    def not_found(e):
        return error_response("Recurso não encontrado", HTTPStatus.NOT_FOUND)
    
    @app.errorhandler(400)
    def bad_request(e):
        return error_response("Requisição inválida", HTTPStatus.BAD_REQUEST)
