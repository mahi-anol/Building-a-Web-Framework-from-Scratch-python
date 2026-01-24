class HttpStatus:
    OK="200 OK"
    INTERNAL_SERVER_ERROR="500 Internal Server Error"
    NOT_FOUND="404 Not Found"
    METHOD_NOT_ALLOWED="405 Method Not Allowed"

class JsonContentType:
    type=('content-type','text/json')


inventory={

    "mobile":[
        {
            "product_id":1,"product_name":"S25 ultra","brand":"Samsung"
        },
        {
            "product_id":2,"product_name":"iphone","brand":"Apple"
        }
    ],
    "laptop":[
        {
            "product_id":3,"product_name":"Macbook Pro M4","brand":"Apple"
        },
        {
            "product_id":4,"product_name":"Dell XPS","brand":"Dell"
        }
    ]
}

products=[
        {
            "id":1,"product_name":"S25 ultra","brand":"Samsung"
        },
        {
            "id":2,"product_name":"iphone","brand":"Apple"
        }
    ]