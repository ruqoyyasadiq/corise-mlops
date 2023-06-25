import os
from fastapi.testclient import TestClient
from .app.server import app
from .app.classifier import NewsCategoryClassifier

os.chdir('app')
client = TestClient(app)

"""
We've built our web application, and containerized it with Docker.
But imagine a team of ML engineers and scientists that needs to maintain, improve and scale this service over time. 
It would be nice to write some tests to ensure we don't regress! 

  1. `Pytest` is a popular testing framework for Python. If you haven't used it before, take a look at https://docs.pytest.org/en/7.1.x/getting-started.html to get started and familiarize yourself with this library.

  2. How do we test FastAPI applications with Pytest? Glad you asked, here's two resources to help you get started:
    (i) Introduction to testing FastAPI: https://fastapi.tiangolo.com/tutorial/testing/
    (ii) Testing FastAPI with startup and shutdown events: https://fastapi.tiangolo.com/advanced/testing-events/
"""


def test_root():
    """
    [TO BE IMPLEMENTED]
    Test the root ("/") endpoint, which just returns a {"Hello": "World"} json response
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}


def test_predict_empty():
    """
    [TO BE IMPLEMENTED]
    Test the "/predict" endpoint, with an empty request body
    """
    response = client.post("/predict")
    assert response.status_code == 422


def test_predict_en_lang():
    """
    [TO BE IMPLEMENTED]
    Test the "/predict" endpoint, with an input text in English (you can use one of the test cases provided in README.md)
    """
    request_body = {
        "source": "BBC Technology",
        "url": "http://news.bbc.co.uk/go/click/rss/0.91/public/-/2/hi/business/4144939.stm",
        "title": "System gremlins resolved at HSBC",
        "description": "Computer glitches which led to chaos for HSBC customers on Monday are fixed, the High Street bank confirms."
    }
    
    with TestClient(app) as client:
        response = client.post("/predict", json=request_body)
        assert response.status_code == 200
        assert response.json()['label'] == "Business"


def test_predict_es_lang():
    """
    [TO BE IMPLEMENTED]
    Test the "/predict" endpoint, with an input text in Spanish. 
    Does the tokenizer and classifier handle this case correctly? Does it return an error?
    """
    request_body = {
        "source": "Tecnología de la BBC",
        "url": "http://aleatorio.co.uk/",
        "title": "Gremlins del sistema resueltos en HSBC",
        "description": "Los problemas informáticos que provocaron el caos para los clientes de HSBC el lunes se solucionaron, confirma el banco High Street."
    }

    with TestClient(app) as client:
        response = client.post("/predict", json=request_body)
        assert response.status_code == 200
        assert response.json()['label'] == "Business"

    '''
    The token and classifier is able to handle this case correctly.
    The testcase used is the direct spanish translation of the previous testcase.
    '''


def test_predict_non_ascii():
    """
    [TO BE IMPLEMENTED]
    Test the "/predict" endpoint, with an input text that has non-ASCII characters. 
    Does the tokenizer and classifier handle this case correctly? Does it return an error?
    """
    request_body = {
        "source": "Tecnología de la BBC",
        "url": "http://aleatorio.co.uk/",
        "title": "Gremlins del sistema resueltos en HSBC",
        "description": "¡™£´åßƒ∂ƒ©˙ƒ´ß†®¥†®¨ˆ£"
    }

    with TestClient(app) as client:
        response = client.post("/predict", json=request_body)
        assert response.status_code == 200
        assert response.json()['label'] == "Entertainment"

    '''
    The token and classifier is able to handle non-ascii characters.
    Although the predictions don't add up given the incoherent jargon fed in as input.
    '''
