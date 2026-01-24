import json
from contants import HttpStatus,JsonContentType

def json_response(response: dict | list[dict],start_response,status=HttpStatus.OK,response_headers=[]):
    response_body=json.dumps(response)

    response_headers = []
    
    response_headers.append(JsonContentType.type)
    # print(response_headers)
   
    start_response(status,response_headers)
    return [response_body.encode("utf-8")]