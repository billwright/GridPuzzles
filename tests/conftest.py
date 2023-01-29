import pytest
from puzzle_service import app


@pytest.fixture()
def service():
    # app.config.update({
    #     "TESTING": True,
    # })

    # other setup can go here

    yield app

    # clean up / reset resources here


@pytest.fixture()
def client(service):
    return app.test_client()

