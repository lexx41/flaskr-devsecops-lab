import os
from flask import Flask, request, render_template  # Безопасная функция 

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    # ИСПРАВЛЕНИЕ 1: Использование переменных окружения для секретов (вместо хардкода)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', os.urandom(24))

    # ИСПРАВЛЕНИЕ 2: Debug mode off в production
    app.config['DEBUG'] = os.environ.get('FLASK_DEBUG', 'False') == 'True'

    @app.route('/')
    def index():
        # ИСПРАВЛЕНИЕ 3: Безопасное экранирование ввода (используем render_template 
        name = request.args.get('name', 'Guest')
        return render_template('index.html', name=name)

    @app.route('/admin')
    def admin():
        # ИСПРАВЛЕНИЕ 4: Добавлена проверка аутентификации
        auth_token = request.headers.get('Authorization')
        expected_token = os.environ.get('ADMIN_TOKEN')
        if not auth_token or auth_token != f'Bearer {expected_token}':
            return 'Unauthorized', 401
        return 'Admin panel'

    # ИСПРАВЛЕНИЕ 5: Удаляем опасный endpoint /eval
  

    return app
