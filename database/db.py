import psycopg2
from psycopg2 import pool
from contextlib import contextmanager
from settings.config import db_config

# Класс для управления подключением к базе данных
class Database:
    def __init__(self, db_config):
        self.pool = pool.SimpleConnectionPool(1, 10, **db_config)

    @contextmanager
    def get_conn(self):
        conn = self.pool.getconn()
        try:
            yield conn
        finally:
            self.pool.putconn(conn)


db = Database(db_config)


# Базовый класс для всех моделей
class BaseModel:
    def __init__(self, db):
        self.db = db

    @contextmanager
    def get_cursor(self):
        with self.db.get_conn() as conn:
            with conn.cursor() as cursor:
                yield cursor
            conn.commit()


# Класс для работы с пользователями
class User(BaseModel):
    def create_user(self, first_name, last_name, username):
        with self.get_cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO users (first_name, last_name, username)
                VALUES (%s, %s, %s) RETURNING user_id;
                """,
                (first_name, last_name, username)
            )
            user_id = cursor.fetchone()[0]
            return user_id

    def get_user(self, user_id):
        with self.get_cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE user_id = %s;", (user_id,))
            return cursor.fetchone()

    def update_user(self, user_id, first_name=None, last_name=None, username=None):
        fields = []
        values = []
        if first_name:
            fields.append("first_name = %s")
            values.append(first_name)
        if last_name:
            fields.append("last_name = %s")
            values.append(last_name)
        if username:
            fields.append("username = %s")
            values.append(username)

        values.append(user_id)
        with self.get_cursor() as cursor:
            cursor.execute(
                f"UPDATE users SET {', '.join(fields)} WHERE user_id = %s;",
                tuple(values)
            )

    def delete_user(self, user_id):
        with self.get_cursor() as cursor:
            cursor.execute("DELETE FROM users WHERE user_id = %s;", (user_id,))

    def assign_role(self, user_id, role_id):
        with self.get_cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO user_roles (user_id, role_id)
                VALUES (%s, %s);
                """,
                (user_id, role_id)
            )


# Класс для работы с чатами
class Chat(BaseModel):
    def create_chat(self, chat_name):
        with self.get_cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO chats (chat_name)
                VALUES (%s) RETURNING chat_id;
                """,
                (chat_name,)
            )
            chat_id = cursor.fetchone()[0]
            return chat_id

    def get_chat(self, chat_id):
        with self.get_cursor() as cursor:
            cursor.execute("SELECT * FROM chats WHERE chat_id = %s;", (chat_id,))
            return cursor.fetchone()

    def update_chat(self, chat_id, chat_name):
        with self.get_cursor() as cursor:
            cursor.execute(
                "UPDATE chats SET chat_name = %s WHERE chat_id = %s;",
                (chat_name, chat_id)
            )

    def delete_chat(self, chat_id):
        with self.get_cursor() as cursor:
            cursor.execute("DELETE FROM chats WHERE chat_id = %s;", (chat_id,))

    def add_user_to_chat(self, chat_id, user_id, role):
        with self.get_cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO user_chat_roles (chat_id, user_id, role)
                VALUES (%s, %s, %s);
                """,
                (chat_id, user_id, role)
            )


# Класс для работы с задачами
class Task(BaseModel):
    def create_task(self, title, description, due_date, user_id=None, chat_id=None):
        with self.get_cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO tasks (title, description, due_date, user_id, chat_id)
                VALUES (%s, %s, %s, %s, %s) RETURNING task_id;
                """,
                (title, description, due_date, user_id, chat_id)
            )
            task_id = cursor.fetchone()[0]
            return task_id

    def get_task(self, task_id):
        with self.get_cursor() as cursor:
            cursor.execute("SELECT * FROM tasks WHERE task_id = %s;", (task_id,))
            return cursor.fetchone()

    def update_task(self, task_id, title=None, description=None, due_date=None, completed=None):
        fields = []
        values = []
        if title:
            fields.append("title = %s")
            values.append(title)
        if description:
            fields.append("description = %s")
            values.append(description)
        if due_date:
            fields.append("due_date = %s")
            values.append(due_date)
        if completed is not None:
            fields.append("completed = %s")
            values.append(completed)

        values.append(task_id)
        with self.get_cursor() as cursor:
            cursor.execute(
                f"UPDATE tasks SET {', '.join(fields)} WHERE task_id = %s;",
                tuple(values)
            )

    def delete_task(self, task_id):
        with self.get_cursor() as cursor:
            cursor.execute("DELETE FROM tasks WHERE task_id = %s;", (task_id,))


# Класс для работы с администраторами
class Admin(BaseModel):
    def create_admin(self, user_id, role_id):
        with self.get_cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO administrators (user_id, role_id)
                VALUES (%s, %s) RETURNING admin_id;
                """,
                (user_id, role_id)
            )
            admin_id = cursor.fetchone()[0]
            return admin_id

    def get_admin(self, admin_id):
        with self.get_cursor() as cursor:
            cursor.execute("SELECT * FROM administrators WHERE admin_id = %s;", (admin_id,))
            return cursor.fetchone()

    def delete_admin(self, admin_id):
        with self.get_cursor() as cursor:
            cursor.execute("DELETE FROM administrators WHERE admin_id = %s;", (admin_id,))


# Класс для работы с уведомлениями
class Notification(BaseModel):
    def create_notification(self, user_id, chat_id, message):
        with self.get_cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO notifications (user_id, chat_id, message)
                VALUES (%s, %s, %s) RETURNING notification_id;
                """,
                (user_id, chat_id, message)
            )
            notification_id = cursor.fetchone()[0]
            return notification_id

    def get_notification(self, notification_id):
        with self.get_cursor() as cursor:
            cursor.execute("SELECT * FROM notifications WHERE notification_id = %s;", (notification_id,))
            return cursor.fetchone()

    def mark_as_read(self, notification_id):
        with self.get_cursor() as cursor:
            cursor.execute("UPDATE notifications SET read = TRUE WHERE notification_id = %s;", (notification_id,))
