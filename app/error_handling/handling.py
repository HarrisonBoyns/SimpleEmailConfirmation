from marshmallow import ValidationError


def register_error_handling(app):
    @app.errorhandler(ValidationError)
    def validation_error(error):
        return {
                   "message": "validation error occured",
                   "error": error.messages
               }, 400
