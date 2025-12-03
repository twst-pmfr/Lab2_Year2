from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import os

# 🔍 Создание экземпляра приложения
app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # 🔐 Для сессий и flash-сообщений


# 🔍 База данных
def init_db():
    """Инициализация базы данных"""
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Создание таблицы пользователей
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()


# 🔍 Главная страница
@app.route('/')
def index():
    """Главная страница"""
    return render_template('index.html', title='Главная страница')


# 🔍 Страница "О нас"
@app.route('/about')
def about():
    """Страница о компании"""
    return render_template('about.html', title='О нас')


# 🔍 Страница с пользователями
@app.route('/users')
def users():
    """Отображение списка пользователей"""
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM users ORDER BY created_at DESC')
    users = cursor.fetchall()

    conn.close()

    return render_template('users.html', title='Пользователи', users=users)


# 🔍 Добавление пользователя
@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    """Добавление нового пользователя"""
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']

        try:
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()

            cursor.execute(
                'INSERT INTO users (name, email) VALUES (?, ?)',
                (name, email)
            )

            conn.commit()
            conn.close()

            flash('Пользователь успешно добавлен!', 'success')
            return redirect(url_for('users'))

        except sqlite3.IntegrityError:
            flash('Пользователь с таким email уже существует!', 'error')

    return render_template('add_user.html', title='Добавить пользователя')


# 🔍 API endpoint для получения пользователей в JSON
@app.route('/api/users')
def api_users():
    """API для получения пользователей в формате JSON"""
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()

    conn.close()

    # Преобразование в список словарей
    users_list = []
    for user in users:
        users_list.append({
            'id': user[0],
            'name': user[1],
            'email': user[2],
            'created_at': user[3]
        })

    return {'users': users_list}


# 🔍 Обработка ошибок
@app.errorhandler(404)
def page_not_found(error):
    """Обработка ошибки 404"""
    return render_template('404.html', title='Страница не найдена'), 404


# 🔍 Запуск приложения
if __name__ == '__main__':
    init_db()  # Инициализируем базу данных
    app.run(debug=True, host='0.0.0.0', port=5000)