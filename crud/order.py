from core.db_settings import execute_query
from crud.menu import update_menu_amount


def create_order(user_id, menu_product_id, amount, duration_id, table_number):
    """Create a new order and reduce the number of meals"""

    stock_updated = update_menu_amount(menu_product_id, amount)

    if not stock_updated:
        return False, "Not enough food!"


    query = """
        INSERT INTO orders (user_id, menu_product_id, amount, duration_id, table_number, status, order_type)
        VALUES (%s, %s, %s, %s, %s, 'pending', 'dine_in')
    """
    params = (user_id, menu_product_id, amount, duration_id, table_number)

    success = execute_query(query, params)
    if success:
        return True, "Order accepted!"
    return False, "Error"


def get_user_orders(user_id):
    """View all user orders"""
    query = """
        SELECT o.id, p.title, o.amount, d.from_time, o.table_number, o.status
        FROM orders o
        JOIN menu_products m ON o.menu_product_id = m.id
        JOIN products p ON m.product_id = p.id
        JOIN durations d ON o.duration_id = d.id
        WHERE o.user_id = %s;
    """
    result = execute_query(query, (user_id,), fetch="all")
    return result if result else []