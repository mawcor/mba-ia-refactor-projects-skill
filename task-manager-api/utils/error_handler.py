from flask import jsonify

class APIError(Exception):
    def __init__(self, message, status_code=400):
        super().__init__()
        self.message = message
        self.status_code = status_code

def register_error_handlers(app):
    @app.errorhandler(APIError)
    def handle_api_error(e):
        return jsonify({'error': e.message}), e.status_code

    @app.errorhandler(Exception)
    def handle_generic_error(e):
        app.logger.error(f"Erro interno: {str(e)}")
        return jsonify({'error': 'Erro interno'}), 500
    
    @app.errorhandler(404)
    def not_found_error(e):
        return jsonify({'error': 'Recurso não encontrado'}), 404
