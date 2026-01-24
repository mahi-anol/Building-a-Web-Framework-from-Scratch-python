from contants import HttpStatus
from helpers import json_response
import logging
from webob import Request,Response

logger=logging.getLogger(__name__)

class Handlers:
    @staticmethod
    def generic_exception_handler(request:Request,ex:Exception)->Response:
        logger.exception(ex)
        response={
            "message": f" Unhandled exception occured {str(ex)}"
        }
        return Response(json_body=response,status=HttpStatus.INTERNAL_SERVER_ERROR)
    
    @staticmethod
    def url_not_found_handler(request:Request)->Response:
        response={
            "message": f"Requested path:{request.path} does not exist"
        }
        return Response(json_body=response,status=HttpStatus.NOT_FOUND)