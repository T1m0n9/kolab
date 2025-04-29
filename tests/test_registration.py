import pytest
import sqlite3
import os
from registration.registration import create_db, add_user, authenticate_user, display_users

@pytest.fixture(scope="module")
def setup_database():
    """Фикстура для настройки базы данных перед тестами и её очистки после."""
    create_db()
    yield
    try:
        os.remove('users.db')
    except PermissionError:
        pass

@pytest.fixture
def connection():
    """Фикстура для получения соединения с базой данных и его закрытия после теста."""
    conn = sqlite3.connect('users.db')
    yield conn
    conn.close()


def test_create_db(setup_database, connection):
    """Тест создания базы данных и таблицы пользователей."""
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
    table_exists = cursor.fetchone()
    assert table_exists, "Таблица 'users' должна существовать в базе данных."

def test_add_new_user(setup_database, connection):
    """Тест добавления нового пользователя."""
    add_user('testuser', 'testuser@example.com', 'password123')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE username='testuser';")
    user = cursor.fetchone()
    assert user, "Пользователь должен быть добавлен в базу данных."

# Возможные варианты тестов:

def test_add_user_exist():
    
    assert add_user('user1', 'user1@MAIL.RU', 'user1') == True
    assert add_user('user1', 'user1@MAIL.RU', 'user1') == False

def test_connect_user():
    add_user('user2','user2@mail.ru','user2')
    assert authenticate_user('user2','user2') == True

def test_connect_nonuser():
    assert authenticate_user('123','123') == False

def test_connect_poruser():
    add_user('user3','user3','user3')
    assert authenticate_user('user3','123') == False

def test_display_users(setup_database, capsys):
    """Тест корректного отображения списка пользователей."""
    add_user('displaytest', 'displaytest@example.com', 'password123')
    display_users()
    captured = capsys.readouterr()
    assert 'displaytest' in captured.out, "Функция отображения должна выводить логины пользователей."
    assert 'password123' not in captured.out, "Пароли не должны отображаться."

"""
Тест добавления пользователя с существующим логином.
Тест успешной аутентификации пользователя.
Тест аутентификации несуществующего пользователя.
Тест аутентификации пользователя с неправильным паролем.
Тест отображения списка пользователей.
"""