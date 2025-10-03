from flask import render_template, jsonify, request

def register_error_handlers(app):
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        from models import db
        db.session.rollback()
        return render_template('500.html'), 500

    @app.errorhandler(Exception)
    def handle_exception(error):
        # Логирование ошибки
        app.logger.error(f"Произошла ошибка: {str(error)}")
        
        # Возврат JSON ответа для API запросов
        if request.is_json:
            return jsonify({
                "error": "Internal Server Error",
                "message": str(error)
            }), 500
            
        # Для обычных запросов возвращаем HTML страницу
        return render_template('error.html', error=error), 500