from flask import Flask
from flask import render_template
from flask import request
app =Flask(__name__)

@app.route('/')
def hello():
    return 'HELLO'


@app.route('/login', methods = ['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        return f'Попытка входа: {username}'
    else:
        return '''
            <form method = "post">
                Логин: <input name="username"><br>
                Пароль: <input name="password" type ="password"><br>
                <button type="submit">Войти</button>
            </form>

            '''
    
@app.route('/calc', methods = ['GET','POST'])
def calc():
    if request.method == 'POST':
        a = request.form.get('a')
        b = request.form.get('b')
        try:
            result = int(a) + int(b)
            return f'Сумма: {result}'
        except (ValueError, TypeError):
            return 'Ошибка: введите числа', 400
    else:
        return '''
            <form method = "post" >
                Первое число: <input name="a"><br>
                Второе число: <input name="b"><br>
                <button type="submit">Рассчитать</button>
            </form>

            '''


#init
if __name__ == '__main__':
    app.run(port=3001)