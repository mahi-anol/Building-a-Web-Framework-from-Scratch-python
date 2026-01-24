from contants import HttpStatus
from helpers import json_response
import logging

logger=logging.getLogger(__name__)
class Handlers:
    @staticmethod
    def generic_exception_handler(environ,start_response,ex:Exception)->list[bytes]:
        logger.exception(ex)
        response={
            "message": f" Unhandled exception occured {str(ex)}"
        }
        return json_response(
            response=response,
            start_response=start_response,
            status=HttpStatus.INTERNAL_SERVER_ERROR
        )
    
    @staticmethod
    def url_not_found_handler(environ,start_response)->list[bytes]:
        path=environ.get('PATH_INFO','/')
        response={
            "message": f"Requested path:{path} does not exist"
        }
        return json_response(
            response=response,
            start_response=start_response,
            status=HttpStatus.NOT_FOUND
        )