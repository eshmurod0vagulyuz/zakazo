from core.db_settings import execute_query

def create_user(username, password):
    """Adding a new user to the database"""
    query = """
        INSERT INTO users (username, password) 
        VALUES (%s, %s) 
        RETURNING id;
    """

    return execute_query(query, (username, password), fetch="one")

def get_user_by_username(username):
    """Find a user by username"""
    query = "SELECT * FROM users WHERE username = %s;"
    return execute_query(query, (username,), fetch="one")

def update_user_login_status(user_id, status: bool):
    query = "UPDATE users SET is_login = %s WHERE id = %s;"
    return execute_query(query, (status, user_id))

def get_all_users():
    """Get a list of all users for admin."""
    query = "SELECT id, username, created_at FROM users;"
    result = execute_query(query, fetch="all")
    return result if result is not None else []