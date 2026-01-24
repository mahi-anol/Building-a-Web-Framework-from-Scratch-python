from contants import HttpStatus
from helpers import json_response
class Handlers:
    @staticmethod
    def generic_exception_handler(environ,start_response,ex:Exception)->list[bytes]:
        response={
            "message": f" Unhandled exception occured {str(ex)}"
        }
        return json_response(
            response=response,
            start_response=start_response,
            status=HttpStatus.INTERNAL_SERVER_ERROR
        )