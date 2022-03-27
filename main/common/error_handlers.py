from .exceptions import BaseError, InternalServerError, MethodNotAllowed, NotFound


def register_error_handlers(app):
    @app.errorhandler(404)
    def not_found(_):
        return NotFound().to_response()

    @app.errorhandler(405)
    def not_allowed(_):
        return MethodNotAllowed().to_response()

    @app.errorhandler(BaseError)
    def handle_error(error: BaseError):
        from main.libs.log import ServiceLogger

        logger = ServiceLogger(__name__)

        status_code = error.status_code
        if isinstance(status_code, int) and status_code not in [401, 403, 500]:
            logging_method = logger.warning
        else:
            logging_method = logger.error

        logging_method(
            message=error.error_message,
            data={
                'error_data': error.error_data,
            },
        )
        return error.to_response()

    @app.errorhandler(Exception)
    def handle_exception(e):
        from main.libs.log import ServiceLogger

        logger = ServiceLogger(__name__)
        logger.exception(message=str(e))
        return InternalServerError().to_response()
