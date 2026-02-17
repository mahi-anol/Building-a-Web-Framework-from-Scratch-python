from webob import Request, Response
from Framework.constants import HttpStatus
import logging
from Framework.exceptions import ResponseError
logger=logging.getLogger(__name__)


class CommonHandlers:
    @staticmethod
    def generic_exception_handler(request:Request,excp:Exception)->Response:
        logger.exception(excp)
        response={
            "message":f"Unhandled Exception Occured: {str(excp)}"
        }
        return Response(
            json_body=response,
            status=HttpStatus.INTERNAL_SERVER_ERROR
        )
    
    @staticmethod
    def url_not_found_handler(request:Request)->Response:
        response={
            "message":f"Request Path: {request.path} does not exist"
        }
        return Response(
            json_body=response,
            status=HttpStatus.NOT_FOUND
        )
    
    @staticmethod
    def method_not_allowed_handler(request:Request)->Response:
        response={
            "message":f"{request.method} request is not allowed for {request.path}"
        }
        return Response(
            json_body=response,
            status=HttpStatus.METHOD_NOT_ALLOWED
        )
    @staticmethod
    def handle_response_error(request:Request,exc:ResponseError)->Response:
        logger.exception(exc)
        response={
            "message": exc.message
        }
        return Response(
            json_body=response,
            status=exc.htto_status
        )