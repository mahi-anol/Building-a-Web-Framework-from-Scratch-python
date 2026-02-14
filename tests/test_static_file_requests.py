from tests.constants import BASE_URL
from webob import Response
from tests.conftest import TFramework


def test_static_file_n_exists_request(app,client):
    response:Response=client.get(f"{BASE_URL}/css/style.css")
    assert response.status_code==404

def test_static_file_not_exists_request(static_dir):

    app=TFramework(static_dir=static_dir)
    client=app.test_session()
    response:Response=client.get(f"{BASE_URL}/css/mahi.css")
    assert response.status_code==404


def test_static_file_not_exists_request(static_dir):
    dir_name="css"
    file_name="style.css"
    asset=static_dir.mkdir(dir_name).join(file_name)
    file_content="body {background-color:red}"
    asset.write(file_content)
    app=TFramework(static_dir=static_dir)
    client=app.test_session()
    response:Response=client.get(f"{BASE_URL}/{dir_name}/{file_name}")
    assert response.status_code==200
    