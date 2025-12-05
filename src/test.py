import pytest
from flask import Flask
from app import app  # импортируйте ваше приложение

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_get_request(client):
    response = client.get('/calc')
    assert response.status_code == 200
    assert 'Первое число' in response.data.decode('utf-8')
    assert 'Второе число' in response.data.decode('utf-8')

def test_post_request_with_valid_numbers(client):
    response = client.post('/calc', data={'a': '5', 'b': '3'})
    assert response.status_code == 200
    assert 'Сумма: 8' in response.data.decode('utf-8')

def test_post_request_with_invalid_input(client):
    response = client.post('/calc', data={'a': 'abc', 'b': '3'})
    assert response.status_code == 500  # или другой ожидаемый статус

def test_post_request_with_empty_fields(client):
    response = client.post('/calc', data={'a': '', 'b': ''})
    assert response.status_code == 500  # или другой ожидаемый статус