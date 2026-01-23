from collections.abc import Callable
from typing import Any

from psycopg2.extras import DictRow

from auth.confirmation import generate_code, send_email
from core.db_settings import execute_query


def register() -> bool:
    """
    Register new users
    :return: True if success else False
    """
    username: str = input("Username: ")
    email: str = input("Email: ")
    password: str = input("Password: ")

    # check email if exists or not
    # ask password twice
    query: str = "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)"
    params: tuple[str, str, str] = (username, email, password,)

    if execute_query(query=query, params=params):
        code = generate_code(user_email=email)
        if send_email(
                recipient_email=email, subject="Confirmation code",
                body=f"This is your code: {code}"
        ):
            print("Code sent to your email")
            if validate():
                return True
            return False
        else:
            print("Something went wrong, try again later")
            return False
    else:
        print("Something went wrong, try again later")
        return False


def validate() -> Callable | bool:
    """
    Validate user by giving one time password
    :return: True if success else return back
    """
    code: str = input("Code: ")
    query: str = "SELECT * FROM codes WHERE code = %s"
    params: tuple[str] = (code,)
    user_code: DictRow | None = execute_query(query=query, params=params, fetch="one")

    if user_code:
        query1 = "DELETE FROM codes WHERE code = %s"
        params1 = (code,)
        execute_query(query=query1, params=params1)

        query2 = "UPDATE users SET is_active=True WHERE email = %s"
        params2 = (user_code['email'],)
        execute_query(query=query2, params=params2)

        return True
    else:
        print("Invalid code")
        return validate()


def login() -> bool:
    """
    Login by email
    :return: True if success else False
    """
    email: str = input("Email: ")
    password: str = input("Password: ")

    query: str = "SELECT * FROM users WHERE email=%s AND password=%s"
    params: tuple[str, str] = (email, password,)

    if execute_query(query=query, params=params, fetch="one"):
        query2 = "UPDATE users SET is_login=True WHERE email = %s"
        params2 = (email,)
        execute_query(query=query2, params=params2)

        return True
    return False


def get_active_user() -> DictRow | None | list[tuple[Any, ...]]:
    """
    Get active user that is login currently
    :return:
    """
    query = "SELECT * FROM users WHERE is_login=TRUE"
    return execute_query(query=query, fetch="one")


def logout_all() -> None:
    """
    Update all user is_login to False
    :return:
    """
    query1 = "UPDATE users SET is_login=False"
    execute_query(query=query1)