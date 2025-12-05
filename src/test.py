import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_calc_get(client):
    """Тест GET-запроса к /calc"""
    response = client.get('/calc')
    assert response.status_code == 200
    assert 'Первое число:' in response.get_data(as_text=True)
    assert 'Второе число:' in response.get_data(as_text=True)
    assert '<form method = "post">' in response.get_data(as_text=True)

def test_calc_post_valid(client):
    """Тест POST-запроса с валидными данными"""
    response = client.post('/calc', data={'a': '5', 'b': '3'})
    assert response.status_code == 200
    assert 'Сумма: 8' in response.get_data(as_text=True)

def test_calc_post_negative_numbers(client):
    """Тест с отрицательными числами"""
    response = client.post('/calc', data={'a': '-5', 'b': '10'})
    assert response.status_code == 200
    assert 'Сумма: 5' in response.get_data(as_text=True)

def test_calc_post_zero(client):
    """Тест с нулями"""
    response = client.post('/calc', data={'a': '0', 'b': '0'})
    assert response.status_code == 200
    assert 'Сумма: 0' in response.get_data(as_text=True)

def test_calc_post_large_numbers(client):
    """Тест с большими числами"""
    response = client.post('/calc', data={'a': '1000000', 'b': '2000000'})
    assert response.status_code == 200
    assert 'Сумма: 3000000' in response.get_data(as_text=True)

def test_calc_post_empty_string(client):
    """Тест с пустыми строками (вызовет ValueError)"""
    response = client.post('/calc', data={'a': '', 'b': ''})
    # Ожидаем ошибку 500 или обработку исключения
    assert response.status_code == 500

def test_calc_post_non_numeric(client):
    """Тест с нечисловыми значениями (вызовет ValueError)"""
    response = client.post('/calc', data={'a': 'abc', 'b': 'xyz'})
    assert response.status_code == 500

def test_calc_post_missing_data(client):
    """Тест с отсутствующими данными"""
    response = client.post('/calc', data={'a': '5'})  # b отсутствует
    assert response.status_code == 500

def test_calc_post_float_numbers(client):
    """Тест с дробными числами (может вызвать ValueError при int())"""
    response = client.post('/calc', data={'a': '5.5', 'b': '2.5'})
    # int() не работает с float в строковом виде, поэтому ожидаем ошибку
    assert response.status_code == 500

def test_calc_post_float_numbers_handled(client):
    """Тест обработки дробных чисел в улучшенной версии"""
    response = client.post('/calc', data={'a': '5.5', 'b': '2.5'})
    assert response.status_code == 400
    assert 'Ошибка: введите целые числа' in response.get_data(as_text=True)