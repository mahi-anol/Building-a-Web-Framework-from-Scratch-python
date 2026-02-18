from webob.response import Response
from App import app

@app.route("/static")
def static_view(request)->Response:
    return Response(body="<h1>This is a static view</h1")


@app.route('/dashboard')
def dashboard(request)->Response:
    name="Mahi"
    title="Dashboard view"
    html_content=app.template(template_name="dashboard.html",context={'name':name,'title':title})
    return Response(body=html_content)
# @app.route('/dashboard')
# def dashboard(request)->Response:
#     name="Mahi"
#     return Response(body=f"<h1>Hello {name}, welcome to the Dashboard</h1>")